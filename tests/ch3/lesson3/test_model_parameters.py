import subprocess
import os
from pathlib import Path
import pytest
from dotenv import dotenv_values
from tests.support.constants import LLM_TIMEOUTS, DEFAULT_TIMEOUT

# Path to the lesson script under test
SCRIPT_PATH = Path("ch3_chat_models/3_model_parameters.py")


# 🔹 Ollama-specific test
@pytest.mark.ollama
@pytest.mark.parametrize("env_file", [".env.test.ollama"])
def test_model_parameters_script_ollama(env_file):
    _run_and_verify_model_parameters(env_file)


# 🔹 OpenAI-specific test
@pytest.mark.openai
@pytest.mark.parametrize("env_file", [".env.test.openai"])
def test_model_parameters_script_openai(env_file):
    _run_and_verify_model_parameters(env_file)


# 🔹 Anthropic-specific test
@pytest.mark.anthropic
@pytest.mark.parametrize("env_file", [".env.test.anthropic"])
def test_model_parameters_script_anthropic(env_file):
    _run_and_verify_model_parameters(env_file)


# 🔧 Shared test logic
def _run_and_verify_model_parameters(env_file):
    env_path = Path(env_file)
    if not env_path.exists():
        pytest.skip(f"{env_file} not found")

    env_vars = os.environ.copy()
    env_vars.update(dotenv_values(env_path))
    provider = env_vars.get("MODEL_PROVIDER", "").lower()
    timeout = LLM_TIMEOUTS.get(provider, DEFAULT_TIMEOUT)

    result = subprocess.run(
        ["python", str(SCRIPT_PATH)],
        capture_output=True,
        env=env_vars,
        text=True,
        timeout=timeout
    )

    # 🔍 Validate script executed without error
    assert result.returncode == 0, f"Script failed:\n{result.stderr}"

    output = result.stdout.strip()

    # 🔍 Validate non-trivial LLM output
    assert len(output) > 50, f"Response too short:\n{output}"

    # 🔍 Validate topic appears in output
    assert "cowboy" in output.lower(), "Expected word 'cowboy' missing from output"
