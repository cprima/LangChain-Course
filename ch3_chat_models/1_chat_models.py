from dotenv import load_dotenv

load_dotenv()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=2,
    max_completion_tokens=1000
)

output = llm.invoke("write a story about an astronaut")

print(output.content)