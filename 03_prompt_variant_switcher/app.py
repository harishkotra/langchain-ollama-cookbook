import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import ConfigurableField

st.set_page_config(page_title="Prompt Variant Switcher", layout="wide")

st.title("Prompt Variant Switcher")
st.markdown("""
This demo shows how to **hot-swap Prompt Templates** (personas) at runtime using
LangChain's `configurable_alternatives` directly on a `PromptTemplate`.
""")

# Sidebar config
st.sidebar.header("Prompt Strategy")
prompt_type = st.sidebar.radio(
    "Select Persona",
    ["Concise (Brief)", "Verbose (Detailed)", "Side-by-side Compare"],
    index=0
)

# 1. Define Prompts
concise_template = PromptTemplate.from_template(
    "Answer the following question in 10 words or less: {question}"
)

verbose_template = PromptTemplate.from_template(
    """You are a verbose, detailed professor. 
    Please answer the following question with extensive background context, examples, and a long explanation. 
    
    Question: {question}"""
)

# 2. Make prompt configurable
# We set 'concise' as the default, and 'verbose' as an alternative
prompt = concise_template.configurable_alternatives(
    ConfigurableField(id="prompt_type"),
    default_key="concise",
    verbose=verbose_template
)

# 3. LLM
llm = OllamaLLM(model="llama3.2")
chain = prompt | llm

question = st.text_input("Ask a question:", "Why is the sky blue?")

if st.button("Get Answer"):
    compare_mode = "Side-by-side" in prompt_type
    selected_key = "concise" if "Concise" in prompt_type else "verbose"

    if compare_mode:
        with st.spinner("Answering with both personas..."):
            concise_response = chain.invoke(
                {"question": question},
                config={"configurable": {"prompt_type": "concise"}}
            )
            verbose_response = chain.invoke(
                {"question": question},
                config={"configurable": {"prompt_type": "verbose"}}
            )

        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Concise")
            st.write(concise_response)
            st.caption("Prompt Template")
            st.code(concise_template.template)

        with col_right:
            st.subheader("Verbose")
            st.write(verbose_response)
            st.caption("Prompt Template")
            st.code(verbose_template.template)
    else:
        with st.spinner(f"Answering with '{selected_key}' persona..."):
            response = chain.invoke(
                {"question": question},
                config={"configurable": {"prompt_type": selected_key}}
            )

        st.success(f"**Persona Used:** {selected_key.title()}")
        st.write(response)

        st.divider()
        st.caption("Prompt Template Used:")
        if selected_key == "concise":
            st.code(concise_template.template)
        else:
            st.code(verbose_template.template)

st.divider()
st.caption("How it works")
st.code(
    """
# 1) Define multiple templates
concise = PromptTemplate.from_template("Answer in 10 words: {question}")
verbose = PromptTemplate.from_template("Explain with detail: {question}")

# 2) Create a switchable prompt node
prompt = concise.configurable_alternatives(
    ConfigurableField(id="prompt_type"),
    default_key="concise",
    verbose=verbose,
)

# 3) Choose at runtime via config
chain.invoke(
    {"question": "Why is the sky blue?"},
    config={"configurable": {"prompt_type": "verbose"}},
)
""".strip(),
    language="python",
)