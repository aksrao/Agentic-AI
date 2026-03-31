from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from load_api import load_models
from langchain_core.prompts import PromptTemplate

GOOGLE_API_KEY = load_models("gemini")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=GOOGLE_API_KEY)


template = PromptTemplate.from_template("""Answer the question based on the
    context below. If the question cannot be answered using the information
    provided, answer with "I don't know".
    Context: {context}
    Question: {question}
    Answer: """
)
prompt = template.invoke({
    "context": """The most recent advancements in NLP are being driven by Large
    Language Models (LLMs). These models outperform their smaller
    counterparts and have become invaluable for developers who are creating
    applications with NLP capabilities. Developers can tap into these
    models through Hugging Face's `transformers` library, or by utilizing
    OpenAI and Cohere's offerings through the `openai` and `cohere`
    libraries, respectively.""",
    "question": "Which is apple"
})

response = llm.invoke(prompt)
print(response.content)