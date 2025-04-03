# client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain import hub
from langchain_core.messages import HumanMessage

# Set your OpenAI API key
import os
os.environ["OPENAI_API_KEY"] = "your-openai-api-key"

# Initialize the OpenAI model
model = ChatOpenAI(model="gpt-4o-mini")

# Pull the ReAct prompt from LangChain Hub
#prompt = hub.pull("hwchase17/react")

# Define MCP server parameters
server_params = StdioServerParameters(
    command="python",
    args=["math_server.py"],  # Path to your MCP server script
)

# Async function to run the agent
async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()  # Connect to the MCP server
            tools = await load_mcp_tools(session)  # Load MCP tools into LangChain
            agent = create_react_agent(model, tools)  # Create a ReAct agent with prompt
            # Pass messages as a list of message objects
            response = await agent.ainvoke({
                "messages": [HumanMessage(content="What’s (5 + 7) × 2?")]
            })
            # Print the full response for debugging
            print("Full response:", response)
            # Access the last message's content as the result
            result = response["messages"][-1].content
            print("Result:", result)
            return result

if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)
