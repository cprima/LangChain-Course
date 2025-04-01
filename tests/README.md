
# 🧪 Test Framework for LangChain-Course

This test suite verifies selected LangChain course scripts using real LLM backends, configured via `.env.test.*` files. It checks token usage and response behavior across providers.

---

### 🔒 Testing Philosophy

Lesson scripts are treated as standalone executables. They are **not imported** or modified during testing.

Each script is executed via `subprocess.run(...)`, preserving original behavior. `.env.test.*` files are injected through the `env=` argument to control provider, model, and API credentials.

This approach ensures:

- Authentic execution, consistent with course intent
- Isolation between tests and lesson logic
- Compatibility with real-world APIs and environments

Refactoring scripts into importable functions is intentionally avoided to remain aligned with the educational source.

---

## ✅ Test Structure

```
tests/
├── ch3/
│   └── lesson5/
│       └── test_token_consumption.py
├── support/
│   └── constants.py
├── conftest.py
└── README.md  ← this file
```

---

## ⚙️ Setup

1. **Install test dependencies** (inside an activated virtual environment):

```bash
pip install -r requirements-dev.txt
```

2. **Create provider-specific `.env` test files**:

```bash
cp .env.test.example .env.test.openai
cp .env.test.example .env.test.ollama
cp .env.test.example .env.test.anthropic
```

3. **Edit each file** to set `MODEL_PROVIDER`, `CHAT_MODEL`, and API keys as needed.

---

## 🧪 Running Tests

Run all tests:

```bash
pytest -v
```

Run tests for a specific backend:

```bash
pytest -m openai
pytest -m ollama
pytest -m anthropic
```

---

## 🕒 Per-Provider Timeouts

Some providers (e.g. Ollama) are slower. Timeout durations are defined in:

```python
# tests/support/constants.py

LLM_TIMEOUTS = {
    "openai": 30,
    "anthropic": 30,
    "ollama": 120,
}
```

---

## 📦 Git Hygiene

Git excludes:

```
.env.test.*
```

Only the example file is tracked:

```
.env.test.example
```

---

## 🧼 Notes

- Tests do not import or refactor lesson scripts.
- Tests run scripts in subprocesses using real `.env` context.
- Tests are skipped if required `.env.test.*` files are missing.
```
