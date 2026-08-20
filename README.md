# LangChain Multi-Agent Research System

An open-source research assistant that uses specialized LangChain agents to search the web, extract useful source content, write a structured report, and review the result with an AI critic.

The project includes a Streamlit interface for interactive research and a Python pipeline entry point for scripted runs.

## Features

- Web search with Tavily, returning recent sources, URLs, and snippets.
- Dedicated reader agent that selects and scrapes a relevant source.
- Local LLM inference through Ollama.
- Structured report generation with sources, key findings, and a conclusion.
- Critic pass that scores the report and identifies strengths and improvements.
- Streamlit UI with progress states, raw research output, report download, and critic feedback.

## Architecture

The research workflow is a sequential pipeline:

```text
User topic
	|
	v
Search Agent -- Tavily web search --> Search results
	|
	v
Reader Agent -- requests + content extraction --> Scraped content
	|
	v
Writer chain -- Ollama LLM --> Research report
	|
	v
Critic chain -- Ollama LLM --> Score and feedback
```

### Project layout

```text
.
├── app.py                    # Streamlit application
├── main.py                   # Scripted pipeline example
├── requirements.txt          # Python dependencies
└── src/
	├── agents/agents.py      # Agents, prompts, and LangChain chains
	├── pipelines/pipeline.py # End-to-end research orchestration
	└── tools/tools.py        # Tavily search and URL scraping tools
```

## Technologies

- **Python** - Application runtime
- **Streamlit** - Interactive web interface
- **LangChain** - Agent and prompt orchestration
- **Ollama** - Local model serving
- **Qwen 2.5 3B** - Default local model (`qwen2.5:3b`)
- **Tavily** - Web search API
- **Requests, Trafilatura, Readability, Beautiful Soup** - Fetching and extracting readable web content
- **python-dotenv** - Environment variable loading
- **Rich** - Terminal output formatting

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/download) installed and running
- A Tavily API key

## Installation

1. Clone the repository and enter the project directory:

   ```bash
   git clone <repository-url>
   cd LangChain-Multi-Agent-Research-System
   ```

2. Create and activate a virtual environment:

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

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   pip install langchain-ollama
   ```

4. Download the default Ollama model:

   ```bash
   ollama pull qwen2.5:3b
   ```

5. Create a `.env` file in the project root:

   ```env
   TAVILY_API_KEY=your_tavily_api_key
   ```

   Get a key from [Tavily](https://tavily.com/). Keep `.env` private and do not commit it.

## Usage

### Streamlit application

Start the interactive research assistant with:

```bash
streamlit run app.py
```

Then enter a research topic in the browser and run the pipeline.

### Python pipeline

Run the example topic from `main.py` with:

```bash
python main.py
```

For custom integrations, import `run_research_pipeline`:

```python
from src.pipelines.pipeline import run_research_pipeline

result = run_research_pipeline("The impact of AI on the job market in 2026")
print(result["report"])
print(result["feedback"])
```

## Configuration

The default model is configured in `src/agents/agents.py`:

```python
ChatOllama(model="qwen2.5:3b", temperature=0)
```

Change the model name there after pulling the corresponding model with Ollama.

## Notes and limitations

- Search and scraping require network access.
- Tavily usage is subject to the limits of your Tavily account.
- Some websites may block automated requests or return content that cannot be cleanly extracted.
- Generated reports should be checked against the linked sources before being used for important decisions.

## Contributing

Contributions are welcome. Please open an issue to discuss a significant change before submitting a pull request. Keep changes focused, document new configuration, and include a clear description of how the change was tested.

## License

This project is distributed under the terms of the [MIT License](LICENSE).