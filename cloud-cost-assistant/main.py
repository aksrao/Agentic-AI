from load_api import load_models
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate

GOOGLE_API_KEY= load_models()

async def main():
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0,api_key=GOOGLE_API_KEY)
    mcp_servers_config= {
            "awslabs.aws-documentation-mcp-server": {
            "command": "uvx",
            "args": ["awslabs.aws-documentation-mcp-server@latest"],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": "ERROR",
                "AWS_DOCUMENTATION_PARTITION": "aws",
                "MCP_USER_AGENT": "Chrome/131.0.0.0"
            }
        }
    }
    mcp_client = MultiServerMCPClient(mcp_servers_config)

    tools = await mcp_client.get_tools()
    if not tools:
        print("No tools discovered from the MCP server. Exiting.")
        return

    print(f"Discovered tools: {[tool.name for tool in tools]}")
    

if __name__ == "__main__":
    # Run the main asynchronous function
    import asyncio
    asyncio.run(main())
