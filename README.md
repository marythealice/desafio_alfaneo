Para construir a imagem do projeto com docker, insira o comando a seguir:

docker build -t "desafio_alfaneo" .

Para rodar a aplicação com a imagem gerada:

docker run -it --name web_scraper_api -p 8000:8000 desafio_alfaneo:latest
