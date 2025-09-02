from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from tavily import TavilyClient
import os

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API environment variable is not set")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API environment variable is not set")

# Initialize LLM and Tavily client
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class MessagesState(TypedDict):
    output: str
    user_input: str
    search_context: str

def router(state: MessagesState) -> str:
    """Decide whether to use Tavily or go directly to Gemini."""
    query = state["user_input"].lower()
    # Very simple heuristic (you can improve with regex or LLM classifier)
    search_keywords = ["weather", "news", "who", "what", "when", "where", "current", "latest", "temperature"]
    if any(word in query for word in search_keywords):
        return "tavily_search"
    return "assistant"

def tavily_search(state: MessagesState) -> MessagesState:
    """Fetch search results from Tavily."""
    query = state["user_input"]
    response = tavily_client.search(query)
    if response["results"]:
        context = "\n".join([res["content"] for res in response["results"][:2]])
    else:
        context = "No relevant search results found."
    return {"output": "", "user_input": query, "search_context": context}

def assistant(state: MessagesState) -> MessagesState:
    """Generate LLM response with optional Tavily context."""
    if state.get("search_context"):
        prompt = f"""
        The user asked: "{state['user_input']}"
        
        Here is real-time information from Tavily search:
        {state['search_context']}
        
        Please answer using this context.
        """
    else:
        prompt = state["user_input"]

    response = llm.invoke(prompt)
    output = response.content if hasattr(response, "content") else str(response)
    return {"output": output, "user_input": state["user_input"], "search_context": state.get("search_context", "")}

# Build graph
builder = StateGraph(MessagesState)

# Add nodes
builder.add_node("tavily_search", tavily_search)
builder.add_node("assistant", assistant)

# Add edges
builder.add_conditional_edges(START, router, {"tavily_search": "tavily_search", "assistant": "assistant"})
builder.add_edge("tavily_search", "assistant")
builder.add_edge("assistant", END)

graph = builder.compile()

# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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
        result = graph.invoke({"user_input": query, "search_context": ""})
        return {"output": result["output"]}
    except Exception as e:
        return {"output": f"Error: {str(e)}"}, 500
