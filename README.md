# enact-python

Python SDK for the Enact protocol. Execute and manage protocol tasks locally or remotely.

## Installation

```bash
pip install enact-python
```

## Quick Start

```python
from enact import EnactClient

# Initialize client
client = EnactClient("https://api.myregistry.com")

# Execute a task
result = await client.execute_task("GetStockPrice", {
    "ticker": "AAPL",
    "api_key": "xxx"
})
print(result)
```

## Development

This project uses Poetry for dependency management. To get started:

1. Install Poetry: https://python-poetry.org/docs/#installation
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Run tests:
   ```bash
   poetry run pytest
   ```

## License

MIT
