from mcp.server.fastmcp import FastMCP
# import uvicorn # No longer needed for stdio

# MCP_SERVER_PORT = 8079 # Not used for stdio
# MCP_SERVER_HOST = "localhost" # Not used for stdio

mcp_server = FastMCP(name="EchoMCPServer", stateless_http=False) # stateless_http might not be relevant for stdio

@mcp_server.tool(description="A simple echo tool via MCP")
def echo_tool(message: str) -> str:
    # For stdio, server-side prints might interfere with message packing if not careful.
    # Best to use logging for debugging in a real stdio server.
    # For this test, this print might go to stderr or be handled by MCP library.
    print(f"EchoMCPServer: echo_tool was called with message: '{message}'", flush=True) # flush to ensure it's seen
    return f"Echo from MCP STDIN/STDOUT Server: {message}"

if __name__ == "__main__":
    print("Starting Echo MCP Server on STDIN/STDOUT.", flush=True)

    try:
        # Attempt to run FastMCP with stdio transport directly
        # This is the most straightforward way if supported by the library version (mcp 1.9.3)
        mcp_server.run(transport="stdio")
        print("Echo MCP Server on STDIN/STDOUT finished.", flush=True)
    except TypeError as te:
        print(f"Running FastMCP with mcp_server.run(transport='stdio') failed: {te}", flush=True)
        print("This version of FastMCP may not support 'transport' keyword in run(), or 'stdio' is not a recognized value.", flush=True)
        print("Alternative methods for running FastMCP over stdio (e.g., using mcp.server.stdio.stdio_server with a low-level server run) would be more complex and require specific SDK knowledge.", flush=True)
        print("For this subtask, we are relying on run(transport='stdio'). If this fails, manual SDK consultation is needed.", flush=True)
    except Exception as e:
        print(f"An unexpected error occurred while trying to run MCP server on STDIN/STDOUT: {e}", flush=True)
        import traceback
        traceback.print_exc()

    # Note: If mcp_server.run(transport="stdio") is blocking and runs indefinitely (as a server should),
    # code here will only execute after the server stops.
    # If it's non-blocking or fails, the script might terminate quickly.
    # The `flush=True` is added to prints to ensure they are seen immediately,
    # especially if stdout is being redirected or if the process exits abruptly.
