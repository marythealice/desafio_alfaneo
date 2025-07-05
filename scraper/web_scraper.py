import os
import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait


def fetch_data(full_name: str, state: str):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    driver = webdriver.Remote(
        command_executor=os.environ["SELENIUM_REMOTE_URL"],
        options=chrome_options
    )
    driver.get("https://cna.oab.org.br")

    name_input = driver.find_element(By.ID, "txtName")
    name_input.clear()
    name_input.send_keys(full_name)

    select_state_box = driver.find_element(By.ID, "cmbSeccional")
    select_state = Select(select_state_box)
    select_state.select_by_value(state)

    search_button = driver.find_element(By.ID, "btnFind")
    search_button.click()


    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//html/body/div[2]/div[1]/div[2]/div[2]/div[1]"))
        WebDriverWait(driver, 10).until(element_present)
        print("Page is ready!")
    except TimeoutException:
        print("entrou execao")
        return None
    
    row_element = driver.find_element(By.XPATH, "//html/body/div[2]/div[1]/div[2]/div[2]/div[1]")
    row_element.click()

    try:
        element_present = EC.presence_of_element_located((By.ID, "imgDetail"))
        WebDriverWait(driver, 10).until(element_present)
        print("Page is ready!")
    except TimeoutError:
        print("Loading took time!")


    img = driver.find_element(By.ID, "imgDetail")
    img_url = img.get_attribute("src")

    response = requests.get(img_url)
    with open("detalhes.png", "wb") as f:
        f.write(response.content)
    print("separando")
    image = Image.open("detalhes.png")
    text = pytesseract.image_to_string(image, lang="por")
    info_array = []

    if "regular" in text.lower():
        info_array.append("ativo")
    else:
        info_array.append("inativo")


    soup = BeautifulSoup(driver.page_source, "html.parser")
    div_result = soup.find("div", {"id": "divResult"})
    child = div_result.findChild("div")

    for info in child.find_all("span"):
        info_array.append(info.get_text())

    items_to_remove = {'1', 'Nome:', 'Tipo:','Inscrição:','UF:'}

    info_array = list(filter(lambda x: x not in items_to_remove, info_array))

    if os.path.exists("detalhes.png"):
        os.remove("detalhes.png")

    data_response = {"oab": info_array[3], "nome": info_array[1], "uf":info_array[4], "categoria": info_array[2], "situacao": info_array[0]}
    print(data_response)
    driver.quit()
    return data_response

