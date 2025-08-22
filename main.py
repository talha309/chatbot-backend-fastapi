from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API environment variable is not set")

# Initialize the language model
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

class MessagesState(TypedDict):
    output: str
    user_input: str

def assistant(state: MessagesState) -> MessagesState:
    response = llm.invoke(state["user_input"])
    # Extract string content from AIMessage object
    output = response.content if hasattr(response, "content") else str(response)
    return {"output": output}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_edge(START, "assistant")
builder.add_edge("assistant", END)
graph = builder.compile()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def route():
    return {"message": "Welcome to Chatbot App"}

@app.get("/chat/{query}")
async def get_content(query: str):
    try:
        result = graph.invoke({"user_input": query})
        return {"output": result["output"]}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}, 500