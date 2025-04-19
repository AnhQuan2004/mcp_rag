from mcp.client.mcpclient import MCPClient

# Initialize client connecting to the MCP server
client = MCPClient(
    transport_config={
        "type": "sse",
        "url": "http://localhost:8000/sse"
    }
)

# Call the search_doc_for_rag_context tool to find information about "phase 1"
response = client.call_tool(
    tool_name="search_doc_for_rag_context",
    query="what is phase 1 in paper"
)

# Print the response
print(response) 