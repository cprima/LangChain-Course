import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field
from typing import List

from langchain.chat_models import init_chat_model

class Person(BaseModel):
    name: str
    occupation: str
    related_persons: list[str]


loader = WebBaseLoader("https://en.wikipedia.org/wiki/Benjamin_Franklin")

page = loader.load()


prompt = PromptTemplate.from_template(
"""
"Provide the name of the person (first + last name), the occupation and a list of related
persons for the following person: {person_info}

Don't make things up, and only use the information which is provided to you
""")
                                                                                      
llm = init_chat_model(
    os.getenv("CHAT_MODEL"), 
    model_provider = os.getenv("MODEL_PROVIDER"),
    temperature = 0
)

llm_with_tools = llm.bind_tools([Person])

chain = prompt | llm_with_tools

output = chain.invoke({"person_info":page[0].page_content})

print(output.tool_calls[0]["args"])
