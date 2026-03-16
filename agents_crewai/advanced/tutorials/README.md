# Tutorials & Extras

These files are **not required** to run the main advanced agent (`main.py`). They are learning resources and optional extensions.

---

## Files

| File | Purpose | How to run |
|---|---|---|
| `minimal_parallel_tutorial.py` | Learn sequential vs parallel processing with simple examples. No API keys needed. | `python minimal_parallel_tutorial.py` |
| `examples.ipynb` | Interactive notebook demoing individual tools (yfinance, Exa) | Open in VS Code, select `crew_agents_venv` kernel |
| `api_server.py` | FastAPI server that exposes the agents as a REST API | `python start_server.py` (see below) |
| `start_server.py` | Launcher for the API server with environment checks | `python start_server.py` |
| `example_client.py` | Python client that calls the API server endpoints | `python example_client.py` (server must be running) |

---

## Running the API Server

```powershell
# 1. Install extra dependencies
pip install fastapi uvicorn

# 2. Start the server (from the tutorials folder)
python start_server.py

# 3. Open API docs in browser
#    http://localhost:8000/docs

# 4. In a separate terminal, run the example client
python example_client.py
```

---

## Suggested Learning Order

1. `minimal_parallel_tutorial.py` - Understand parallel processing basics
2. `examples.ipynb` - Experiment with individual tools
3. `../main.py` - Run the full multi-agent system
4. `api_server.py` + `example_client.py` - Expose agents as an API
