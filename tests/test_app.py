from fastapi.testclient import TestClient
from http import HTTPStatus
from scraper.app import app

client = TestClient(app)

def test_post_deve_retornar_400_com_nome_vazio():
    response = client.post("/fetch_oab", 
        json={
            "name": "",
            "uf": "MS"
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Campo de nome não pode ser vazio."}

def test_post_deve_retornar_400_com_uf_vazia():
    response = client.post("/fetch_oab", 
        json={
            "name": "Luiz Antonio de Souza Basilio",
            "uf": ""
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Campo de uf não pode ser vazio."}

def test_post_deve_retornar_400_com_uf_invalida():
    response = client.post("/fetch_oab", 
        json={
            "name": "Luiz Antonio de Souza Basilio",
            "uf": "ST"
        }
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail":"'uf' inserida não é valida: ST."}

def test_post_deve_retornar_404_se_advogado_nao_for_encontrado():
    response = client.post("/fetch_oab", 
        json={
            "name": "Maria Alice Nantes Nunes",
            "uf": "MS"
        }
    )

    assert response.status_code == HTTPStatus.NOT_FOUND



def test_post_deve_retornar_200_com_nome_e_uf_preenchidos_e_advogado_existente():
    response = client.post("/fetch_oab", 
        json={
            "name": "Luiz Antonio de Souza Basilio",
            "uf": "ES"
        }
    )

    assert response.status_code == HTTPStatus.OK
