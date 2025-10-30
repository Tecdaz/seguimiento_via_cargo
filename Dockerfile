# Stage 1: Builder
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Instalar dependencias de build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

COPY pyproject.toml ./
RUN uv pip install -e . --system

# Stage 2: Runtime
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copiar solo lo necesario del builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Instalar solo las dependencias mínimas para chromium headless
RUN playwright install chromium && \
    playwright install-deps chromium && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python3", "main.py"]