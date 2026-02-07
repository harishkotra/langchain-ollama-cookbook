import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField

st.set_page_config(page_title="Multi-LLM Selector", layout="wide")

st.title("Multi-LLM Selector with LangChain + Ollama")
st.markdown("""
This demo showcases how to switch between different local LLMs (Ollama) dynamically using **`configurable_alternatives`**.
Instead of redefining the chain, we simply pass a config parameter at runtime.
""")

# Sidebar controls
st.sidebar.header("Configuration")
selected_model = st.sidebar.selectbox(
    "Select Model",
    ["llama3.2", "gemma3:4b", "qwen3:4b"],
    help="Switch between models instantly."
)

# 1. Define the base model (llama3.2)
llm = OllamaLLM(model="llama3.2")

# 2. Add alternatives configurable via 'model_provider' id
llm_with_fallback = llm.configurable_alternatives(
    ConfigurableField(id="model_provider"), 
    default_key="llama",
    gemma=OllamaLLM(model="gemma3:4b"),
    qwen=OllamaLLM(model="qwen3:4b"),
)

# 3. Create a simple chain that passes input through
prompt_template = ChatPromptTemplate.from_template("{input}")
chain = prompt_template | llm_with_fallback

# User Input
st.subheader("Enter your prompt")

# Quick Prompts
quick_prompts = {
    "Custom": "",
    "Creative Writing": "Write a short poem about a robot discovering nature for the first time.",
    "Coding": "Write a Python function to check if a string is a palindrome, with type hints and docstrings.",
    "Reasoning": "If a train leaves Station A at 60 mph and another leaves Station B at 80 mph, and they are 300 miles apart, when will they meet?",
    "Fun Fact": "Tell me a fun fact about capybaras."
}

selected_prompt_type = st.selectbox("Quick Prompts", list(quick_prompts.keys()), index=0)

# managing state for the text area if a quick prompt is selected
if selected_prompt_type != "Custom":
    default_text = quick_prompts[selected_prompt_type]
else:
    default_text = ""

# If the user switches prompt types, we want to update the text area. 
# However, if they type in "Custom", we keep it. 
# A simple way is to use `value` which updates on rerun if the key changes or we can just rely on user manual input for custom.
# Let's use session state to handle the preset updates cleanly if we wanted to be very fancy, 
# but for this simple app, we can just set the value if it's not custom, 
# or let the user type if it is. 
# ACTUALLY, to make it simple and robust:
user_input = st.text_area("Your Prompt:", value=default_text, height=150)

if st.button("Generate"):
    if not user_input:
        st.warning("Please enter a prompt.")
    else:
        # Map the selection to the key used in configurable_alternatives
        # "llama3.2" -> "llama" (default)
        # "gemma3:4b" -> "gemma"
        # "qwen3:4b" -> "qwen"
        
        config_map = {
            "llama3.2": "llama",
            "gemma3:4b": "gemma",
            "qwen3:4b": "qwen"
        }
        
        config_key = config_map.get(selected_model, "llama")
        
        with st.spinner(f"Generating with {selected_model}..."):
            try:
                # 4. Invoke with config
                response = chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"model_provider": config_key}}
                )
                
                # Visual Confirmation of the Switch
                st.success("Generation Complete!")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(label="Active Model", value=selected_model)
                    if config_key == "llama":
                        st.info("Used **Default** Path")
                    else:
                        st.warning(f"Used **Alternative** Path: `{config_key}`")
                with col2:
                    st.markdown(response)
                
                st.divider()
                
                st.subheader("🔍 How `configurable_alternatives` Routed This Request")
                
                # Create two columns to show the "Switch" concept
                route_col1, route_col2 = st.columns(2)
                
                with route_col1:
                    st.markdown("### 1. The Setup")
                    st.code("""
llm = OllamaLLM(model="llama3.2")
llm_with_fallback = llm.configurable_alternatives(
    ConfigurableField(id="model_provider"), 
    default_key="llama",
    gemma=OllamaLLM(model="gemma3:4b"),
    qwen=OllamaLLM(model="qwen3:4b"),
)
                    """, language="python")
                    
                with route_col2:
                    st.markdown("### 2. The Runtime Config")
                    st.markdown(f"You selected **{selected_model}**, so we passed:")
                    st.json({
                        "configurable": {
                            "model_provider": config_key
                        }
                    })
                    if config_key == "llama":
                        st.caption("Matches `default_key='llama'`, so **llama3.2** was used.")
                    else:
                        st.caption(f"Matches key='{config_key}', so **{selected_model}** was used.")

                st.markdown("### 3. The Execution Code")
                st.code(f"""
chain.invoke(
    {{"input": "{user_input}"}},  # <--- Your prompt passed here
    config={{"configurable": {{"model_provider": "{config_key}"}}}}
)
                """, language="python")
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info(f"Make sure you have run `ollama pull {selected_model}`")
