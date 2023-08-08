FROM python:3.11-slim

WORKDIR /app

RUN pip3 install poetry
COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root

COPY . .

CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1
