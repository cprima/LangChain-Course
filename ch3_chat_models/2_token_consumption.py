from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

output = llm.invoke("why is the sky blue?")

print(f"OUTPUT:\n{output.content}\n\nTOKEN CONSUMPTION:{output.response_metadata['token_usage']}")
