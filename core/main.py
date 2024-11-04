from fastapi import FastAPI, HTTPException, APIRouter
from openai import OpenAI
import os
import asyncio
from dotenv import load_dotenv
from api1 import *
from api9 import *

load_dotenv()
app = FastAPI()
router = APIRouter()

# Retrieve OpenAI API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("Missing OpenAI API key. Set the OPENAI_API_KEY environment variable.")

client = OpenAI(api_key=openai_api_key)

api1 = Api1(client, router)
api9 = Api9(client, router)

app.include_router(router)

#start server from /core with below
#python -m uvicorn main:app --reload

