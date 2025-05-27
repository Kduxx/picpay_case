FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y curl build-essential && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root

FROM python:3.11-slim AS api

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY picpay_case ./picpay_case
COPY pyproject.toml ./

EXPOSE 8000

CMD ["uvicorn", "picpay_case.main:app", "--host", "0.0.0.0", "--port", "8000"]
