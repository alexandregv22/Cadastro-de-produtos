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
                st.write(f"**Descrição:** {product[2]}")  # descricao
                try:
                    preco = float(product[3])
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

def delete_all_products():
    try:
        conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USER};PWD={SQL_PASSWORD}")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Produtos")
        conn.commit()
        conn.close()
        st.success("Todos os produtos foram excluídos!")
    except Exception as e:
        st.error(f"Erro ao excluir todos os produtos: {e}")

if st.button("Limpar lista de produtos"):
    delete_all_products()
    list_products_screen()

def delete_product_by_field(nome=None, descricao=None, preco=None):
    try:
        conn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SQL_SERVER};DATABASE={SQL_DATABASE};UID={SQL_USER};PWD={SQL_PASSWORD}")
        cursor = conn.cursor()
        conditions = []
        params = []
        if nome:
            conditions.append("nome = ?")
            params.append(nome)
        if descricao:
            conditions.append("descricao = ?")
            params.append(descricao)
        if preco is not None:
            # Tolerância de 1 centavo para comparação de float
            conditions.append("ABS(preco - ?) < 0.01")
            params.append(preco)
        if not conditions:
            st.warning("Preencha pelo menos um campo para excluir um produto.")
            return
        where_clause = " AND ".join(conditions)
        sql = f"DELETE FROM Produtos WHERE {where_clause}"
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
        st.success("Produto(s) excluído(s) com sucesso!")
    except Exception as e:
        st.error(f"Erro ao excluir produto(s): {e}")

with st.form("delete_product_form"):
    del_nome = st.text_input("Nome do produto para excluir (opcional)")
    del_descricao = st.text_input("Descrição do produto para excluir (opcional)")
    del_preco = st.text_input("Preço do produto para excluir (opcional)")
    submitted = st.form_submit_button("Excluir Produto")
    if submitted:
        preco_val = None
        if del_preco:
            preco_str = del_preco.replace(",", ".")  # Permite vírgula ou ponto
            try:
                preco_val = float(del_preco)
            except ValueError:
                st.warning("Preço inválido, digite um número ou deixe em branco.")
        delete_product_by_field(
            nome=del_nome if del_nome else None,
            descricao=del_descricao if del_descricao else None,
            preco=preco_val
        )
