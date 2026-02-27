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
def get_minio_client():
    return boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

# Função para extração dos dados via API
def extrair_dados():
    response = requests.get(GITHUB_URL)

    if response.status_code != 200:
        raise Exception("Erro ao acessar repositório GitHub")

    arquivos = response.json()
    s3 = get_minio_client()

    for arquivo in arquivos:
        nome = arquivo["name"]
        download_url = arquivo["download_url"]

        file_response = requests.get(download_url)

        if file_response.status_code == 200:
            s3.put_object(
                Bucket=BUCKET_NAME,
                Key=f"{BRONZE_DATA}{nome}",
                Body=file_response.content,
            )
            print(f"Arquivo enviado para MinIO: {nome}")
        else:
            print(f"Erro ao baixar {nome}")
        