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

<img width="2882" height="2440" alt="screencapture-localhost-8501-2026-02-07-13_16_02" src="https://github.com/user-attachments/assets/e95acfe6-6a31-44d1-b4e4-91bad84c4e72" />
<img width="2882" height="5498" alt="screencapture-localhost-8501-2026-02-07-13_17_49" src="https://github.com/user-attachments/assets/41b4f87a-6d50-4368-b126-57966e588f07" />


### 2. Temperature Tuner Agent
Adjust creativity (temperature) on the fly.
```bash
streamlit run 02_temp_tuner_agent/app.py
```

<img width="2884" height="2520" alt="screencapture-localhost-8501-2026-02-09-23_07_55" src="https://github.com/user-attachments/assets/befef4be-1a75-41d0-9de7-02d14f6b27c0" />
<img width="2884" height="2520" alt="screencapture-localhost-8501-2026-02-09-23_09_03" src="https://github.com/user-attachments/assets/6d0adc62-e6d9-4e95-b627-31b06f56eafe" />
<img width="2884" height="2520" alt="screencapture-localhost-8501-2026-02-09-23_09_09" src="https://github.com/user-attachments/assets/4770ef97-4a6a-4f5c-9058-23fbb28560c4" />
