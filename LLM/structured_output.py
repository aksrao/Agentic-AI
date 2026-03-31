from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from load_api import load_models
from pydantic import BaseModel

class Answer_with_structure(BaseModel):
    '''An answer to the user's question along with justification for the
    answer.'''
    answer: str
    '''The answer to the user's question'''
    justification: str
    '''Justification for the answer'''

GOOGLE_API_KEY = load_models("gemini")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY, temperture=0)
structured_llm = llm.with_structured_output(Answer_with_structure)

res = structured_llm.invoke("""What weighs more, a pound of bricks or a pound of feathers""")
print(res)
