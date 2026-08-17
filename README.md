# EchoFlow

EchoFlow is an AI-powered Windows voice input assistant. Press a global hotkey, speak naturally, and have the resulting text inserted into your active application.

## Prerequisites
- Windows 10/11
- Python 3.12+
- NVIDIA API Key

## Setup
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -e .[dev]`
5. Copy `.env.example` to `.env` and add your NVIDIA API key.

## Architecture
EchoFlow is primarily a PySide6 application with a modular architecture for speech-to-text, LLM processing, and Windows interactions.

## Development
To format and check code:
```bash
ruff format .
ruff check .
mypy .
pytest
```
