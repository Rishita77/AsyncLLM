import pytest
from core.retry import retry_with_backoff

@pytest.mark.asyncio
async def test_retry_succeeds_after_failures():
    attempts = 0
    
    async def flaky():
        nonlocal attempts
        attempts += 1
        
        if attempts < 3:
            raise Exception("fail")
        
        return "success"
    
    result = await retry_with_backoff(flaky, max_retries=5)
    
    assert result == "success"
    assert attempts == 3