import os
from dotenv import load_dotenv

def load_models(model: str)-> str:

    load_dotenv(override=True)


    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
    HF_TOKEN = os.getenv("hugging_face_api")

    if GOOGLE_API_KEY and HF_TOKEN:
        print("Check: Keys Loaded successfully.")
        if model == "gemini":
            return GOOGLE_API_KEY
        else:
            return HF_TOKEN
    else:
        print("Check: Keys Missing! Check your `.env` file.")
