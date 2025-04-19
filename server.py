from mcp.server.fastmcp import FastMCP
import os
from dotenv import load_dotenv
from groundx import GroundX, Document
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastMCP with server name "eyelevel-rag"
# For SSE transport we need to specify init_server=True to properly initialize 
mcp = FastMCP(
    name="eyelevel-rag",
    init_server=True
)

client = GroundX(api_key=os.getenv("GROUNDX_API_KEY"))

@mcp.tool()
def search_doc_for_rag_context(query: str) -> str:
    """
    Searches and retrieves relevant context from a knowledge base,
    based on the user's query.
    Args:
        query: The search query supplied by the user.
    Returns:
        str: Relevant text content that can be used by the LLM to answer the query.
    """
    response = client.search.content(
        id=17933,
        query=query,
        n=10,
    )

    return response.search.text

@mcp.tool()
def ingest_documents(local_file_path: str) -> str:
    """
    Ingest documents from a local file into the knowledge base.
    Args:
        local_file_path: The path to the local file containing the documents to ingest.
    Returns:
        str: A message indicating the documents have been ingested.
    """
    file_name = os.path.basename(local_file_path)
    client.ingest(
        documents=[
            Document(
            bucket_id=17279,
            file_name=file_name,
            file_path=local_file_path,
            file_type="pdf",
            search_data=dict(
                key = "value",
            ),
            )
        ]
    )
    return f"""Ingested {file_name} into the knowledge base. 
               It should be available in a few minutes"""

if __name__ == "__main__":
    # Start the server with SSE transport
    print("Starting MCP server with SSE transport on port 8000...")
    mcp.run(transport='sse')
