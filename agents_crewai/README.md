# CrewAI Agents

Multi-agent systems built with [CrewAI](https://docs.crewai.com/) — from single-agent to parallel multi-agent architectures.

---

## 1. Prerequisites

- **Python 3.11 or 3.12** (3.13+ may have compatibility issues with numpy/other packages)
- **VS Code** with the Python extension installed
- An **OpenRouter API key** ([get one here](https://openrouter.ai/keys))
- An **Exa API key** (needed for intermediate & advanced agents) ([get one here](https://exa.ai))

---

## 2. Project Structure

```
crewai_agents/
├── .env                          # API keys (never commit this)
├── .gitignore
├── crew_agents_venv/             # Python virtual environment
│
└── agents/
    ├── beginner/                 # Single-agent system
    │   ├── agents.py             # Agent definition + LLM config
    │   ├── tasks.py              # Task definition
    │   ├── main.py               # Entry point
    │   └── examples.ipynb        # Example agents (notebook)
    │
    ├── intermediate/             # Sequential multi-agent system
    │   ├── agents.py             # 4 agents: Log Analyzer, Issue Investigator, Solution Specialist, Code Fix Generator
    │   ├── tasks.py              # 4 sequential tasks with context passing
    │   ├── tools.py              # FileReadTool + EXASearchTool
    │   ├── main.py               # Entry point
    │   └── examples.ipynb        # Tool examples (notebook)
    │
    ├── advanced/                 # Parallel multi-agent system
    │   ├── agents.py             # 4 agents: News Explorer, Data Explorer, Analyst, Financial Expert
    │   ├── tasks.py              # 4 tasks (2 parallel + 2 sequential)
    │   ├── tools.py              # Custom tools (yfinance) + EXASearchTool
    │   ├── main.py               # Entry point with ThreadPoolExecutor
    │   └── tutorials/            # Learning resources & API server (see tutorials/README.md)
    │
    └── dummy_logs/               # Sample log files for intermediate agent
```

---

## 3. Environment Setup

### 3.1 Create Virtual Environment

```powershell
# If Python 3.11 is not on PATH, use the full path:
& "C:\Path\To\Python311\python.exe" -m venv crew_agents_venv

# Activate the venv
.\crew_agents_venv\Scripts\Activate.ps1
```

> **Bash/macOS/Linux:**
> ```bash
> python3.11 -m venv crew_agents_venv
> source crew_agents_venv/bin/activate
> ```

### 3.2 Install Dependencies

```powershell
pip install crewai crewai-tools python-dotenv

# Required for intermediate and advanced agents (Exa search):
pip install exa_py

# Additional packages for advanced agent (stock analysis):
pip install yfinance curl_cffi
```

### 3.3 Configure `.env` File

Create a `.env` file in the project root (`crewai_agents/.env`):

```env
# Required for all agents (LLM via OpenRouter)
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here

# Required for intermediate and advanced agents (Exa web search)
EXA_API_KEY=your-exa-api-key-here
```

> **Note:** CrewAI itself does not require an API key. The keys above are for the LLM provider (OpenRouter) and search tool (Exa).

> **Using CrewAI's default LLM:** If you don't specify `llm=` on an agent (like in the beginner `examples.ipynb`), CrewAI defaults to OpenAI's `gpt-4o`. In that case, you need an `OPENAI_API_KEY` instead:
> ```env
> OPENAI_API_KEY=sk-your-openai-api-key-here
> ```
> You do **not** need both — use `OPENROUTER_API_KEY` if you explicitly pass `llm=` with OpenRouter config, or `OPENAI_API_KEY` if you want CrewAI's default.

### 3.4 VS Code Kernel Setup (for notebooks)

1. Open any `.ipynb` file in VS Code
2. Click the kernel picker (top-right)
3. Select **crew_agents_venv** as the kernel
4. Restart the kernel if you change it

---

## 4. Running the Agents

Make sure the venv is activated before running any agent.

### 4.1 Beginner - Hate Speech Detector (Single Agent)

```
agents/beginner/
├── agents.py    →  1 agent (Hate Speech Detector)
├── tasks.py     →  1 task (classify text)
└── main.py      →  Entry point
```

**How it works:**
- A single agent receives text input and classifies it as hate speech or not.
- Uses OpenRouter (`openai/gpt-4o`) as the LLM.

```powershell
cd agents/beginner
python main.py
```

---

### 4.2 Intermediate - DevOps Log Analyzer (Sequential Multi-Agent)

```
agents/intermediate/
├── agents.py    →  4 agents with system_template and parameters
├── tasks.py     →  4 tasks with context passing
├── tools.py     →  FileReadTool + EXASearchTool
└── main.py      →  Entry point
```

**Agent Flow (Sequential):**

```
┌──────────────────┐     ┌────────────────────────┐     ┌───────────────────────┐     ┌───────────────────────┐
│  Log Analyzer    │────>│  Issue Investigator    │────>│  Solution Specialist  │────>│  Code Fix Generator   │
│                  │     │                        │     │                       │     │                       │
│  - Reads log file│     │  - Takes analysis as   │     │  - Takes analysis +   │     │  - Takes all previous │
│  - Identifies    │     │    context             │     │    investigation as   │     │    tasks as context   │
│    errors        │     │  - Searches online via │     │    context            │     │  - Generates code     │
│  - Root cause    │     │    Exa for solutions   │     │  - Step-by-step fix   │     │    patches & configs  │
│    analysis      │     │  - Finds documentation │     │  - Rollback plan      │     │  - Validation scripts │
└──────────────────┘     └────────────────────────┘     └───────────────────────┘     └───────────────────────┘
```

**Key Concepts:**
- **Context passing:** Each task receives the output of previous tasks via `context=[previous_task]`
- **System template:** Custom system prompt defining the agent's expertise
- **Tools:** `FileReadTool` reads log files, `EXASearchTool` searches the web
- **Parameters:** `max_iter`, `max_rpm`, `max_execution_time`, `respect_context_window`

**Requirements:** `OPENROUTER_API_KEY` + `EXA_API_KEY`

```powershell
cd agents/intermediate
python main.py
```

Output is saved to `agents/intermediate/task_outputs/`.

---

### 4.3 Advanced - Investment Advisor (Parallel Multi-Agent)

```
agents/advanced/
├── agents.py    →  4 agents
├── tasks.py     →  4 tasks (2 parallel + 2 sequential)
├── tools.py     →  Custom tools (@tool decorator) + EXASearchTool
└── main.py      →  Entry point with parallel execution
```

**Agent Flow (Parallel + Sequential):**

```
Phase 1 (Parallel):
┌──────────────────────┐
│  Data Explorer       │──┐
│  - get_company_info  │  │
│  - get_income_stmts  │  │
└──────────────────────┘  │
                          ├──> Phase 2 (Sequential):
┌──────────────────────┐  │    ┌──────────────┐     ┌──────────────┐
│  News Explorer       │──┘    │  Analyst     │────>│  Fin Expert  │
│  - Exa web search    │       │  - Combines  │     │  - Buy/Hold/ │
└──────────────────────┘       │    all data  │     │    Sell rec  │
                               └──────────────┘     └──────────────┘
```

**Key Concepts:**
- **Parallel execution:** `ThreadPoolExecutor` runs financial data + news gathering simultaneously
- **Custom tools:** Built with `@tool` decorator wrapping `yfinance` API calls
- **Multiple crews:** Separate `Crew` objects for parallel vs sequential phases

**Requirements:** `OPENROUTER_API_KEY` + `EXA_API_KEY`

```powershell
cd agents/advanced
python main.py                        # Default: analyzes RELIANCE stock
python main.py --stock INFY           # Analyze a specific stock
```

Output is saved to `agents/advanced/task_outputs/`.

---

## 5. How `.env` Loading Works

Each agent folder loads the `.env` file using `python-dotenv`:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env from the current working directory
```

**Important:** `load_dotenv()` looks for `.env` in the **current working directory**, not the script's directory. Always `cd` into the agent folder before running, or the `.env` in the project root won't be found if you run from a subfolder.

If running from the project root:
```powershell
# This won't work (load_dotenv looks in agents/beginner/ for .env):
python agents/beginner/main.py

# This works (load_dotenv finds .env in current dir):
cd agents/beginner
python main.py
```

---

## 6. Troubleshooting

| Problem | Solution |
|---|---|
| `numpy` build fails | Use Python 3.11 or 3.12, not 3.13+ |
| `OPENAI_API_KEY is required` | You're using OpenRouter — make sure `llm=` is set on every agent |
| `.env` not loading | Run from the correct directory (see Section 5) |
| `EXA_API_KEY` error | Add your Exa key to `.env` (needed for intermediate/advanced) |
| Kernel not found in VS Code | Install `ipykernel`: `pip install ipykernel` |
| `No module named 'exa_py'` | Run `pip install exa_py` manually |
| Rate limiting errors | Reduce `max_rpm` values in agent definitions |
