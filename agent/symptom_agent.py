# agent/symptom_agent.py
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from agent.prompts import SYSTEM_PROMPT
from agent.tools import ALL_TOOLS

# Environment variables load karein (.env file se)
load_dotenv()

# 1. LLM Setup (Groq use kar rahe hain)
llm = ChatGroq(
    model="llama3-70b-8192", 
    groq_api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

# 2. Agent Setup with Error Handling for different LangGraph versions
try:
    # Latest versions use 'state_modifier'
    agent_executor = create_react_agent(
        llm, 
        tools=ALL_TOOLS, 
        state_modifier=SYSTEM_PROMPT
    )
    print("Agent initialized with state_modifier")
except TypeError:
    try:
        # Some intermediate versions use 'prompt'
        agent_executor = create_react_agent(
            llm, 
            tools=ALL_TOOLS, 
            prompt=SYSTEM_PROMPT
        )
        print("Agent initialized with prompt")
    except TypeError:
        # Fallback for older versions
        agent_executor = create_react_agent(
            llm, 
            tools=ALL_TOOLS
        )
        print("Agent initialized without modifier (Manual system prompt may be needed)")

def get_agent_response(user_input: str):
    """
    User ke input ko agent tak bhejta hai aur response return karta hai
    """
    try:
        # Agent ko invoke karein
        response = agent_executor.invoke({
            "messages": [("user", user_input)]
        })
        
        # Last message content return karein
        return response["messages"][-1].content
    except Exception as e:
        return f"Arre! Thoda error aaya hai: {str(e)}"