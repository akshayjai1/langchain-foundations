# Python Packaging and Imports: Common Confusions Clarified

This document clarifies three common confusions when working with Python packages, particularly when integrating Ollama with LangChain.

## 1. Package Names vs Import Names (Hyphens vs Underscores)

### The Confusion
When you see `langchain-ollama` in installation instructions but need to write `from langchain_ollama import ChatOllama` in code, it can be confusing.

### The Explanation
Python has a convention for naming:

- **Package name** (what you install via pip/uv): Uses **hyphens** (`-`)
  - Example: `langchain-ollama`, `langchain-openai`, `google-cloud-storage`

- **Module name** (what you import in code): Uses **underscores** (`_`)
  - Example: `from langchain_ollama import ChatOllama`

### Why This Happens
Python's import system doesn't allow hyphens in module names (they're interpreted as minus operators). So package maintainers use hyphens for the distribution name (more readable) and Python automatically converts them to underscores for imports.

### Examples
| Installation | Import |
|---|---|
| `pip install langchain-ollama` | `from langchain_ollama import ChatOllama` |
| `pip install langchain-openai` | `from langchain_openai import ChatOpenAI` |
| `pip install google-cloud-storage` | `from google.cloud import storage` |
| `pip install python-dotenv` | `from dotenv import load_dotenv` |

### In Your Project
```bash
# Installation with uv
uv pip install langchain-ollama

# Or add to pyproject.toml
dependencies = [
    "langchain-ollama>=0.1.0",
]

# Then in your code
from langchain_ollama import ChatOllama
```

---

## 2. Why `init_chat_model` Doesn't Work with Ollama

### The Confusion
LangChain has a convenient `init_chat_model()` function that works with many providers. You might expect it to work with Ollama like this:

```python
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="llama3.2",
    model_provider="openai",  # ❌ This doesn't work for Ollama
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)
```

But you get an authentication error: `Error code: 401 - Incorrect API key provided`

### Why It Fails
`init_chat_model()` is a **provider-agnostic factory function** that only supports specific built-in providers:

- ✅ `openai`
- ✅ `anthropic`
- ✅ `google_genai`
- ✅ `azure_openai`
- ✅ `bedrock`
- ❌ `ollama` (NOT supported)

When you pass `model_provider="openai"` with a custom `base_url`, it still uses the **OpenAI client** under the hood. The OpenAI client validates the API key format against OpenAI's requirements, which causes the 401 error even though you're pointing to a local Ollama instance.

### The Solution
Use `ChatOllama` directly from the `langchain_ollama` package:

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    base_url="http://localhost:11434",
    temperature=0.7,
)
```

`ChatOllama` is purpose-built for Ollama and doesn't try to validate against OpenAI's API key format.

### When to Use Each
| Use Case | Solution |
|---|---|
| Using OpenAI, Anthropic, Google, etc. | `init_chat_model()` |
| Using Ollama locally | `ChatOllama` directly |
| Need flexibility to switch providers | Create a factory function (see below) |

### Factory Pattern for Flexibility
If you want to switch between providers easily:

```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.7, **kwargs):
    """Factory function to get LLM based on environment configuration."""
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if provider == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(
            model=os.getenv("OLLAMA_MODEL", "llama3.2"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            temperature=temperature,
            **kwargs
        )

    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-4"),
            temperature=temperature,
            **kwargs
        )

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        return ChatAnthropic(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022"),
            temperature=temperature,
            **kwargs
        )

    else:
        raise ValueError(f"Unknown provider: {provider}")

# Usage
llm = get_llm()
response = llm.invoke("Hello!")
```

---

## 3. Using `uv` vs `pip` for Package Management

### The Confusion
You have `uv` installed and configured in your project, but I suggested using `pip install`. This is inconsistent with your project setup.

### The Explanation
Both `pip` and `uv` are Python package managers, but they have different characteristics:

| Feature | pip | uv |
|---|---|---|
| Speed | Slower | 10-100x faster |
| Caching | Basic | Aggressive |
| Dependency Resolution | Sequential | Parallel |
| Lock Files | Optional | Built-in |
| Installation | `pip install` | `uv pip install` or `uv sync` |
| Use Case | General purpose | Modern, performance-focused |

### When to Use Each

**Use `pip` when:**
- Working in a simple environment
- You don't have `uv` installed
- You're in a virtual environment without project management

**Use `uv` when:**
- Your project has `pyproject.toml` (like yours)
- You want faster installs and reproducible builds
- You want to manage the entire project (dependencies, venv, Python version)

### In Your Project
Since you have `uv` configured, use it consistently:

```bash
# ✅ Correct: Add to pyproject.toml
dependencies = [
    "langchain-ollama>=0.1.0",
]

# Then sync
uv sync

# ✅ Alternative: Direct install with uv
uv pip install langchain-ollama

# ❌ Avoid: Using pip directly
pip install langchain-ollama  # This bypasses uv's management
```

### Why Consistency Matters
- **Reproducibility**: `uv` creates lock files that ensure everyone uses the same versions
- **Performance**: `uv` caches dependencies, making subsequent installs much faster
- **Project Integrity**: Mixing `pip` and `uv` can cause version conflicts

---

## Summary: Best Practices

1. **Package Names**: Remember hyphens for installation, underscores for imports
   ```bash
   uv pip install langchain-ollama
   from langchain_ollama import ChatOllama
   ```

2. **Provider Selection**: Use the right tool for the job
   ```python
   # For Ollama
   from langchain_ollama import ChatOllama

   # For OpenAI, Anthropic, etc.
   from langchain.chat_models import init_chat_model
   ```

3. **Package Management**: Stick with `uv` in this project
   ```bash
   # Add to pyproject.toml, then:
   uv sync
   ```

---

## References

- [Python Packaging Guide](https://packaging.python.org/)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/chat/ollama/)
- [uv Documentation](https://docs.astral.sh/uv/)
- [PEP 427 - Wheel Binary Package Format](https://www.python.org/dev/peps/pep-0427/)
