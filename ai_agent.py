from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()

# ✅ Define custom DuckDuckGo tool
@tool
def duckduckgo_search(query: str) -> str:
    """Searches the web using DuckDuckGo and returns the top 3 result snippets."""
    with DDGS() as ddgs:
        results = ddgs.text(query)
        top_results = list(results)[:3]
        if not top_results:
            return "No relevant results found."
        return "\n\n".join([f"{r['title']}:\n{r['body']}\n{r['href']}" for r in top_results])


# ✅ System prompt
default_system_prompt = (
    "You are a smart and friendly AI assistant. "
    "Use the DuckDuckGo search tool only when strictly necessary. "
    "Otherwise, rely on your own knowledge."
)

# ✅ Response generation function
def get_response_ai_agent(llm_id: str, query: str, allow_search: bool, system_prompt: str, provider: str):
    llm = ChatGroq(model='llama-3.3-70b-versatile')

    tools = [duckduckgo_search] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt or default_system_prompt
    )

    state = {"messages": [HumanMessage(content=query)]}
    result = agent.invoke(state)
    messages = result.get("messages")

    ai_messages = [m.content for m in messages if isinstance(m, AIMessage)]
    return ai_messages[-1] if ai_messages else "No AI response generated."
