# Chatbot App 🤖

This is a simple chatbot application built using **FastAPI**, **LangGraph**, and **LangChain with Google Gemini (Generative AI)**.
The app demonstrates how to create a conversational agent with a graph-based workflow and serve it through an API endpoint.

---

![Chatbot Screenshot](backend_fastapi\Screenshot_2.png)
## 🚀 Features

* **Google Gemini LLM**: Powered by `ChatGoogleGenerativeAI` to handle natural language queries.
* **LangGraph Workflow**: Uses `StateGraph` to manage state transitions between nodes.
* **FastAPI Integration**: Exposes chatbot functionality as REST API endpoints.
* **Environment Variables**: Keeps API keys safe with `.env` file configuration.

---

## 🛠️ Tech Stack

* **Python**
* **FastAPI** (for API endpoints)
* **LangGraph** (to structure the chatbot workflow)
* **LangChain** (for LLM integration)
* **Google Gemini API** (LLM model)
* **dotenv** (for environment variables)

---

## 📂 Project Structure

```bash
.
├── main.py         # Main application file (chatbot + API routes)
├── .env            # Environment file (stores Gemini API key)
├── requirements.txt # Project dependencies
└── README.md       # Documentation
```

---

## ⚙️ Setup & Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/your-username/chatbot-app.git
   cd chatbot-app
   ```

2. **Create and activate virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Mac/Linux
   venv\Scripts\activate      # On Windows
   ```

3. **Install dependencies**

   ```bash
   uv add fastapi
   uv add uvicorn python-dotenv
   uv add langgraph langgraph-google-genai
   ```

4. **Create `.env` file** and add your Gemini API key:

   ```bash
   GEMINI_API=your_google_api_key_here
   ```

5. **Run the server**

   ```bash
   uv run uvicorn main:app --reload
   ```

---

## 🔗 API Endpoints

* **Root** (welcome message)

  ```http
  GET /
  ```

* **Chat with the bot**

  ```http
  GET /chat/{query}
  ```

  Example:

  ```http
  GET /chat/Hello%20there
  ```

  Response:

  ```json
  {
    "output": "Hello! How can I help you today?"
  }
  ```

---

## 📌 Example Usage

```bash
curl http://127.0.0.1:8000/chat/What%20is%20LangGraph
```

Response:

```json
{
  "output": "LangGraph is a framework for building graph-based AI agents..."
}
```

<img width="462" height="410" alt="postman_upload" src="https://github.com/user-attachments/assets/0e1b0eb3-6a97-405e-a0c2-4b8160709727" />




---

## ✅ Future Improvements

* Add memory to maintain multi-turn conversations.
* Extend graph with multiple nodes for different tasks.
* Build a frontend (React/Next.js) to interact with the chatbot.

