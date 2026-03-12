# Projeto em construção...

# Projeto Médico – Engenharia de Dados (Arquitetura Lakehouse)

Este projeto implementa uma arquitetura completa de dados baseada no conceito de Lakehouse, simulando um ambiente real de produção. A solução foi construída com containers Docker e integra orquestração, processamento distribuído, armazenamento em Data Lake, catálogo centralizado, modelagem analítica e visualização.

O objetivo é reproduzir, localmente, padrões utilizados por empresas data-driven que precisam de pipelines escaláveis, reprocessáveis, auditáveis e desacoplados.

---

## Visão Geral da Arquitetura

A arquitetura foi desenhada separando claramente responsabilidades entre orquestração, processamento, armazenamento e consumo analítico. Cada componente foi escolhido para representar soluções amplamente utilizadas em ambientes corporativos.

O fluxo geral funciona da seguinte forma:

1. O Airflow orquestra a execução do pipeline.
2. Dados são extraídos de uma fonte externa via API e armazenados no Data Lake (MinIO).
3. O Spark processa e transforma os dados em formato Delta Lake.
4. As tabelas são registradas no catalogo Hive Metastore.
5. O Trino consulta os dados diretamente do Data Lake.
6. O dbt realiza modelagem analítica (camada Gold).
7. O Metabase consome os dados para visualização.

---

## Apache Airflow – Orquestração

O Airflow é responsável por coordenar todo o fluxo de dados. Ele gerencia dependências entre tarefas, agenda execuções e permite monitoramento centralizado dos pipelines.

Foi configurado com Celery Executor e Redis para simular um ambiente distribuído, onde múltiplos workers executam tarefas paralelamente. Essa escolha reflete arquiteturas reais em produção, onde escalabilidade e confiabilidade são essenciais.

O PostgreSQL é utilizado como banco de metadados do Airflow, garantindo persistência do estado das DAGs e histórico de execuções.

O Airflow também possui cliente Spark instalado, permitindo submissão de jobs diretamente para o cluster Spark.

---

## Apache Spark 3.5 – Processamento Distribuído

O Spark é o motor de processamento da arquitetura. Ele executa transformações distribuídas sobre grandes volumes de dados e escreve resultados em formato Delta Lake.

Foi configurado como cluster Standalone (master + worker), refletindo uma topologia real de processamento paralelo.

A escolha do Spark se deve à sua capacidade de:

- Processar dados em larga escala
- Integrar-se facilmente com Data Lakes
- Trabalhar com Delta Lake para garantir transações ACID
- Permitir reprocessamento eficiente

O Spark foi integrado ao MinIO via protocolo S3A e ao Hive Metastore para registro das tabelas.

---

## MinIO – Data Lake (Compatibilidade com AWS S3)

O MinIO atua como armazenamento principal do projeto, simulando um Data Lake em ambiente cloud. Ele é compatível com a API S3, o que permite replicar arquiteturas baseadas em Amazon S3 localmente.

Os dados são organizados nas camadas Bronze, Silver e Gold, permitindo separação entre dados brutos, tratados e analíticos.

A escolha do MinIO permite que a arquitetura seja facilmente migrada para ambientes como AWS S3, Google Cloud Storage ou Azure Data Lake, mantendo a mesma lógica estrutural.

---

## Delta Lake – Camada Transacional

O Delta Lake foi incorporado ao Spark para transformar o Data Lake em uma estrutura transacional.

Ele fornece:

- Transações ACID
- Controle de versão de dados
- Evolução de schema
- Operações de merge e upsert
- Garantia de consistência

Sem Delta Lake, o Data Lake seria apenas um repositório de arquivos. Com Delta, ele se torna confiável para workloads analíticos e pipelines incrementais.

---

## Hive Metastore – Catálogo Centralizado

O Hive Metastore atua como catálogo de metadados, armazenando informações sobre bancos, tabelas e schemas.

Sua presença permite que múltiplos engines (Spark e Trino) compartilhem as mesmas definições de tabelas.

Essa camada é essencial para simular ambientes corporativos que utilizam catálogos centralizados como AWS Glue Catalog.

---

## Trino – Query Engine Distribuída

O Trino foi adicionado como engine SQL para consulta interativa diretamente no Data Lake.

Ele permite acesso rápido e distribuído às tabelas registradas no Hive Metastore, desacoplando o consumo do processamento.

Isso simula cenários onde múltiplas equipes consomem dados sem depender diretamente do cluster Spark.

---

## dbt – Modelagem Analítica

O dbt é utilizado como camada de transformação orientada a SQL. Ele atua sobre o Trino e organiza modelos analíticos na camada Gold.

Essa separação permite que:

- Spark realize processamento pesado e estruturante
- dbt cuide da modelagem analítica e métricas

Essa abordagem é comum em arquiteturas modernas que separam engenharia de dados de analytics engineering.

---

## Metabase – Visualização

O Metabase foi incluído para simular a camada final de consumo. Ele se conecta ao Trino e permite criação de dashboards e análises exploratórias.

Isso fecha o ciclo completo da arquitetura: ingestão, processamento, modelagem e consumo.

---

## Estrutura e Isolamento de Ambientes

Cada serviço roda em seu próprio container, com dependências isoladas. O Spark utiliza Python 3.8 (compatível com sua imagem oficial), enquanto o Airflow roda com Python 3.12. Essa separação evita conflitos de bibliotecas e reflete boas práticas de engenharia.

A infraestrutura é totalmente reproduzível via Docker Compose.

---

## Aplicação em Ambiente Real

Essa arquitetura pode ser adaptada diretamente para cloud substituindo os componentes locais por serviços gerenciados:

- Airflow → MWAA ou Cloud Composer
- Spark → EMR, Dataproc ou Databricks
- MinIO → S3 ou GCS
- Hive Metastore → Glue Catalog
- Trino → Athena ou Starburst
- dbt → dbt Cloud
- Metabase → Power BI ou Looker

A lógica arquitetural permanece a mesma, mudando apenas o provedor da infraestrutura.

---

## Conclusão

Este projeto demonstra a construção de uma plataforma de dados moderna baseada em Lakehouse, com separação clara entre orquestração, processamento, armazenamento, catálogo, modelagem e consumo.

Ele simula padrões utilizados por empresas que precisam de pipelines escaláveis, auditáveis e preparados para ambientes distribuídos.

A arquitetura foi pensada para refletir práticas reais de Engenharia de Dados e permitir evolução futura para ambientes cloud.
