import asyncio

from fastapi import HTTPException
from pydantic import BaseModel


class CodeRequest(BaseModel):
    description: str
    language: str


class Api7:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate_code_with_comments/",
            endpoint=self.get_code_with_comments,
            methods=["POST"]
        )

    def generateCodeWithCommentsFromNL(self, description: str, language: str) -> str:
        base_prompt = (
            f"Generate {language} code from the following description with inline comments:\n"
            f"{description}\n"
            "Example input: 'Create a Python function that checks if a number is even'\n"
            "Expected output format:\n"
            "\"\"\"\n"
            "def is_even(n):\n"
            "    # Check if the number is divisible by 2\n"
            "    if n % 2 == 0:\n"
            "        return True\n"
            "    # If not divisible by 2, it's not even\n"
            "    return False\n"
            "\"\"\""
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": base_prompt}]
        )

        output = response.choices[0].message.content
        return output

    async def get_code_with_comments(self, request: CodeRequest):
        if not request.description:
            raise HTTPException(status_code=400, detail="Description must be provided in search query")

        if not request.language:
            raise HTTPException(status_code=400, detail="Language must be provided in search query")

        try:
            code_with_comments = await asyncio.to_thread(self.generateCodeWithCommentsFromNL, request.description,
                                                         request.language)
            return code_with_comments

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
