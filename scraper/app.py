from fastapi import FastAPI, HTTPException
from scraper.web_scraper import fetch_data
from scraper.models import Request, Response, valid_ufs
from requests.exceptions import HTTPError

app = FastAPI()

@app.post("/fetch_oab/", response_model=Response)
async def fetch_oab_data(request: Request):
    if (request.name == ""):
        raise HTTPException(status_code=400, detail=f"Campo de nome não pode ser vazio.")

    if (request.uf == ""):
        raise HTTPException(status_code=400, detail=f"Campo de uf não pode ser vazio.")
    elif (request.uf != request.uf.upper()):
        request.uf = request.uf.upper()
    if (request.uf not in valid_ufs):
        raise HTTPException(status_code=400, detail=f"'uf' inserida não é valida: {request.uf}.")
    try:
        result = fetch_data(request.name, request.uf)
        if (result is None):
            raise HTTPException(status_code=404, detail="Advogado não encontrado.")

        return result
    
    except HTTPError as e:
        print(f"Houve um erro: {e}")