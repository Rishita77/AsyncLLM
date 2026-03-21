from typing import Optional
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=API_KEY)

async def call_llm(prompt:str) -> Optional[str]:
       
    response = await client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )
    
    return response.output_text