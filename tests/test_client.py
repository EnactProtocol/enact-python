import pytest
from enact import EnactClient

@pytest.mark.asyncio
async def test_get_task():
    client = EnactClient("http://localhost:8000")
    # Add your tests here
    assert True

@pytest.mark.asyncio
async def test_execute_task():
    client = EnactClient("http://localhost:8000")
    # Add your tests here
    assert True
