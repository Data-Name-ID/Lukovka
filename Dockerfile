FROM python:3.12-alpine AS builder

WORKDIR /project
RUN pip install --no-cache-dir poetry && poetry config virtualenvs.in-project true

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --without dev --no-interaction --no-ansi --no-root


FROM python:3.12-alpine

WORKDIR /project
ENV VENV_BIN_PATH=/project/.venv/bin

RUN apk add --no-cache openssl
RUN mkdir -p ./certs
RUN openssl genrsa -out ./certs/jwt-private.pem 2048
RUN openssl rsa -in ./certs/jwt-private.pem -outform PEM -pubout -out ./certs/jwt-public.pem

COPY --from=builder /project/.venv/ ./.venv/
COPY ./app/ .

CMD ${VENV_BIN_PATH}/alembic upgrade head && ${VENV_BIN_PATH}/uvicorn main:app --host 0.0.0.0 --port ${BACKEND__RUN__PORT}
