# Cadastro de Produtos com Streamlit, Azure Blob Storage e SQL Server

Este projeto é uma aplicação web para cadastro e listagem de produtos, desenvolvida com [Streamlit](https://streamlit.io/), integrando armazenamento de imagens no [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs/) e persistência de dados em um banco de dados [SQL Server](https://www.microsoft.com/en-us/sql-server/).

<p align="center">
  <img src="https://th.bing.com/th/id/R.7b5d07f05da6bbea20429b051fd4f29d?rik=ZTC0CNdd9k2IGQ&pid=ImgRaw&r=0" alt="Azure Blob Storage" height="90"/>
  <img src="https://www.python.org/static/community_logos/python-logo.png" alt="Python" height="90"/>
  <img src="https://th.bing.com/th/id/OIP.pofVW4p6qp0s6h9GblYjagHaF-?rs=1&pid=ImgDetMain" alt="SQL Server" height="90"/>
  <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" alt="Streamlit" height="90"/>
</p>

## Funcionalidades

- Cadastro de produtos com nome, preço, descrição e imagem.
- Upload de imagens para o Azure Blob Storage.
- Listagem dos produtos cadastrados, exibindo informações e imagem.
- Interface web simples e intuitiva com Streamlit.

## Tecnologias Utilizadas

- ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white&style=flat-square) Framework Python para criação rápida de aplicações web interativas.
- ![Azure Blob Storage](https://img.shields.io/badge/Azure%20Blob%20Storage-0089D6?logo=microsoft-azure&logoColor=white&style=flat-square) Serviço de armazenamento de objetos para guardar as imagens dos produtos.
- ![SQL Server](https://img.shields.io/badge/SQL%20Server-CC2927?logo=microsoft-sql-server&logoColor=white&style=flat-square) Banco de dados relacional para armazenar os dados dos produtos.
- ![pyodbc](https://img.shields.io/badge/pyodbc-3776AB?logo=python&logoColor=white&style=flat-square) Driver ODBC para conexão Python com SQL Server.
- ![azure-storage-blob](https://img.shields.io/badge/azure--storage--blob-0089D6?logo=microsoft-azure&logoColor=white&style=flat-square) SDK Python para integração com o Azure Blob Storage.
- ![python-dotenv](https://img.shields.io/badge/python--dotenv-3776AB?logo=python&logoColor=white&style=flat-square) Gerenciamento de variáveis de ambiente.
- ![uuid](https://img.shields.io/badge/uuid-3776AB?logo=python&logoColor=white&style=flat-square) Geração de identificadores únicos para nomes de arquivos.

## Como Executar

1. **Clone o repositório:**
   ```sh
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. **Instale as dependências:**
   pip install -r requirements.txt

**Estrutura do Código**

**Formulário de cadastro:** Permite inserir nome, preço, descrição e imagem do produto.<br>
**Upload de imagem:** Salva a imagem no Azure Blob Storage e retorna a URL.<br>
**Inserção no banco:** Salva os dados do produto no SQL Server, incluindo a URL da imagem.<br>
**Listagem de produtos:** Exibe os produtos cadastrados em cards, mostrando nome, descrição, preço e imagem.<br>

**Licença**<br>
Este projeto é distribuído sob a licença MIT.
