from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from ai_agent import get_response_ai_agent
import uvicorn

# ✅ Define allowed models
ALLOWED_MODEL_NAMES = ["llama3-70b-8192", "mixtral-8x-7b-32768", "llama-3.3-70b-versatile"]

# ✅ Define request structure
class RequestState(BaseModel):
    model_name: str
    model_provider: str
    system_prompt: str
    messages: List[str]
    allow_search: bool

# ✅ Initialize FastAPI app
app = FastAPI(title="AI Chat Bot")

# ✅ API endpoint for chatting
@app.post("/chat")
def chat_endpoint(request: RequestState):
    print("📥 Received Request:", request.dict())  # Log input

    try:
        if request.model_name not in ALLOWED_MODEL_NAMES:
            return {"error": "Model not supported"}

        # Unpack request
        llm_id = request.model_name
        query = request.messages[-1]  # Use last user message
        allow_search = request.allow_search
        system_prompt = request.system_prompt
        provider = request.model_provider

        # 🧠 Get AI response
        response = get_response_ai_agent(llm_id, query, allow_search, system_prompt, provider)
        return {"response": response}

    except Exception as e:
        print("❌ Error occurred:", str(e))
        return {"error": str(e)}


# ✅ Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

