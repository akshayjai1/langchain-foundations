# Using Ollama with LangChain Foundations

This guide explains how to replace OpenAI API calls with Ollama, a local LLM runtime, in this LangChain foundations project.

## Why Use Ollama?

- **No API costs**: Run models locally without paying per token
- **Privacy**: Your data never leaves your machine
- **Offline capability**: Work without internet connection
- **Experimentation**: Try different models freely
- **No rate limits**: Only limited by your hardware

## Prerequisites

### 1. Install Ollama

Download and install Ollama from [ollama.ai](https://ollama.ai)

**Windows**: Download the installer from the website
**macOS**: `brew install ollama`
**Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

### 2. Pull Models

After installation, pull the models you want to use:

```bash
# Recommended models for this project
ollama pull llama3.2        # Fast, good for general tasks
ollama pull llama3.1:8b     # Balanced performance
ollama pull mistral         # Good alternative
ollama pull phi3            # Lightweight option

# For advanced use cases
ollama pull llama3.1:70b    # High quality (requires more RAM)
ollama pull codellama       # Optimized for code
```

### 3. Verify Ollama is Running

```bash
ollama list                 # List installed models
ollama serve                # Start Ollama server (usually auto-starts)
```

## Method 1: Using langchain-ollama (Recommended)

### Installation

Add to your `pyproject.toml` dependencies:

```toml
dependencies = [
    # ... existing dependencies
    "langchain-ollama>=0.1.0",
]
```

Or install directly:

```bash
pip install langchain-ollama
```

### Usage in Notebooks

Replace OpenAI imports with Ollama:

```python
# Instead of:
# from langchain_openai import ChatOpenAI
# llm = ChatOpenAI(model="gpt-4")

# Use:
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

# Use exactly the same as before
response = llm.invoke("Hello, how are you?")
print(response.content)
```

### Configuration Options

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,           # Creativity (0.0 - 1.0)
    num_predict=256,           # Max tokens to generate
    top_k=40,                  # Diversity parameter
    top_p=0.9,                 # Nucleus sampling
    repeat_penalty=1.1,        # Penalize repetition
    base_url="http://localhost:11434",  # Ollama server URL
)
```

## Method 2: Using langchain-community Ollama

### Installation

Already included in your dependencies:

```toml
"langchain-community>=0.4.1",
```

### Usage

```python
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

# For simple text completion
llm = Ollama(model="llama3.2")

# For chat-based interactions (recommended)
chat_model = ChatOllama(model="llama3.2")

# Use with chains
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("user", "{input}")
])

chain = prompt | chat_model
response = chain.invoke({"input": "Explain quantum computing"})
```

## Method 3: Using OpenAI-Compatible API

Ollama provides an OpenAI-compatible API endpoint, so you can use existing OpenAI code with minimal changes.

### Usage

```python
from langchain_openai import ChatOpenAI

# Point to Ollama's OpenAI-compatible endpoint
llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Required but not used
    model="llama3.2",
)

# Use exactly as you would with OpenAI
response = llm.invoke("Hello!")
```

## Method 4: Environment Variable Configuration

Create a configuration system to switch between providers easily.

### Update .env file

```bash
# Choose provider: openai, ollama, anthropic
LLM_PROVIDER=ollama

# OpenAI settings
OPENAI_API_KEY=your-key-here

# Ollama settings
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# Anthropic settings
ANTHROPIC_API_KEY=your-key-here
```

### Create a helper module

Create `llm_factory.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm(temperature=0.7, **kwargs):
    """Factory function to get LLM based on environment configuration."""
    provider = os.getenv("LLM_PROVIDER", "openai").lower()

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

# Usage in notebooks
llm = get_llm()
response = llm.invoke("Hello!")
```

## Adapting Specific Notebooks

### Module 1: Foundational Models

**1.1_foundational_models.ipynb / 1.1_prompting.ipynb**

```python
# Original
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4")

# Replace with
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.2")
```

**1.2_tools.ipynb / 1.2_web_search.ipynb**

```python
# Ollama models support tool calling
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",  # Ensure model supports function calling
    temperature=0,
)

# Bind tools as usual
llm_with_tools = llm.bind_tools([your_tool])
```

**Note**: Not all Ollama models support function calling. Use `llama3.1`, `llama3.2`, or `mistral` for tool support.

**1.4_multimodal_messages.ipynb**

```python
# For vision capabilities, use LLaVA models
from langchain_ollama import ChatOllama

# Pull vision model first: ollama pull llava
llm = ChatOllama(model="llava")

# Use with image messages
from langchain_core.messages import HumanMessage

message = HumanMessage(
    content=[
        {"type": "text", "text": "What's in this image?"},
        {"type": "image_url", "image_url": {"url": "path/to/image.jpg"}},
    ]
)

response = llm.invoke([message])
```

### Module 2: Advanced Patterns

**2.1_travel_agent.ipynb & 2.3_multi_agent.ipynb**

```python
# Replace all LLM initializations
from langchain_ollama import ChatOllama

# For agents
agent_llm = ChatOllama(
    model="llama3.1:8b",  # Use models with good reasoning
    temperature=0.7,
)

# For supervisors (use larger models if possible)
supervisor_llm = ChatOllama(
    model="llama3.1:70b",  # Or llama3.1:8b if RAM limited
    temperature=0,
)
```

**2.2_state.ipynb & 2.4_wedding_planners.ipynb**

```python
# LangGraph works seamlessly with Ollama
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph

llm = ChatOllama(model="llama3.2")

# Use in graph nodes as usual
def my_node(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}
```

### Module 3: Production Patterns

**3.4_dynamic_models.ipynb**

```python
# Switch between models dynamically
def get_model_for_task(task_type):
    if task_type == "simple":
        return ChatOllama(model="phi3")  # Fast, lightweight
    elif task_type == "complex":
        return ChatOllama(model="llama3.1:70b")  # High quality
    else:
        return ChatOllama(model="llama3.2")  # Balanced

llm = get_model_for_task("complex")
```

## Model Recommendations by Use Case

| Use Case | Recommended Model | Why |
|----------|------------------|-----|
| General chat | `llama3.2` | Fast, good quality |
| Code generation | `codellama` | Optimized for code |
| Tool calling | `llama3.1:8b` | Supports function calling |
| Vision tasks | `llava` | Multimodal support |
| Fast prototyping | `phi3` | Lightweight, quick |
| High quality | `llama3.1:70b` | Best reasoning (needs 32GB+ RAM) |
| Long context | `llama3.1:8b` | 128k context window |

## Performance Considerations

### Hardware Requirements

- **Minimum**: 8GB RAM for 7B parameter models
- **Recommended**: 16GB RAM for 8B models, 32GB for 13B models
- **High-end**: 64GB+ RAM for 70B models
- **GPU**: Optional but significantly faster (NVIDIA, AMD, or Apple Silicon)

### Speed Optimization

```python
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    num_predict=128,        # Limit output length
    num_ctx=2048,           # Reduce context window if not needed
    num_gpu=1,              # Use GPU if available
    num_thread=8,           # Adjust based on CPU cores
)
```

### Batch Processing

```python
# Process multiple requests efficiently
llm = ChatOllama(model="llama3.2")

# Use batch method
responses = llm.batch([
    "Question 1",
    "Question 2",
    "Question 3",
])
```

## Troubleshooting

### Ollama Not Running

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama manually
ollama serve
```

### Model Not Found

```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama3.2
```

### Out of Memory

- Use smaller models (`phi3`, `llama3.2:3b`)
- Reduce `num_ctx` parameter
- Close other applications
- Consider using quantized models

### Slow Performance

- Enable GPU acceleration
- Use smaller models for development
- Reduce `num_predict` for shorter responses
- Increase `num_thread` for CPU inference

### Function Calling Not Working

Ensure you're using a model that supports function calling:

```bash
# These models support function calling
ollama pull llama3.1:8b
ollama pull llama3.2
ollama pull mistral
```

## Hybrid Approach

You can use both OpenAI and Ollama in the same project:

```python
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# Use Ollama for development/testing
dev_llm = ChatOllama(model="llama3.2")

# Use OpenAI for production/complex tasks
prod_llm = ChatOpenAI(model="gpt-4")

# Choose based on environment
import os
llm = dev_llm if os.getenv("ENV") == "dev" else prod_llm
```

## Cost Comparison

| Scenario | OpenAI (GPT-4) | Ollama (Local) |
|----------|----------------|----------------|
| 1M input tokens | ~$10 | $0 (electricity only) |
| 1M output tokens | ~$30 | $0 (electricity only) |
| Development | Pay per use | Free unlimited |
| Production | Scales with usage | Fixed hardware cost |

## Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [LangChain Ollama Integration](https://python.langchain.com/docs/integrations/llms/ollama)
- [Ollama Model Library](https://ollama.ai/library)
- [LangChain Model Comparison](https://python.langchain.com/docs/integrations/chat/)

## Next Steps

1. Install Ollama and pull a model
2. Test with a simple notebook (1.1_prompting.ipynb)
3. Create the `llm_factory.py` helper for easy switching
4. Update your `.env` file with Ollama configuration
5. Gradually migrate notebooks as needed

Happy local LLM experimentation! 🚀
# 2
Based on the guide, here's how to use Ollama with `init_chat_model`:

## Method 1: Using OpenAI-compatible endpoint (simplest)

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model="llama3.2",
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but not used
)

response = model.invoke("Hello!")
print(response.content)
```

## Method 2: Using langchain-ollama directly

```python
from langchain_ollama import ChatOllama
from langchain.chat_models import init_chat_model

# init_chat_model can accept a model instance
model = init_chat_model(model=ChatOllama(model="llama3.2"))

response = model.invoke("Hello!")
print(response.content)
```

## Method 3: Using environment variable

Update your `.env`:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

Then:

```python
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="llama3.2",
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = model.invoke("Hello!")
print(response.content)
```

## Pull a model first

Make sure you have a model pulled:

```bash
ollama pull llama3.2
ollama list  # Verify it's installed
```

The OpenAI-compatible endpoint method (Method 1) is usually the simplest since `init_chat_model` already supports the `base_url` parameter.
