import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import ConfigurableField

st.set_page_config(page_title="Temperature Tuner Agent", layout="wide")

st.title("Temperature Tuner: Deterministic vs. Creative")
st.markdown("""
Adjust the **Temperature** and **Max Tokens** of the LLM on-the-fly without re-initializing the model.
- **Low Temp `(0.1)`**: Deterministic, factual, good for data extraction or trading bots.
- **High Temp `(0.9)`**: Creative, random, good for storytelling.
""")

# Sidebar settings
st.sidebar.header("Agent Settings")

mode = st.sidebar.radio("Mode", ["Single Run", "Compare (Deterministic vs Creative)"])

if mode == "Single Run":
    temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    max_tokens = st.sidebar.slider("Max Tokens (num_predict)", 50, 500, 200, 10)
else:
    st.sidebar.info("Comparison Mode: Running the same chain with Low (0.1) and High (0.9) temperature.")

# 1. Define LLM with default settings
llm = OllamaLLM(model="llama3.2", temperature=0.5, num_predict=200)

# 2. Make fields configurable
# This allows us to override 'temperature' and 'num_predict' at runtime
configurable_llm = llm.configurable_fields(
    temperature=ConfigurableField(id="llm_temperature", name="LLM Temperature", description="The temperature of the LLM"),
    num_predict=ConfigurableField(id="llm_max_tokens", name="Max Tokens", description="Maximum tokens to generate")
)

# 3. Simple Chain (acting as our "Agent" for this demo)
prompt = ChatPromptTemplate.from_template("You are a helpful assistant. Answer the following request: {input}")
chain = prompt | configurable_llm

input_text = st.text_input("Enter your request:", value="Write a short haiku about coding.")

if st.button("Run Agent"):
    with st.spinner("Running..."):
        if mode == "Single Run":
            # 4. Invoke with config containing the slider values
            response = chain.invoke(
                {"input": input_text},
                config={
                    "configurable": {
                        "llm_temperature": temperature,
                        "llm_max_tokens": max_tokens
                    }
                }
            )
            
            st.subheader("Output")
            st.write(response)
            
            st.divider()
            st.subheader("Configuration Used")
            st.json({
                "model": "llama3.2",
                "temperature": temperature,
                "max_tokens": max_tokens
            })
            st.code(f"""
# The Magic Line
chain.invoke(..., config={{
    "configurable": {{
        "llm_temperature": {temperature}, 
        "llm_max_tokens": {max_tokens}
    }}
}})
            """)
        else:
            # Comparison Mode
            col1, col2 = st.columns(2)
            
            # Run Deterministic
            with col1:
                st.subheader("🔵 Deterministic (Temp 0.1)")
                with st.spinner("Running Deterministic..."):
                    response_det = chain.invoke(
                        {"input": input_text},
                        config={
                            "configurable": {
                                "llm_temperature": 0.1,
                                "llm_max_tokens": 200
                            }
                        }
                    )
                    st.write(response_det)
                    st.caption("Config: `temperature=0.1`")

            # Run Creative
            with col2:
                st.subheader("🔴 Creative (Temp 0.9)")
                with st.spinner("Running Creative..."):
                    response_creative = chain.invoke(
                        {"input": input_text},
                        config={
                            "configurable": {
                                "llm_temperature": 0.9,
                                "llm_max_tokens": 200
                            }
                        }
                    )
                    st.write(response_creative)
                    st.caption("Config: `temperature=0.9`")
            
            st.divider()
            st.subheader("💡 equivalent code")
            st.code("""
# One object, two behaviors!
chain.invoke(..., config={"configurable": {"llm_temperature": 0.1}})
chain.invoke(..., config={"configurable": {"llm_temperature": 0.9}})
            """, language="python")
