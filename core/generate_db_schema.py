import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()


def generateDatabaseSchemaFromNL(description: str) -> dict:
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": base_prompt}]
    )

    schema_output_str = response.choices[0].message.content
    schema = json.loads(schema_output_str)

    return schema


@app.get("/generate_schema/")
def get_schema(description: str):
    if not description:
        raise HTTPException(status_code=400, detail="Description must be provided in search query")

    try:
        db_schema = generateDatabaseSchemaFromNL(description)
        return db_schema

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not decode JSON response from OpenAI.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))