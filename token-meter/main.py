import os
from typing import Union, List, Tuple, Optional
from dotenv import load_dotenv
import json
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from datetime import datetime
from transformers import AutoTokenizer

load_dotenv(override=True)

app = FastAPI()

class parameters(BaseModel):
    model: Optional[str]
    SBU: str
    payload: Union[str, List[Tuple[str, str]]]
    temperature: Optional[float] = 1.0
    repo_id: Optional[str]
    task: Optional[str]
    provider: Optional[str] = "auto"


def record_tokens(provider, p: parameters, file_path="token_usage.json",usage_metadata = None, output_text = None):
    record= {}
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []

    # Generate next ID
    next_id = len(data) + 1

    if provider == "google":
        input_tokens = usage_metadata.get("input_tokens", 0)
        output_tokens = usage_metadata.get("output_tokens", 0)
        total_tokens = usage_metadata.get("total_tokens", input_tokens + output_tokens)
        
        record = {
            "id": next_id,
            "sbu": p.SBU,
            "model": p.model,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "Input Tokens Used": input_tokens,
            "Output Tokens Used": output_tokens,
            "Total Tokens Used": total_tokens
        }
        data.append(record)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Token usage recorded for google")
    if provider == "Hugging_face":
        prompt = p.payload
        tokenizer = AutoTokenizer.from_pretrained(p.repo_id) 
        input_tokens = len(tokenizer.encode(prompt))
        output_tokens = len(tokenizer.encode(output_text))
        total_tokens = input_tokens + output_tokens
        record = {
            "id": next_id,
            "sbu": p.SBU,
            "model": p.repo_id,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "Input Tokens Used": input_tokens,
            "Output Tokens Used": output_tokens,
            "Total Tokens Used": total_tokens
        }
        data.append(record)
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        print("Token usage recorded for hugging face model:-", p.repo_id)

@app.get("/gemini")
def gemini(p: parameters):
    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    if GOOGLE_API_KEY:
        print("Check: Keys Loaded successfully.")
    else:
        print("Keys are missing")
    llm = ChatGoogleGenerativeAI(model=p.model, api_key=GOOGLE_API_KEY)
    messages=p.payload
    response= llm.invoke(messages)
    record_tokens("google",p ,usage_metadata=response.usage_metadata)
    return response.text

@app.get("/hugging-face")
def hugging_face(p: parameters):

    HF_TOKEN = os.getenv("hugging_face_api")
    if HF_TOKEN:
        print("Check: Keys Loaded successfully.")
    else:
        print("hugging face tokens are missing")
    llm = HuggingFaceEndpoint(
        repo_id= p.repo_id,
        task= p.task,
        huggingfacehub_api_token=HF_TOKEN,
        temperature=p.temperature,
        provider=p.provider
    )
    chat = ChatHuggingFace(llm=llm)
    response = chat.invoke(p.payload)
    record_tokens("Hugging_face",p ,output_text=response.content)
    return response.content