# Usar a imagem do LaTeX como base
FROM texlive/texlive:latest

# Evitar prompts interativos durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python e dependências necessárias
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash && rm -rf /var/lib/apt/lists/*

# Criar diretório da aplicação
WORKDIR /app

# Criar e ativar ambiente virtual
ENV VIRTUAL_ENV=/app/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copiar os requisitos e instalar dependências
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Criar diretório temp com permissões adequadas
RUN mkdir -p temp && chmod 777 temp

# Comando para executar a aplicação com Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
