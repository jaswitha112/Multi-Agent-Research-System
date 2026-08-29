# Multi-Agent Research System

An open-source research assistant that combines specialized LangChain agents with web search and content extraction. Given a topic, it finds relevant sources, reads a selected source, drafts a structured report, and reviews the report with an AI critic.

The project provides both a Streamlit interface for interactive research and a Python entry point for scripted runs.


## Features

- Search the web with Tavily and collect titles, URLs, and snippets.
- Select and scrape a relevant source with a dedicated reader agent.
- Generate a structured report with an OpenRouter chat model.
- Review the report for factual quality, completeness, clarity, consistency, and source quality.
- Display progress, research output, the final report, and critic feedback in Streamlit.

## Architecture

The application uses a sequential four-stage pipeline. `run_research_pipeline` coordinates the workflow and stores each stage in a shared state dictionary.

```text
User topic
    |
    v
Search agent -- web_search --> Tavily results
    |
    v
Reader agent -- scrape_url --> Extracted source content
    |
    v
Writer chain -- OpenRouter --> Structured research report
    |
    v
Critic chain -- OpenRouter --> Score, strengths, and improvements
```

Agent Responsibilities

- Search Agent: Discovers relevant information across the web using Tavily

- Reader Agent: Extracts clean, readable content from URLs

- Writer Chain: Composes structured, professional research reports

- Critic Chain: Evaluates reports and provides improvement suggestions


### Project structure

```text
.
├── app.py                    # Streamlit interface
├── main.py                   # Scripted pipeline example
├── requirements.txt          # Python dependencies
└── src/
    ├── agents/agents.py      # Agents, prompts, and LangChain chains
    ├── pipelines/pipeline.py # End-to-end workflow orchestration
    └── tools/tools.py        # Tavily search and URL scraping tools
```

## Technology stack

- **Python 3.10+** - Application runtime
- **LangChain** - Agent creation, prompts, tools, and output parsing
- **OpenRouter** - Chat model access through `langchain-openrouter`
- **Streamlit** - Interactive web interface
- **Tavily** - Web search API
- **Requests** - HTTP requests for source pages
- **Trafilatura, Readability, Beautiful Soup** - HTML content extraction and cleanup
- **python-dotenv** - Loading local environment variables from `.env`
- **Rich** - Optional terminal logging and formatting support

## Requirements

- Python 3.10 or newer
- An [OpenRouter](https://openrouter.ai/) API key
- A [Tavily](https://tavily.com/) API key
- Internet access for search and source retrieval

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd LangChain-Multi-Agent-Research-System
   ```

2. Create and activate a virtual environment.

   **Windows PowerShell:**

   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:

   ```env
   OPENROUTER_API_KEY=your_openrouter_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Keep this file private and never commit API keys to source control.

## Usage

### Streamlit application

Start the interactive application:

```bash
streamlit run app.py
```

Streamlit will print a local URL. Open it in your browser, enter a research topic, and run the pipeline.

### Python pipeline

Run the example topic in `main.py`:

```bash
python main.py
```

Use the pipeline from another Python module:

```python
from src.pipelines.pipeline import run_research_pipeline

result = run_research_pipeline("The impact of AI on the job market in 2026")
print(result["report"])
print(result["feedback"])
```

## Configuration

The default OpenRouter model is configured in `src/agents/agents.py`:

```python
ChatOpenRouter(model="openrouter/free", temperature=0)
```

To use a different OpenRouter-supported model, update the `model` value and confirm that the model is available to your account.

## Limitations

- Search and scraping require network access and valid API keys.
- Tavily and OpenRouter usage may be subject to account limits or costs.
- Some websites block automated requests or do not expose content that can be extracted reliably.
- Generated reports can contain errors and should be checked against the linked sources before being used for important decisions.

## Contributing

Contributions are welcome. To contribute:

1. Open an issue for bugs, questions, or larger proposals.
2. Create a focused branch for your change.
3. Keep secrets out of commits and document any new configuration.
4. Test the Streamlit app or Python pipeline locally and describe the checks in your pull request.

## License

This project is distributed under the terms of the [MIT License](LICENSE).
