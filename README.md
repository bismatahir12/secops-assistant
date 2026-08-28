# SecOps Assistant

An AI-powered IT/Security Operations Assistant — small SaaS-style platform.
Users connect a (simulated) system, an AI agent investigates alerts using
real tool-calling (threat-intel lookup, log parsing), answers questions over
uploaded security docs via RAG, and produces reports, backed by a real
dashboard.


## Stack

- FastAPI (async) + SQLAlchemy 2.0 (async) + PostgreSQL
- JWT auth (OAuth2 password flow)
- Docker Compose
- pytest 

## Run it

```bash
cp backend/.env.example backend/.env
python -c "import secrets; print(secrets.token_hex(32))"

docker compose up --build
```

API will be live at http://localhost:8000, interactive docs at
http://localhost:8000/docs. Try it there: `POST /auth/signup`, then use the
"Authorize" button with your credentials, then `POST /systems`.

## Run tests locally (no Docker needed — uses in-memory SQLite)

```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v
```

Expected: 6 passing tests covering signup, duplicate-email rejection, login
success/failure, and `/auth/me` token validation.

## Project layout

```
backend/
  app/
    core/        # config, db session, JWT/password helpers, auth dependency
    models/      # SQLAlchemy models (User, System)
    schemas/     # Pydantic request/response models
    routers/     # auth.py, systems.py
    main.py      # app wiring, CORS, table creation on startup
  tests/         # pytest, in-memory SQLite fixtures
docker-compose.yml
```
## Notes on scope

"Connecting a system" registers a source record — it does not perform a live
integration. Alert ingestion is simulated via a seed script and a webhook
endpoint. This is a deliberate scoping decision, not an unfinished feature —
see the project writeup for reasoning.
