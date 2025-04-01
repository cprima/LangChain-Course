import subprocess
import os
from pathlib import Path
import pytest
from dotenv import dotenv_values
from tests.support.constants import LLM_TIMEOUTS, DEFAULT_TIMEOUT

# Script under test
SCRIPT_PATH = Path("ch3_chat_models/4_token_consumption.py")

# Test for OpenAI backend
@pytest.mark.openai
@pytest.mark.parametrize("env_file", [".env.test.openai"])
def test_token_script_openai(env_file):
    _run_and_verify(env_file)

# Test for Ollama backend
@pytest.mark.ollama
@pytest.mark.parametrize("env_file", [".env.test.ollama"])
def test_token_script_ollama(env_file):
    _run_and_verify(env_file)

# Test for Anthropic backend
@pytest.mark.anthropic
@pytest.mark.parametrize("env_file", [".env.test.anthropic"])
def test_token_script_anthropic(env_file):
    _run_and_verify(env_file)


def _run_and_verify(env_file):
    # Skip if the specific .env file doesn't exist
    env_path = Path(env_file)
    if not env_path.exists():
        pytest.skip(f"Missing {env_file}")

    # Load environment variables from the test env file
    env = os.environ.copy()
    env.update(dotenv_values(env_path))

    # Use a backend-specific timeout
    provider = env.get("MODEL_PROVIDER", "").lower()
    timeout = LLM_TIMEOUTS.get(provider, DEFAULT_TIMEOUT)

    # Execute the script as a subprocess with the configured environment
    result = subprocess.run(
        ["python", str(SCRIPT_PATH)],
        capture_output=True,
        text=True,
        env=env,
        timeout=timeout
    )

    # Ensure the script executed without error
    assert result.returncode == 0, f"Script error:\n{result.stderr}"

    # Expect at least 4 lines of output: model name + token stats
    lines = result.stdout.strip().splitlines()
    assert len(lines) >= 4, f"Unexpected output:\n{result.stdout}"

    # Parse and validate numeric token output
    try:
        input_tokens = int(lines[1].split(":")[1].strip())
        output_tokens = int(lines[2].split(":")[1].strip())
        total_tokens = int(lines[3].split(":")[1].strip())
    except Exception as e:
        pytest.fail(f"Failed to parse tokens:\n{result.stdout}\n{e}")

    # Assert token counts are valid and internally consistent
    assert input_tokens > 0, "Input token count must be positive"
    assert 100 <= output_tokens <= 5000, "Output token count out of expected range"
    assert total_tokens == input_tokens + output_tokens, "Token total mismatch"
