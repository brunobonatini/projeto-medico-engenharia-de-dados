from pydantic_settings import BaseSettings

# Classe de configuração e definição das variáveis de ambiente e paths
class Settings(BaseSettings):
    
    # Fonte de dados
    github_url: str
    # MiniO
    minio_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str

    # Paths
    bronze_data: str
    silver_data: str
    gold_data: str

    class Config:
        env_file = '.env'

settings = Settings()