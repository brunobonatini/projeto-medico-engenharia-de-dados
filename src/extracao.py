import requests
import boto3
from botocore.client import Config
from conf.settings import settings
import os

GITHUB_URL = settings.github_url
MINIO_ENDPOINT = settings.minio_endpoint
BUCKET_NAME = settings.minio_bucket
BRONZE_DATA = settings.bronze_data

MINIO_ACCESS_KEY = settings.minio_access_key
MINIO_SECRET_KEY = settings.minio_secret_key

# Função de conexão do MiniO via boto3
def conexao_minio_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

# Função para verificar se bucket existe, senão cria
def garantir_bucket(s3):
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
    except ClientError:
        print(f"Criando bucket: {BUCKET_NAME}")
        s3.create_bucket(Bucket=BUCKET_NAME)

# Função para extração dos dados via API
def extrair_dados():
    print("Iniciando extração...")

    response = requests.get(GITHUB_URL, timeout=10)

    if response.status_code != 200:
        raise Exception("Erro ao acessar repositório da API")

    arquivos = response.json()
    s3 = conexao_minio_client()
    garantir_bucket(s3)

    arquivos_enviados = []

    for arquivo in arquivos:
        nome = arquivo["name"]
        download_url = arquivo["download_url"]

        print(f"Baixando {nome}...")

        file_response = requests.get(download_url, timeout=10)

        if file_response.status_code == 200:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{BRONZE_DATA}{nome}",
                Body=file_response.content,
            )
            print(f"Arquivo enviado para Bronze: {nome}")
            arquivos_enviados.append(nome)
        else:
            print(f"Erro ao baixar {nome}")
    
    print("Extração finalizada.")
    return arquivos_enviados
        