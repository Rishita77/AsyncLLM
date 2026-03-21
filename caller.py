from typing import Optional
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv
from core.rate_limiter import TokenBucket

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=API_KEY)

async def call_llm(prompt:str, request_bucket: TokenBucket, token_bucket: TokenBucket) -> Optional[str]:
    
    estimated_tokens = len(prompt.split()) * 1.5
    
    await request_bucket.acquire(1)
    await token_bucket.acquire(int(estimated_tokens))
       
    response = await client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )
    
    return response.output_text