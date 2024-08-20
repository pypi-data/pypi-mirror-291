import asyncio
import aiohttp
import json
import requests

from typing import (
    Any,
    Callable,
    Dict,
    Optional
)
from pydantic import BaseModel, root_validator

from openfinance.agentflow.llm.base import BaseLLM, Message

class Qwen(BaseLLM):
    name = "Qwen"
    api_key: str
    base_url: str

    async def acall(
        self,
        content,
        mode: Optional[str] = None  # 可以是"json_object"
    ) -> Dict[str, str]:
        print("content: ", content)
        if isinstance(content, str):
            body = {
                'model': 'qwen-turbo',
                "input": {
                    "messages": [
                        {
                            "role": "user",
                            "content": content
                        }
                    ]
                },
                "parameters": {
                    # "temperature": self.temperature,
                    # "top_p": self.top_p,
                    # "top_k": self.top_k,                    
                    "result_format": "message"
                }
            }

            headers = {
                'Content-Type': 'application/json',
                'Authorization':f'Bearer {self.api_key}'
            }                              
        # print(json.dumps(body, indent=2, ensure_ascii=False))
        # print("self.base_url: ", self.base_url)
        # print("self.api_key: ", self.api_key)
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.base_url,
                json = body,
                headers = headers
            ) as response:
                resp = await response.json()
        # resp = requests.post(self.base_url, headers=headers, json=body)
        print(resp)
        content = resp["output"]["choices"][0]["message"]["content"]
        return Message("assistant", content)

if __name__ == "__main__":
    model = Qwen(
        model="gpt4",
        api_key="",
        base_url=""
    )

    result = asyncio.run(model._acall("what is your name"))
    print(result)
