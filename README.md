# Enact Python SDK

![Status: Alpha](https://img.shields.io/badge/Status-Alpha-yellow) ![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg) [![Discord](https://img.shields.io/badge/Discord-Enact_PROTOCOL-blue?logo=discord&logoColor=white)](https://discord.gg/mMfxvMtHyS)

The Enact Python SDK provides a Python implementation of the Enact Protocol, a standardized framework for defining and executing automated tasks and workflows. This SDK enables you to create, share, and execute reusable, composable, and verifiable capabilities in a structured, auditable environment.

## Features

- 🔍 Semantic search for tasks using natural language
- 🔄 Execute tasks locally or remotely
- 📦 Automatic dependency management with virtual environments
- 💾 Smart caching of virtual environments
- 🛡️ Isolated execution environments for each unique dependency set

## Installation

```bash
pip install enact-python
```

## Quick Start

### Basic Task Execution

```python
from enact import EnactClient
import asyncio

async def main():
    # Initialize client
    client = EnactClient("http://localhost:8080")

    # Execute a task
    result = await client.execute_task("text-processor", {
        "text": "Hello, world!"
    })
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### Semantic Search

Find tasks using natural language descriptions:

```python
from enact import EnactClient
import asyncio

async def main():
    client = EnactClient("http://localhost:8080")
    
    # Search for tasks
    results = await client.search_tasks(
        "process text input and perform analytics"
    )
    
    # Process results
    for result in results:
        print(f"\nTask ID: {result.id}")
        print(f"Description: {result.description}")
        print(f"Similarity Score: {result.similarity}")
        
        # Execute highly relevant tasks
        if result.similarity > 0.8:
            result = await client.execute_task(result.id, {
                "text": "Sample text for analysis"
            })
            print("Output:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## Task Definition

Tasks in Enact follow a standardized YAML schema:

```yaml
enact: 1.0.0
id: TextProcessor
name: Text Analysis
description: Processes text and returns analytics
version: 1.0.0
type: atomic
authors:
    - name: Jane Doe
dependencies:
    python:
        version: ">=3.9,<4.0"
        packages:
            - name: pandas
              version: ">=2.0.0,<3.0.0"
inputs:
    text:
        type: string
        description: Text to analyze
tasks:
    -   id: analyze
        type: script
        language: python
        code: |
            # Task implementation
flow:
    steps:
        - task: analyze
outputs:
    analysis:
        type: object
        description: Analysis results
```

## Dependency Management

The SDK handles dependencies automatically:

- Creates isolated virtual environments for each dependency set
- Caches environments at `~/.enact/venvs`
- Manages Python version compatibility
- Handles package installation

Example task execution with dependencies:

```python
# Task with pandas dependency will automatically:
# 1. Create/reuse virtual environment
# 2. Install required packages
# 3. Execute in isolated environment
result = await client.execute_task("DataAnalyzer", {
    "data": [1, 2, 3, 4, 5]
})
```

## Development

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/enact-python.git
cd enact-python
```

2. Install dependencies:
```bash
poetry install
```

3. Run tests:
```bash
poetry run pytest
```

### Project Structure

```
enact-python/
├── src/
│   └── enact/
│       ├── __init__.py
│       ├── client.py       # Main client implementation
│       ├── models.py       # Pydantic models
│       ├── executor.py     # Task execution logic
│       └── dependency_manager.py  # Dependency management
├── tests/
├── examples/
└── pyproject.toml
```

## Best Practices

1. **Task Design**
   - Keep tasks focused on single responsibility
   - Make inputs and outputs explicit
   - Include proper error handling
   - Document dependencies clearly

2. **Searching Tasks**
   - Use natural language descriptions
   - Check similarity scores for relevance
   - Verify input requirements before execution

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

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

## Related Resources

- [Enact Protocol Specification](https://github.com/EnactProtocol/specification)
- [Join our Discord](https://discord.gg/mMfxvMtHyS)

