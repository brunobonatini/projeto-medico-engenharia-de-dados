# Imports das bibliotecas
import requests
import boto3
import os
import logging
import json
from botocore.client import Config
from botocore.exceptions import ClientError
from conf.settings import settings
from datetime import datetime


# Paths
GITHUB_URL = settings.github_url
MINIO_ENDPOINT = settings.minio_endpoint
BUCKET_NAME = settings.minio_bucket
BRONZE_DATA = settings.bronze_data
BRONZE_METADATA = settings.bronze_metadata
MINIO_ACCESS_KEY = settings.minio_access_key
MINIO_SECRET_KEY = settings.minio_secret_key

# Configuração de Log
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

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
    logging.info("Iniciando extração...")
    
    # Partição por data e id de execução
    ingestion_date = datetime.utcnow().strftime("%Y-%m-%d")
    execution_id = datetime.utcnow().strftime("%Y%m%dT%H%M%S")

    arquivos_enviados = []
    status = "success"
    error_message = None
    
    try:
    
        response = requests.get(GITHUB_URL, timeout=10)
    
        if response.status_code != 200:
            raise Exception("Erro ao acessar a API.")

        arquivos = response.json()
        s3 = conexao_minio_client()
        garantir_bucket(s3)

        # Loop para ingestão dos arquivos
        for arquivo in arquivos:
            nome = arquivo["name"]
            download_url = arquivo["download_url"]

            chave = (
                f"{BRONZE_DATA}raw/"
                f"ingestion_date={ingestion_date}/"
                f"execution_id={execution_id}/"
                f"{nome}"
            )

            logging.info(f"Processando {nome}...")

            file_response = requests.get(download_url, timeout=10)

            # Verificar se o retorno é OK
            if file_response.status_code == 200:
                s3.put_object(
                    Bucket=BUCKET_NAME,
                    Key=chave,
                    Body=file_response.content,
                )
                arquivos_enviados.append(nome)
            else:
                logging.warning(f"Erro ao baixar {nome}")

        logging.info(f"{len(arquivos_enviados)} arquivos enviados")

    except Exception as e:
        status = "failed"
        error_message = str(e)
        
        logging.error(f"Falha na execução: {error_message}")
                      
    finally:
    
        # Metadados por execução na camada Bronze (Governaça de dados)
        metadata = {
            "execution_id": execution_id,
            "pipeline": "github_ingestion",
            "source": "github_api",
            "ingestion_date": ingestion_date,
            "execution_timestamp": datetime.utcnow().isoformat(),
            "total_files": len(arquivos_enviados),
            "status": status,
            "error_message": error_message
        }
    
        metadata_key = f"{BRONZE_METADATA}execution_id={execution_id}/metadata.json"
                      
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=metadata_key,
            Body=json.dumps(metadata, indent=4),
            ContentType="application/json"
        )
                      
        logging.info("Metadata da execução salvo")
    
    return arquivos_enviados