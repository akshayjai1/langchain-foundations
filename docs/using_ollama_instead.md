# since I am majorly using ollama, instead of doi...

Exported: 6/1/2026, 6:40:32 AM

---

**User:**

since I am majorly using ollama, instead of doing dot_env in every new jupyter notebook cell and then defining the ollama model, i feel it will be better to create a python file and import it, so that it gets automatically executed, am i right

---

**Assistant:**

You're absolutely right. Creating a Python module for Ollama setup is a much cleaner approach than repeating the same initialization code in every notebook. This gives you several advantages:

1. **Single source of truth** - Update Ollama config in one place
2. **DRY principle** - No repeated code across notebooks
3. **Easier maintenance** - Changes propagate automatically
4. **Cleaner notebooks** - Focus on the actual logic, not boilerplate

Let me check your current setup and create a reusable module for you.

Perfect. I can see you already have `.env` configured with Ollama settings. Now I'll create a dedicated module for Ollama initialization that you can import in any notebook. This will be much cleaner than repeating the setup code.

Done. Now in any notebook, instead of:

```python
from dotenv import load_dotenv
load_dotenv()

from langchain_ollama import OllamaLLM
import os

llm = OllamaLLM(
    model=os.getenv("OLLAMA_MODEL"),
    base_url=os.getenv("OLLAMA_BASE_URL")
)
```

You just do:

```python
from ollama_setup import llm
```

And you're ready to use `llm` in your chains and agents. The module automatically loads your `.env` file and initializes Ollama with your configured settings.

A few benefits:
- **Single import** - one line instead of 5-6
- **Consistent config** - all notebooks use the same Ollama setup
- **Easy to update** - change settings in one place
- **Cleaner notebooks** - focus on the actual logic

You can also customize the module further if needed (add temperature, top_p, or other parameters). Want me to add any other configuration options?

---

**User:**

suppose, i need to import 
file in 
, how to do it

---

**Assistant:**

You can't directly import a Jupyter notebook into another notebook the way you'd import a Python module. However, there are a few practical approaches:

## Option 1: Extract code to a Python module (Recommended)

Convert the reusable code from `1.1_prompting.ipynb` into a Python file, then import it. For example, create `c:\code\p\langchain-foundations\notebooks\module-1\prompting_utils.py`:

```python
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel

class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str

def create_scifi_agent(system_prompt=None):
    """Create a sci-fi writer agent"""
    return create_agent(
        model="gpt-5-nano",
        system_prompt=system_prompt or "You are a science fiction writer"
    )

def get_capital_response(agent, question_text):
    """Get response from agent"""
    question = HumanMessage(content=question_text)
    return agent.invoke({"messages": [question]})
```

Then in your other notebook:
```python
from prompting_utils import create_scifi_agent, get_capital_response

agent = create_scifi_agent()
response = get_capital_response(agent, "What's the capital of the Moon?")
```

## Option 2: Use `nbimport` (if you really need to import the notebook)

Install `nbimport`:
```bash
pip install nbimport
```

Then in your notebook:
```python
import nbimport
import importlib.util

# Load the notebook as a module
spec = importlib.util.spec_from_file_location(
    "prompting", 
    "1.1_prompting.ipynb"
)
prompting = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prompting)
```

This is hacky and not recommended for production.

## Option 3: Use `%run` magic (Quick and dirty)

In your notebook cell:
```python
%run 1.1_prompting.ipynb
```

This executes all cells from that notebook in your current kernel, making all variables available. Simple but messy for larger notebooks.

---

**My recommendation:** Go with **Option 1**. Extract the useful functions and classes into `prompting_utils.py`, then import them cleanly. This keeps your notebooks focused and makes code reusable across multiple notebooks.

Want me to help you refactor the prompting notebook into a utility module?

---

**User:**

i do not understood, why we did not had to write `from notebooks.module-1.prompting_utils import create_scifi_agent`

---

**Assistant:**

Good question! The reason is that when you're in a Jupyter notebook, Python's import system looks for modules in the current working directory (the directory where the notebook is running from), not relative to the notebook's location.

Let me check the current setup:



Here's what's happening:

## Why `from prompting_utils import ...` works

When you run a notebook in `notebooks/module-1/`, Python's import system looks for modules in:
1. The current working directory (where you launched Jupyter from)
2. `sys.path` entries

If you launch Jupyter from `c:\code\p\langchain-foundations`, then:
- `c:\code\p\langchain-foundations` is in `sys.path`
- `c:\code\p\langchain-foundations\notebooks\module-1` is a subdirectory
- So `from prompting_utils import ...` works because Python finds it in the current directory

## Why `from notebooks.module-1.prompting_utils import ...` doesn't work

For that to work, you'd need:
1. An `__init__.py` file in `notebooks/module-1/` to make it a package
2. The parent directory (`c:\code\p\langchain-foundations`) to be in `sys.path`

Let me check if there's an `__init__.py`:



No `__init__.py`, so `notebooks.module-1` isn't a Python package.

## To use the full dotted import, you'd need:

1. Create `notebooks/module-1/__init__.py` (can be empty)
2. Create `notebooks/__init__.py` (can be empty)
3. Then `from notebooks.module-1.prompting_utils import ...` would work

But there's a simpler approach - make the project installable. Since you already have `pyproject.toml`, you can install the project in editable mode:

```bash
uv pip install -e .
```

Then create a proper package structure:

```
lc_foundations/
├── __init__.py
└── notebooks/
    └── module-1/
        ├── __init__.py
        └── prompting_utils.py
```

But honestly, for notebooks, the simplest approach is:
- Put utility files in the same directory as your notebooks
- Use `from prompting_utils import ...` (relative to current directory)
- Or use `%run prompting_utils.ipynb` to execute another notebook

Would you like me to set up the proper package structure with `__init__.py` files so you can use the dotted imports?

---

**User:**

please fix import ollama_setup.py
llm.invoke("what is capital of India")

---

**Assistant:**

I need to understand the issue better. Let me check what error you're getting:

The issue is that when you're in a notebook inside `notebooks/module-1/`, Python can't find `ollama_setup.py` which is in the parent directory `c:\code\p\langchain-foundations\`.

Here are the solutions:

## Solution 1: Add parent directory to Python path (Quick fix)

In your notebook, add this cell at the top:

```python
import sys
sys.path.insert(0, '../..')  # Go up two directories to reach the root

from ollama_setup import llm
llm.invoke("what is capital of India")
```

## Solution 2: Move ollama_setup.py to the notebooks directory (Better)

This way it's accessible from all notebooks:

Let me use the right command for your system:

Perfect! Now in your notebook (`1.1_foundational_models.ipynb`), you can simply use:

```python
from ollama_setup import llm

llm.invoke("what is capital of India")
```

The module is now in the `notebooks/` directory, so it's accessible from all notebooks in `module-1/`, `module-2/`, and `module-3/`.

**Why this works:**
- When you run a notebook from `notebooks/module-1/`, Python looks for imports in the current directory and parent directories
- `ollama_setup.py` is now in `notebooks/`, which is the parent directory
- So `from ollama_setup import llm` finds it automatically

Try it now and let me know if it works!

---

**User:**

```notebooks/module-1/1.1_foundational_models.ipynb (1-4)
import ollama_setup.py

llm.invoke("what is capital of India")
```
How do I fix the following problem in the above code?: ModuleNotFoundError: No module named 'ollama_setup'

---

**Assistant:**

The issue is in your import statement. You have:

```python
import ollama_setup.py
```

This is wrong in two ways:
1. You don't include `.py` in import statements
2. You should use `from` to import the `llm` object

Fix it to:

```python
from ollama_setup import llm

llm.invoke("what is capital of India")
```

Let me update your notebook:

Let me read the notebook to see the exact format:

Now I can fix it. The issue is the import statement has `.py` in it:

Done! The fix was simple:

**Change this:**
```python
import ollama_setup.py
```

**To this:**
```python
from ollama_setup import llm
```

The key differences:
- Remove `.py` from the import (Python adds that automatically)
- Use `from ... import` to get the `llm` object directly
- Now you can call `llm.invoke()` without any prefix

Your notebook should work now!

---

**User:**

```notebooks/module-1/1.1_foundational_models.ipynb (1-4)
from ollama_setup import llm

llm.invoke("what is capital of India")
```
How do I fix the following problem in the above code?: ModuleNotFoundError: No module named 'ollama_setup'

---

**Assistant:**

The issue is that Python still can't find `ollama_setup` even though we created it in the `notebooks/` directory. This happens because Jupyter's working directory might not include the parent path.

Add this to the top of your notebook (before the import):

```python
import sys
sys.path.insert(0, '..')

from ollama_setup import llm
llm.invoke("what is capital of India")
```

The `sys.path.insert(0, '..')` adds the parent directory (`notebooks/`) to Python's search path, so it can find `ollama_setup.py`.

Let me update your notebook:

Let me check the exact format in the JSON:

Now I can fix it:

Done! Now your notebook has:

```python
import sys
sys.path.insert(0, '..')

from ollama_setup import llm

llm.invoke("what is capital of India")
```

This tells Python to look in the parent directory (`notebooks/`) for modules, so it finds `ollama_setup.py`. Try running it now!

---
