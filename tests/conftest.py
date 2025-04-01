import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model


def load_env_file(env_path: Path):
    if not env_path.exists():
        pytest.skip(f"Missing environment file: {env_path}")
    load_dotenv(dotenv_path=env_path, override=True)


def create_llm_from_env():
    return init_chat_model(
        os.getenv("CHAT_MODEL"),
        model_provider=os.getenv("MODEL_PROVIDER"),
        temperature=0.7
    )


@pytest.fixture
def llm_ollama():
    load_env_file(Path(".env.test.ollama"))
    return create_llm_from_env()


@pytest.fixture
def llm_openai():
    load_env_file(Path(".env.test.openai"))
    return create_llm_from_env()


@pytest.fixture
def llm_anthropic():
    load_env_file(Path(".env.test.anthropic"))
    return create_llm_from_env()
