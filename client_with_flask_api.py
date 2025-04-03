# client.py
import asyncio
from mcp import ClientSession
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
import os
os.environ["OPENAI_API_KEY"] = "your-api-key"
model = ChatOpenAI(model="gpt-4o-mini")
SERVER_URL = "http://localhost:8000"  # Adjust based on server output

async def run_agent():
    async with ClientSession(transport="sse", url=SERVER_URL) as session:
        await session.initialize()
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model, tools)
        response = await agent.ainvoke({"messages": [HumanMessage(content="What’s (5 + 7) × 2?")]})
        print("Full response:", response)
        result = response["messages"][-1].content
        print("Result:", result)
        return result

if __name__ == "__main__":
    asyncio.run(run_agent())