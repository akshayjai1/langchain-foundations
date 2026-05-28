# Using uv with Jupyter Notebooks

This guide explains how to set up and use `uv` for managing Python dependencies in Jupyter notebooks.

## Prerequisites

- Python 3.12+ installed
- `uv` installed (install via `pip install uv` or `pipx install uv`)

## Setup Steps

### 1. Run `uv sync`

Sync your project dependencies from `pyproject.toml`:

```bash
uv sync
```

If you encounter SSL certificate issues, use:

```bash
uv sync --allow-insecure-host pypi.org --allow-insecure-host files.pythonhosted.org
```

### 2. Start Jupyter Lab

Use `uv run` to launch Jupyter Lab with your project's dependencies:

```bash
uv run jupyter lab
```

Or specify a notebook to open directly:

```bash
uv run jupyter lab notebooks/module-1/1.2_tools.ipynb
```

If port 8888 is already in use, specify a different port:

```bash
uv run jupyter lab --port=8889
```

## How It Works

- `uv sync` creates/updates a `.venv` virtual environment with all dependencies from `pyproject.toml`
- `uv run` executes commands within that environment, making all installed packages available
- Jupyter Lab runs with access to all your project's dependencies

## Common Commands

| Command | Description |
|---------|-------------|
| `uv sync` | Install/update dependencies from pyproject.toml |
| `uv run jupyter lab` | Start Jupyter Lab with project dependencies |
| `uv run jupyter execute notebook.ipynb` | Execute a notebook non-interactively |
| `uv run python script.py` | Run a Python script with project dependencies |

## Troubleshooting

### Port Already in Use
If you see "The port 8888 is already in use", either:
- Stop the existing Jupyter process
- Use a different port: `uv run jupyter lab --port=8889`

### SSL Certificate Errors
If you see certificate errors during `uv sync`, use the `--allow-insecure-host` flag as shown above.

### Kernel Not Found
If Jupyter doesn't find your kernel, restart Jupyter Lab after running `uv sync`.
