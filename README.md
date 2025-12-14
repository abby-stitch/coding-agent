# Coding Agent
## 1. Introduction
A multi-agent collaborative system that autonomously completes end-to-end web development workflows (from project planning, data crawling, front-end page generation to result evaluation) based on natural language prompt instructions. The system supports extensible test cases (e.g., arXiv CS Daily Papers， GitHub Trending) and leverages large language models (LLMs) to drive specialized agents for modular, automated development.

## 2. Project Architecture
The system adopts a **modular, pipeline-driven multi-agent architecture** with clear separation of responsibilities and linear data/control flow. It is composed of 4 core layers (Agent Layer, LLM Driver Layer, Configuration Layer, Resource Layer) and follows a "single entry point + sequential execution" design to ensure traceability and scalability.

### 2.1 Core Components & Responsibilities
| Layer               | Component                  | Core Responsibility                                                                 | Input                                  | Output                                      |
|---------------------|----------------------------|-------------------------------------------------------------------------------------|---------------------------------------|---------------------------------------------|
| **Agent Layer**     | Planning Agent (`plan_agent.py`) | Generates scenario-specific project plans (page structure, data requirements).      | `test_cases/[case]/plan_prompt.txt`   | `outputs/project_plan.txt`                  |
|                     | Data Agent (`data_agent.py`)     | Generates data crawling scripts + executes them to output structured JSON data.     | `test_cases/[case]/data_prompt.txt`   | `outputs/generated_data_scraper.py`, `outputs/data.json` |
|                     | HTML Agent (`html_agent.py`)     | Generates 3 types of front-end pages (index/list/detail) based on crawled data.     | `test_cases/[case]/html_*_prompt.txt`, `outputs/data.json` | `outputs/index.html`, `outputs/list.html`, `outputs/detail.html` |
|                     | Evaluation Agent (`evaluation_agent.py`) | Validates data/pages against predefined rules and generates evaluation reports.     | `test_cases/[case]/evaluation_prompt.txt`, all output files | `outputs/evaluation_report.txt` |
| **LLM Driver Layer**| LLM Wrapper (`llm.py`)     | Unifies LLM API calls (Alibaba Cloud Tongyi, compatible with OpenAI) for all agents. | `api_key.txt` (LLM API key)          | LLM responses for agent decision-making     |
| **Configuration Layer** | Config (`config.py`)    | Defines the target test case (e.g., `github_trending`, `arxiv_cs_daily`).            | Manual configuration (user input)     | Selected test case name                     |
| **Execution Layer** | Main Entry (`main.py`)     | Orchestrates the full workflow (triggers agents in sequence).                       | Config info (test case)               | End-to-end execution result                 |
| **Resource Layer**  | Test Cases (`test_cases/`) | Stores scenario-specific prompt files (the "instruction set" for agents).           | N/A                                   | Prompt templates for each test case         |
|                     | Outputs (`outputs/`)       | Centralized storage for all agent outputs (plans, data, pages, reports).             | All agent outputs                     | Structured result files                     |

### 2.2 Workflow & Data Flow
The system follows a **linear pipeline workflow** with no circular dependencies, ensuring predictable execution:
```
1. User configures target test case in config.py 
2. main.py triggers Planning Agent to generate project plan
3. Data Agent generates & executes crawler script to produce structured data (data.json)
4. HTML Agent builds front-end pages using data.json and prompt instructions
5. Evaluation Agent validates all outputs and generates evaluation report
6. All results are saved to the outputs/ folder
```

### 2.3 Key Architectural Features
- **Decoupling**: Each agent operates independently—modifying one agent (e.g., updating Data Agent's crawling logic) does not impact others.
- **Prompt-Driven Extensibility**: Add new scenarios (e.g., "Todo List") by only adding prompt files (no core code changes required).
- **Full Automation**: End-to-end workflow (planning → crawling → development → evaluation) requires minimal human intervention.
- **Traceability**: All outputs are centralized in the `outputs/` folder for easy debugging and audit.

## 3. Setup Instructions
### 3.1 Prerequisites
- Python 3.10 (recommended, developed and tested in a Python 3.10 virtual environment; 3.10+ versions are compatible)
- API key for Alibaba Cloud Tongyi LLM (or OpenAI-compatible LLM)
- Conda (for virtual environment management, optional but recommended)

### 3.2 Environment Setup
```bash
# 1. Create and activate Python 3.10 virtual environment (optional)
conda create -n code-agent python=3.10 -y
conda activate code-agent

# 2. Install core dependencies (create requirements.txt first if missing)
pip install openai==2.8.1 requests>=2.31.0 beautifulsoup4>=4.12.2 lxml>=4.9.0 urllib3>=1.26.16

# 3. Configure LLM API key (create api_key.txt in root directory)
echo "your-alibaba-cloud-tongyi-api-key" > api_key.txt
```

### 3.3 Project Execution
#### Step 1: Select Test Case
Edit `config.py` to specify the target test case:
```python
# config.py
SELECTED_TEST_CASE = "arxiv_cs_daily"  # Options: "github_trending" / "arxiv_cs_daily"
```

#### Step 2: Run the Main Program
```bash
# Execute end-to-end workflow
python main.py
```

#### Step 3: Access Generated Web Pages
```bash
# Navigate to output directory
cd outputs

# Start local HTTP server (port 8080 if 8000 is occupied)
python -m http.server 8000

# Open in browser: http://localhost:8000/index.html
```

### Step 0: Add a New Test Case (Todo List)
```bash
# 1. Create test case folder
mkdir -p test_cases/todo_list

# 2. Add required prompt files (refer to github_trending for format)
touch test_cases/todo_list/{plan_prompt.txt,data_prompt.txt,html_index_prompt.txt,html_list_prompt.txt,html_detail_prompt.txt,evaluation_prompt.txt}

# 3. Update config.py
echo 'SELECTED_TEST_CASE = "todo_list"' > config.py

## 5. Notes
- **Output Overwrite**: The `outputs/` folder is overwritten on each run—rename it (e.g., `outputs_github_trending_20251214`) to back up results.
- **Prompt Consistency**: Ensure prompt files use consistent field names (e.g., `data.json` fields match HTML page references) to avoid `undefined` in pages.
