from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

import streamlit as st

st.title("Ask questions to an LLM")

prompt = st.chat_input("Ask me anything..")

if prompt:

    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0,
        max_completion_tokens=1000
    )

    output = llm.invoke(f"{prompt}")


    st.write(f"{output.content}")