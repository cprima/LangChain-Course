from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()

from langchain_openai import ChatOpenAI

example_prompt = PromptTemplate.from_template("Translate the following text from English to {language}: {text_to_translate}")


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

prompt = example_prompt.invoke({"language":"French","text_to_translate":"Flower"})

result = llm.invoke(prompt)

print(result.content)
