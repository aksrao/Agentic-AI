import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            format_response(tools)

            result = await session.call_tool(
                "aws_docs_search",
                {"query": "EC2 pricing"}
            )
            # print(result)

def format_response(parsed):
    return f"""
    💡**Summary**
    {parsed['summary']}

    📌 **Key Points**
    {chr(10).join([f"- {p}" for p in parsed['key_points']])}

    🚀 **Recommendations**
    {chr(10).join([f"- {r}" for r in parsed.get('recommendations', [])])}

    📚 **Source**
    {parsed.get('source', 'AWS Documentation')}
    """
asyncio.run(main())