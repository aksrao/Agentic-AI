import os
from dotenv import load_dotenv

def load_models()-> str:

    load_dotenv(override=True)


    GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

    if GOOGLE_API_KEY:
        print("Check: Keys Loaded successfully.")
    else:
        print("Check: Keys Missing! Check your `.env` file.")
    return GOOGLE_API_KEY
