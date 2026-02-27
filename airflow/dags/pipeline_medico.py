from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

import requests
import os

def extracao_git():

    # Destino dos arquivos dentro do container
    destino_path = "/opt/airflow/script/extracao_api_git.py"

    # Verificar se a pasta existe, caso contrário, criar a pasta
    if not os.path.exists(destino_path):
        os.makedirs(destino_path)

    # URL da API para listar o conteúdo do diretório 'data'
    repositorio_url = 'https://api.github.com/repos/wandersondsm/teste_engenheiro/contents/data'

    response = requests.get(repositorio_url)

    # Condição que verifica se existe arquivos no diretório
    if response.status_code == 200:
        # Listar todos os arquivos no diretório
        arquivos = response.json()
        
        # Loop para obter a URL de todos os arquivos row para cada arquivo
        for arquivo in arquivos:
            arquivo_url = arquivo['download_url']
            
            # Download do arquivo
            arquivo_response = requests.get(arquivo_url)
            
            if arquivo_response.status_code == 200:
                # Definir o caminho completo para salvar o arquivo na pasta 'data' dentro do container
                arquivo_path = os.path.join(destino_path, arquivo['name'])
                
                # Salvar o arquivo na pasta
                with open(arquivo_path, 'wb') as dados:
                    dados.write(arquivo_response.content)
                print(f"Arquivo {arquivo['name']} baixado com sucesso em {arquivo_path}!")
            else:
                print(f"Erro ao baixar {arquivo['name']}")
    else:
        print("Erro ao acessar o diretório no GitHub.")


# Definição da DAG
default_args = {
    "owner": "bruno",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 16),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="executa_script_python",
    default_args=default_args,
    description="Executa um script Python localizado na pasta script",
    schedule_interval=None,
    catchup=False,
    max_active_runs=1,
) as dag_executa_script_python:

# Task para executar o script python
    t_01_executa_script_python = PythonOperator(
        task_id="t_01_executa_script_python",
        python_callable=extracao_git,
    )

    t_01_executa_script_python