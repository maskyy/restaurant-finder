# Build the frontend first
FROM node:latest AS frontend

WORKDIR /app/client

COPY client/package*.json .

RUN npm install

COPY client .

RUN npm run build

# Then acquire the dist folder and build the backend
FROM python:slim AS backend

WORKDIR /app/server

RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libpq-dev build-essential
RUN rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY pyproject.toml poetry.lock .

RUN poetry install --only main --no-root

COPY restaurant-finder .

COPY --from=frontend /app/client/dist /app/client/dist

CMD ["python", "-m", "restaurant-finder.main"]
