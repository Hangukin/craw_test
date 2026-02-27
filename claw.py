import asyncio
import os
from zeroclaw_tools import create_agent, shell, file_read, file_write
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

gemini_key = os.getenv('GEMINI_API_KEY')

async def main():
    # Create agent with tools
    agent = create_agent(
        tools=[shell, file_read, file_write],
        model="gemini-1.5-flash",
        api_key=gemini_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/"
    )
    
    # Execute a task
    result = await agent.ainvoke({
        "messages": [HumanMessage(content="List files in /tmp directory")]
    })
    
    print(result["messages"][-1].content)

asyncio.run(main())