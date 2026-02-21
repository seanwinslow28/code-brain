---
name: python-automation
description: Robust Python scripting assistant. Generates scripts for file processing, resilient API clients, AI-powered web scraping, and scheduled tasks. Use when asked to automate workflows, scrape data, process CSVs, or write maintenance scripts.
---

# Python Automation Scripts

## Purpose

Create production-grade automation scripts that are resilient, maintainable, and secure. This skill emphasizes robust error handling (retries, logging), virtual environment isolation, and modern tooling (uv, instructor) over quick-and-dirty one-offs.

## When to Use

- Writing scripts to process files (CSV, JSON, Text)
- Interacting with external APIs (handling rate limits/retries)
- Web scraping (using AI to parse HTML)
- Scheduling periodic tasks (cron configuration)
- Setting up Python environments (venv, requirements.txt)

## Examples

**Example 1: Resilient API Client**
```
User: "Write a script to fetch data from an API, but handle it if it fails"
Claude: [Uses python-automation]
Here is a robust pattern using `requests.Session` with exponential backoff for reliability:

import os
import time
import requests
from requests.exceptions import HTTPError, ConnectionError

def fetch_data_robust(url, retries=3):
    api_key = os.getenv("API_KEY")
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {api_key}"})
    
    for i in range(retries):
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except (ConnectionError, HTTPError) as e:
            print(f"Attempt {i+1} failed: {e}")
            if i < retries - 1:
                time.sleep(2 * (i + 1)) # Exponential backoff
            else:
                raise
    return None
```

**Example 2: AI Web Scraping**
```
User: "Scrape product prices from this HTML using AI"
Claude: [Uses python-automation]
I'll use `instructor` with `beautifulsoup4` to clean the HTML and extract structured data:

import instructor
import anthropic
from bs4 import BeautifulSoup
from pydantic import BaseModel

class Product(BaseModel):
    title: string
    price: float

def extract_products(html_content: str):
    # Clean HTML to save tokens
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup.find_all(["script", "style", "nav"]):
        tag.decompose()
        
    client = instructor.from_anthropic(anthropic.Anthropic())
    return client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"Extract products: {str(soup)}"}],
        response_model=list[Product],
    )
```

## Domain Content

### 1. Robust API Interactions

Always use a `Session` object and implement retries for transient errors (5xx, 429).

**Status Code Strategy**
| Code | Action |
| :--- | :--- |
| 200 | Process data |
| 400/401/403 | Fail immediately (Client error) |
| 429 | Retry with backoff (Rate limit) |
| 500+ | Retry with backoff (Server error) |

### 2. Secure Error Handling Pattern

Distinguish between expected failures and crashes. Use `try/except/else/finally`.

```python
import logging

logger = logging.getLogger(__name__)

def process_securely(request):
    try:
        token = validate_token(request)
    except InvalidTokenError:
        logger.warning("Invalid auth attempt") # Log safe message
        raise # Fail hard
    else:
        # Only runs if no exception
        return execute_action(token)
    finally:
        cleanup_resources()
```

### 3. Environment Management

Use `uv` for fast dependency management, or standard `venv`.

**Standard Setup**
```bash
python -m venv env
source env/bin/activate  # Mac/Linux
pip install requests python-dotenv
pip freeze > requirements.txt
```

**Config Loading (`.env` pattern)**
Never hardcode secrets.
```python
import os
from dotenv import load_dotenv

load_dotenv() # Load from .env file

DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("DATABASE_URL must be set")
```

### 4. Cron Scheduling (GitHub Actions)

Schedule scripts using standard cron syntax in YAML.

**Syntax**: `minute hour day_of_month month day_of_week`

```yaml
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *" # Daily at 09:00 UTC
jobs:
  run-script:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - name: Execute
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: python main.py
```

### 5. CLAUDE.md for Python Projects

Define standards to help Claude maintain the repo.

```markdown
# CLAUDE.md
## Core Commands
- Run: `python src/main.py`
- Test: `pytest`
- Lint: `ruff check .`
- Install: `pip install -r requirements.txt`

## Architecture
- `src/`: Logic
- `scripts/`: Entry points
- `data/`: Temp storage (gitignored)

## Style
- Type hints required for all functions
- Use pathlib, not os.path
```

## Success Criteria

- [ ] Secrets accessed via `os.getenv()` ONLY (no hardcoding)
- [ ] API calls include timeouts and retry logic
- [ ] Virtual environment used (env/ or .venv/)
- [ ] Requirements pinned in `requirements.txt`
- [ ] Error handling blocks don't swallow exceptions silently

## Copy/Paste Ready

```
"Write a Python script to [task]"
"Create a cron job to run this script daily"
"Add error handling to this API call"
"Setup a new Python environment"
```
