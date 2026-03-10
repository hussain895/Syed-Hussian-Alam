# Stack Visualization (Dash)

Simple interactive Stack visualization using Plotly Dash.

Features:
- Push a value onto the stack
- Pop the top value
- Peek (view) the top value
- Visual stack display (top shown at top)

Prerequisites
- Python 3.8+
- Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run

```bash
python3 app.py
```

Open http://127.0.0.1:8050 in your browser.

Using a virtual environment (venv)

It's recommended to use a Python virtual environment to isolate dependencies.

1. Create and activate a venv (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, run the included helper to create the venv and install packages:

```bash
./setup_venv.sh
```

