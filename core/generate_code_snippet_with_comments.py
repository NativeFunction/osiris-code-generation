import os
from fastapi import FastAPI, HTTPException
from openai import OpenAI
import json

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)
app = FastAPI()


def generateCodeWithCommentsFromNL(description: str, language: str) -> str:
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

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": base_prompt}]
    )

    output = response.choices[0].message.content
    return output

@app.get("/generate_code_with_comments/")
def get_code_with_comments(description: str, language: str):
    if not description:
        raise HTTPException(status_code=400, detail="Description must be provided in search query")

    try:
        code_with_comments = generateCodeWithCommentsFromNL(description, language)
        return code_with_comments

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Could not decode JSON response from OpenAI.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
