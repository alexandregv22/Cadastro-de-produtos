import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pyodbc
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=stadevlab001eastus1;AccountKey=8bZ1WGGJE5TtXFGElzYwrE8AO2a6tTyQzBHqcudhjBAMP0XUenCBnX56t6DqV9CnM+lhuF0x2p8p+AStja97WQ==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "fotos"
ACCOUNT_NAME = "stadevlab001eastus1"

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")

#formulario de cadastro de produto
product_name = st.text_input("Nome do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_description = st.text_area("Descrição do Produto")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

#Salvar image on blob storage
def upload_blob(file):
    blob_service_client = BlobServiceClient.from_connection_string(CONNECTION_STRING)
    container_client = blob_service_client.get_container_client(CONTAINER_NAME)
    blob_name = str(uuid.uuid4()) + file.name
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file.read(), overwrite=True)
    image_url = f"https://{ACCOUNT_NAME}.blob.core.windows.net/{CONTAINER_NAME}/{blob_name}"
    return image_url

def insert_product(product_name, product_price, product_description, product_image):
    try:
        image_url = upload_blob(product_image)
        conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USER};PWD={SQL_PASSWORD}")
        cursor = conn.cursor()
        insert_sql = f"INSERT INTO Produtos (nome, preco, descricao, imagem_url) VALUES ('{product_name}', {product_price}, '{product_description}', '{image_url}')"
        print(insert_sql)
        cursor.execute(insert_sql)
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        st.error(f"Erro ao inserir produto: {e}")
        return False

def list_products():
    try:
        conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USER};PWD={SQL_PASSWORD}")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Produtos")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        st.error(f"Erro ao listar produtos: {e}")
        return []
    
def list_products_screen():
    products = list_products()
    if products:
    #Define o número de cards por linha
        cards_por_linha = 3
        # Cria as colunas iniciais
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product[1]}")  # nome
                st.write(f"**Descrição:** {product[3]}")  # descricao
                try:
                    preco = float(product[2])
                    st.write(f"**Preço:** R$ {preco:.2f}")  # preco
                except (ValueError, TypeError):
                    st.write(f"**Preço:** {product[2]}")  # mostra o valor como está
                if product[4]:  # imagem_url
                    html_img = f'<img src="{product[4]}" width="200" height="200" alt="Imagem do produto">'
                    st.markdown(html_img, unsafe_allow_html=True)
                st.markdown("---")
            # A cada 'cards_por_linha' produtos, se ainda houver produtos, cria novas colunas
        if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
            cols = st.columns(cards_por_linha)
    else:
        st.info


if st.button("Salvar Produto"):
    insert_product(product_name, product_price, product_description, product_image)
    return_message = "Produto salvo com sucesso"
    list_products_screen()

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()
    return_message = "Produtos listados com sucesso"
