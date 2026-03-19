import os
import asyncio
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=API_KEY)

async def main() -> None:
    response = await client.responses.create(
        model="gpt-4o-mini",
        input="You are a pirate. What is the capital of France?"
    )
    print(response.output_text)
    
asyncio.run(main())
    
    