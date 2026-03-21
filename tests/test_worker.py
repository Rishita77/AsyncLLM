import pytest
import asyncio
from worker import worker
from models import LLMResponse

@pytest.mark.asyncio
async def test_worker_processes_success():
    queue = asyncio.Queue()
    result_queue = asyncio.Queue()

    await queue.put(("1", "test prompt"))
    await queue.put(None)

    async def fake_call(prompt, *_):
        return "mocked response"

    async def dummy_bucket(*args, **kwargs):
        return None

    task = asyncio.create_task(
        worker(
            "W1",
            queue,
            result_queue,
            dummy_bucket,
            dummy_bucket,
            fake_call
        )
    )

    await task

    result = await result_queue.get()

    assert isinstance(result, LLMResponse)
    assert result.output_text == "mocked response"
    assert result.error is None