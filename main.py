import asyncio
from batch_processor import run_batch

async def main() -> None:
    
    prompts = [
        "Explain philosophy in LLMs in 21st century",
        "Explain docker to a beginner",
    ]

    results = await run_batch(prompts, num_workers=5)
    
    for r in results:
        print(f"\nID: {r.request_id}")
        print(f"Latency: {r.latency:.2f}s" if r.latency else "Latency: N/A")
        print(f"Output: {r.output_text}")
        print(f"Error: {r.error}")

    
    
asyncio.run(main())
    
    