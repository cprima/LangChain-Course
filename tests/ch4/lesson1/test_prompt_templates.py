import subprocess
import os
from pathlib import Path
import pytest
from dotenv import dotenv_values
from tests.support.constants import LLM_TIMEOUTS, DEFAULT_TIMEOUT

SCRIPT_PATH = Path("./ch4_prompt_templates/1_prompt_templates.py")

# Ollama
@pytest.mark.ollama
@pytest.mark.parametrize("env_file", [".env.test.ollama"])
def test_script_ollama(env_file):
    _run_and_verify_script(env_file)

# OpenAI
@pytest.mark.openai
@pytest.mark.parametrize("env_file", [".env.test.openai"])
def test_script_openai(env_file):
    _run_and_verify_script(env_file)

# Anthropic
@pytest.mark.anthropic
@pytest.mark.parametrize("env_file", [".env.test.anthropic"])
def test_script_anthropic(env_file):
    _run_and_verify_script(env_file)

# Shared logic
def _run_and_verify_script(env_file):
    env_path = Path(env_file)
    if not env_path.exists():
        pytest.skip(f"{env_file} not found")

    env = os.environ.copy()
    env.update(dotenv_values(env_path))
    provider = env.get("MODEL_PROVIDER", "").lower()
    timeout = LLM_TIMEOUTS.get(provider, DEFAULT_TIMEOUT)

    result = subprocess.run(
        ["python", str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout
    )

    assert result.returncode == 0, f"Script failed:\n{result.stderr}"
    assert result.stdout.strip(), "Script returned no output"
