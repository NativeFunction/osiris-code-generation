import asyncio
import json

from fastapi import HTTPException
from pydantic import BaseModel


class CodeRequest(BaseModel):
    description: str


class Api3:
    def __init__(self, _client, router):
        self.client = _client
        router.add_api_route(
            path="/generate_db_schema/",
            endpoint=self.get_schema,
            methods=["POST"]
        )

    def generateDatabaseSchemaFromNL(self, description: str) -> dict:
        base_prompt = (
            "Create a database schema based on the following description: "
            f"{description}\n"
            "The schema should be in Python dictionary format like this:\n"
            "{\n"
            "    \"tables\": {\n"
            "        \"users\": {\n"
            "            \"name\": \"string\",\n"
            "            \"email\": \"string\",\n"
            "            \"age\": \"integer\"\n"
            "        }\n"
            "    }\n"
            "}\n"
            "Make sure the output is a valid Python dictionary."
        )

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": base_prompt}]
        )

        schema_output_str = response.choices[0].message.content
        schema = json.loads(schema_output_str)

        return schema

    async def get_schema(self, request: CodeRequest):
        if not request.description:
            raise HTTPException(status_code=400, detail="Description must be provided in search query")

        try:
            db_schema = await asyncio.to_thread(self.generateDatabaseSchemaFromNL, request.description)
            return db_schema

        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail="Could not decode JSON response from OpenAI.")

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
