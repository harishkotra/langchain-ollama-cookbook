# LangChain + Ollama Demos

This project will contain 5 independent Streamlit applications demonstrating advanced LangChain + Ollama capabilities. One project per day will be pushed to Github to showcase the functionality of Langchain with clear examples.

## Prerequisites

1.  **Install Ollama**: [Download Ollama](https://ollama.com/)
2.  **Check Available Models**:
    Ensure you have `llama3.2`, `gemma3:12b`, and `nomic-embed-text` installed.
    ```bash
    ollama list
    ```

## Installation

1.  Navigate to this directory (if not already there):
    ```bash
    # You should be in the root of the langchain-ollama repo
    ```
2.  Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Demos

You can run each demo individually using Streamlit.

### 1. Multi-LLM Selector
Switch between models mid-chat.
```bash
streamlit run 01_multi_llm_selector/app.py
```