<img width="1200" height="675" alt="roadmaster-visualisation" src="https://github.com/user-attachments/assets/5147f5b7-7e26-474e-a274-cdf36aa54128" />


# Railway Operations System

A comprehensive system for ingesting timetables and SOPs, detecting delays, suggesting recovery moves, and providing SOP-grounded Q&A for railway operations.
Railway Operations (irailops) is an opinionated, open-source system for ingesting timetables and SOPs, simulating/recording train events, detecting delays, recommending recovery moves, and providing SOP-grounded Q&A via a RAG-backed assistant. It includes:

- A FastAPI backend exposing ingestion, events, reasoning and RAG endpoints
- A Streamlit-based operator UI (`src/ui/app.py`) for dashboards and Ops Copilot
- A standalone browser-based Track Visualizer (`track-visualizer/`) that animates delayed trains
- Utilities to seed sample data, generate synthetic scenarios, and run locally or via Docker

## Highlights

- Works with local, open-source LLMs (Ollama, HuggingFace) or a template fallback
- Vector store support: `pgvector` (default) or `qdrant`
- Minimal demo flow: ingest sample data → start API → open Streamlit UI → view visualizer

## Quick Start (Local)

1. Create a Python virtualenv and activate it:

```bash
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows (cmd / PowerShell)
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. (Optional) Prepare local LLMs / embeddings (if you plan to use RAG):

```bash
python setup_models.py
```

4. Initialize the database and seed sample data:

```bash
python -m src.cli setup-db
python -m src.cli ingest-sample
```

5. Start the backend API (default port 8000):

```bash
python -m src.cli start-api
# or
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

6. Start the Streamlit UI (it will try to autodetect the API URL):

```bash
streamlit run src/ui/app.py
# or use the CLI helper which sets API_BASE_URL for you
python -m src.cli start-ui
```

7. (Optional) Run the Track Visualizer (standalone static page):

```bash
cd track-visualizer
python -m http.server 9000
# or
npx serve . -l 9000
# Open: http://localhost:9000/track-visualizer/index.html
# Set API URL top-left to http://localhost:8000 and click Save → Refresh
```

## Docker (optional)

The `docker-compose.yml` brings up Postgres, Neo4j, Qdrant and the API service. To run the full stack:

```bash
docker compose up --build
```

Environment variables and service URLs are configured in `docker-compose.yml` and can be overridden via `.env` or your shell.

## Useful Commands

- Setup DB: `python -m src.cli setup-db`
- Ingest sample data: `python -m src.cli ingest-sample`
- Start API: `python -m src.cli start-api`
- Start UI: `python -m src.cli start-ui`
- Ingest SOPs from `data/sops`: POST `/api/admin/ingest/sop-from-dir` (admin endpoint)

## Track Visualizer

The visualizer is a static HTML/JS app in `track-visualizer/`. It only needs the `/api/events/delayed` endpoint. Notes:

- Serve the folder with a static server (browser blocks file:// fetch)
- The page simulates positions on a schematic network and colors segments based on occupancy
- Use the top-left control to set your API URL (include `http://`), then click Save and Refresh

## Development notes

- Configuration: `src/config.py` (pydantic settings, `.env` supported)
- CLI helpers: `src/cli.py` for setup, ingest and starting services
- API routes: `src/api/main.py`
- Streamlit UI: `src/ui/app.py`
