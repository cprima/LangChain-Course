from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

from langchain_openai import ChatOpenAI

example_prompt = PromptTemplate.from_template("Translate the following text from English to {language}: {text_to_translate}")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

chain = example_prompt | llm | StrOutputParser()

result = chain.invoke({"language":"French","text_to_translate":"Flower"})

print(result)