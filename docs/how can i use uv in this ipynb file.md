# how can i use uv in this ipynb file

Exported: 5/28/2026, 7:30:28 AM

---

**User:**

how can i use uv in this ipynb file

---

**Assistant:**

I'll help you set up `uv` in your Jupyter notebook. Let me first check the current notebook content and your project setup.



To use `uv` in your Jupyter notebook, you have a few options:

## Option 1: Use `uv` to run the notebook directly (recommended)

```bash
uv run jupyter notebook notebooks/module-1/1.2_tools.ipynb
```

Or for a one-off execution:
```bash
uv run jupyter execute notebooks/module-1/1.2_tools.ipynb
```

## Option 2: Install `uv`-managed packages in the notebook

Add this to a cell at the top of your notebook:

```python
import sys
import subprocess

# Use uv to install packages in the current environment
subprocess.check_call([sys.executable, "-m", "uv", "pip", "install", "langchain", "python-dotenv"])
```

## Option 3: Create a `pyproject.toml` for your notebook project

Create a `pyproject.toml` in your notebook directory:

```toml
[project]
name = "langchain-foundations"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "langchain",
    "python-dotenv",
    "jupyter",
]

[tool.uv]
dev-dependencies = [
    "jupyter",
    "notebook",
]
```

Then run:
```bash
uv sync
uv run jupyter notebook
```

## Option 4: Use `uv` to create a dedicated kernel

```bash
# Create a new virtual environment with uv
uv venv .venv-uv
uv pip install langchain python-dotenv jupyter

# Register as a Jupyter kernel
uv run python -m ipykernel install --user --name=uv-kernel --display-name="Python (uv)"
```

Then select "Python (uv)" as your kernel in Jupyter.

---

**Which approach would you like to use?** I can help you set it up based on your preference.

---

**User:**

i already have pyproject.tom, lets run uv sync, but then how do we run specific notebook that is open

---

**Assistant:**

Let me check for the `pyproject.toml` and run `uv sync`.



I see the issue - there's a network certificate problem when trying to download packages. The `uv sync` is failing due to SSL certificate issues.

To run your specific notebook after `uv sync` completes, use:

```bash
uv run jupyter lab notebooks/module-1/1.2_tools.ipynb
```

Or to just open it in JupyterLab:
```bash
uv run jupyter lab
```

Then navigate to your notebook.

**For the certificate issue**, you can try:

1. **Skip certificate verification** (not recommended for production):
   ```bash
   uv sync --no-cert
   ```

2. **Or configure uv to use a different index**:
   ```bash
   uv sync --index-url https://pypi.org/simple/
   ```

3. **Or update certificates**:
   ```bash
   sudo apt-get update && sudo apt-get install --reinstall ca-certificates
   ```

Would you like me to try running `uv sync` with the `--no-cert` flag to bypass the certificate issue?

---

**User:**

yes please run uv sync --no-cert

---

**Assistant:**

I see the correct flag is `--allow-insecure-host`. Let me run it:



`uv sync` completed successfully. Now to run your specific notebook:



Port 8888 is already in use. Let me stop this process and try with a different port:



Jupyter Lab is now running on port 8889. The notebook `1.2_tools.ipynb` should be open in the interface.

**Summary:**
- `uv sync --allow-insecure-host` completed successfully (228 packages installed)
- Jupyter Lab is running at: `http://localhost:8889/lab?token=dbc14ebf450d641b4c21fdb56f8dd1c3d4b3dc30b9ab6197`

You can access it in your browser using that URL. The notebook `1.2_tools.ipynb` should be open in the interface.

---

**User:**

please create learning document based on this session in /docs folder

---

**Assistant:**

Created `/docs/using-uv-with-jupyter.md` with:
- Step-by-step setup instructions
- Common commands reference
- Troubleshooting tips for port conflicts and SSL issues

---
