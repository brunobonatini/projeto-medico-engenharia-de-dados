FROM apache/spark:3.5.3

USER root

RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Jupyter
RUN pip install --no-cache-dir notebook==6.5.6

COPY requirements-notebook.txt .
RUN pip install --no-cache-dir -r requirements-notebook.txt

WORKDIR /projeto

EXPOSE 8888

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token="]
