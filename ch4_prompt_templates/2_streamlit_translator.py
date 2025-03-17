from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from languages import *

load_dotenv()

from langchain_openai import ChatOpenAI

import streamlit as st

example_prompt = PromptTemplate.from_template("Translate the following text from English to {language}: {text_to_translate}")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)



st.title("Language Translation from English")

source_text = st.text_area("Text to translate:")
target_language = st.selectbox("Target language:", languages)
translate = st.button("Translate")

if translate:

    prompt = example_prompt.invoke({"language":target_language,"text_to_translate":source_text})

    output = llm.invoke(prompt)

    st.write(f"{output.content}")
