import asyncio
from typing import Any, Dict, Optional, List # Added List for StdioServerParameters.args

# Imports for MCP library
try:
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client, StdioServerParameters
except ImportError:
    print("MCP library not found or incomplete. MCPToolWrapper will use dummy classes. Please install 'mcp'.")
    # Define dummy classes if mcp is not found, so the rest of the app can load.
    class ClientSession: # type: ignore
        async def initialize(self): pass
        async def call_tool(self, tool_name: str, arguments: Dict[str, Any]): pass

    class StdioServerParameters: # type: ignore
        def __init__(self, command: str, args: List[str], env: Optional[Dict[str, str]] = None, cwd: Optional[str] = None):
            self.command = command
            self.args = args
            self.env = env
            self.cwd = cwd

    class stdio_client: # type: ignore
        def __init__(self, server_params: StdioServerParameters):
            self.server_params = server_params
            print(f"Dummy stdio_client initialized with command: {server_params.command} {' '.join(server_params.args)}")

        async def __aenter__(self):
            print("Dummy stdio_client.__aenter__ called. Returning dummy streams.")
            # Simulate a simple echo behavior for dummy streams if possible, or just placeholders
            async def dummy_read_stream():
                # This would normally yield MCP messages
                yield {"type": "tool_response", "tool_name": "dummy_tool", "payload": {"response": "dummy_echo"}}

            async def dummy_write_stream(message: Dict[str, Any]):
                # This would normally send MCP messages
                pass

            return dummy_read_stream(), dummy_write_stream

        async def __aexit__(self, exc_type, exc, tb):
            print("Dummy stdio_client.__aexit__ called.")
            pass


class MCPClientManager:
    """Manages MCP ClientSession objects and their underlying transports (stdio processes)."""

    def __init__(self):
        self._sessions: Dict[str, ClientSession] = {}
        # For stdio, transport_ctx_manager is the stdio_client instance itself.
        self._transports: Dict[str, Any] = {}
        self._locks: Dict[str, asyncio.Lock] = {}
        print("MCPClientManager initialized for STDIN/STDOUT communication.")

    async def get_session(self, server_command: str) -> ClientSession:
        """
        Gets an existing MCP ClientSession for the given server_command or creates a new one.
        server_command: The command to execute the stdio server (e.g., "python echo_mcp_server.py").
        """
        lock_key = server_command # Use the command as the key for the lock and session

        if lock_key not in self._locks:
            self._locks[lock_key] = asyncio.Lock()

        async with self._locks[lock_key]:
            if lock_key in self._sessions:
                print(f"Returning existing MCP session for command: {server_command}")
                return self._sessions[lock_key]

            print(f"Creating new MCP session for command: {server_command}...")
            transport_ctx_manager = None
            try:
                command_parts = server_command.split()
                executable = command_parts[0]
                args = command_parts[1:]

                server_params = StdioServerParameters(
                    command=executable,
                    args=args
                )
                print(f"MCPClientManager: Configured StdioServerParameters for command: {server_command}")

                transport_ctx_manager = stdio_client(server_params)
                print(f"MCPClientManager: stdio_client created. Calling __aenter__ for {server_command}...")

                # stdio_client context manager yields (read_stream, write_stream) directly.
                read_stream, write_stream = await transport_ctx_manager.__aenter__()
                print(f"MCPClientManager: stdio_client __aenter__ completed for {server_command}.")

                print(f"MCPClientManager: Instantiating ClientSession for {server_command}")
                session = ClientSession(read_stream, write_stream)
                print(f"MCPClientManager: ClientSession instantiated. Initializing session for {server_command}")
                await session.initialize()
                print(f"MCPClientManager: Session initialized for {server_command}")

                self._sessions[lock_key] = session
                self._transports[lock_key] = transport_ctx_manager # Store the client instance itself for __aexit__
                print(f"MCP session for command '{server_command}' created and initialized.")
                return session
            except Exception as e:
                print(f"Error creating MCP session for command '{server_command}': {e}")
                if transport_ctx_manager and hasattr(transport_ctx_manager, '__aexit__'):
                    try:
                        await transport_ctx_manager.__aexit__(type(e), e, e.__traceback__)
                    except Exception as close_e:
                        print(f"Error closing stdio_client during session creation failure for '{server_command}': {close_e}")
                if lock_key in self._sessions:
                     del self._sessions[lock_key]
                if lock_key in self._transports:
                    del self._transports[lock_key]
                raise

    async def close_all_sessions(self):
        """Closes all active MCP sessions by terminating their stdio server processes."""
        print("Closing all MCP sessions (stdio transports)...")
        for server_command, transport_cm in list(self._transports.items()):
            try:
                print(f"Closing MCP stdio transport for command: {server_command}...")
                await transport_cm.__aexit__(None, None, None)
                print(f"MCP stdio transport for command: {server_command} closed.")
            except Exception as e:
                print(f"Error closing MCP stdio transport for command '{server_command}': {e}")

        self._sessions.clear()
        self._transports.clear()
        self._locks.clear()
        print("All MCP sessions and stdio transports cleared.")


class MCPToolWrapper:
    """
    A wrapper that makes an MCP tool look like a standard callable async tool/function.
    The 'server_url' parameter is now interpreted as the command to run the stdio server.
    """
    def __init__(self, mcp_client_manager: MCPClientManager,
                 server_command: str, # Changed from server_url
                 tool_name: str,
                 tool_description: str = ""):
        if mcp_client_manager is None:
            raise ValueError("MCPClientManager instance is required.")
        self.mcp_client_manager = mcp_client_manager
        self.server_command = server_command # Changed from server_url
        self.tool_name = tool_name
        self.tool_description = tool_description
        self.__name__ = tool_name

    async def __call__(self, **kwargs: Any) -> Any:
        """
        Executes the MCP tool by its name with the given arguments via stdio.
        """
        print(f"MCPToolWrapper: Attempting to call tool '{self.tool_name}' via server command '{self.server_command}' with args: {kwargs}")
        try:
            session = await self.mcp_client_manager.get_session(self.server_command)
            result = await session.call_tool(tool_name=self.tool_name, arguments=kwargs)
            print(f"MCPToolWrapper: Tool '{self.tool_name}' call successful. Result: {str(result)[:100]}...")
            return result
        except ImportError as e:
            print(f"MCPToolWrapper: ImportError, MCP library might not be installed. Error: {e}")
            raise
        except Exception as e:
            print(f"MCPToolWrapper: Error calling tool '{self.tool_name}' via '{self.server_command}': {e}")
            raise

    @property
    def __doc__(self) -> str:
        return self.tool_description if self.tool_description else f"MCP tool (stdio): {self.tool_name}"

# Example Usage (for testing purposes, can be commented out)
async def main_test():
    print("Testing MCP STDIN/STDOUT Integration (requires MCP library and echo_mcp_server.py)")

    if ClientSession.__module__ == __name__: # Check if using dummy ClientSession
        print("Using dummy MCP classes, full test won't run effectively.")
        manager = MCPClientManager()
        # Test with a system command like "echo" if echo_mcp_server.py isn't runnable or too complex for dummy
        # For a true dummy test, we need a command that produces predictable output or just test instantiation.
        # This example assumes 'python echo_mcp_server.py' would be the command.
        test_command = "python echo_mcp_server_placeholder.py" # Placeholder, real server might not run
        tool = MCPToolWrapper(manager, test_command, "dummy_echo_tool", "A dummy echo tool via stdio.")
        print(f"Tool name: {tool.__name__}, Doc: {tool.__doc__}")

        # This call would use the dummy stdio_client if mcp is not installed.
        try:
            response = await tool(message="hello dummy stdio")
            print(f"Dummy tool call response: {response}")
        except Exception as e:
            print(f"Dummy tool call failed as expected or due to setup: {e}")

        await manager.close_all_sessions()
        return

    # Actual test logic (requires real MCP setup and echo_mcp_server.py)
    # manager = MCPClientManager()
    # try:
    #     server_cmd = "python echo_mcp_server.py" # Command to run the stdio echo server
    #     test_tool = MCPToolWrapper(manager, server_cmd, "echo_tool",
    #                                "Echoes a message using the stdio MCP echo server.")

    #     print(f"Calling tool: {test_tool.__name__} via command: {server_cmd}")
    #     response = await test_tool(message="Hello MCP STDIN/STDOUT World")
    #     print(f"Response from '{test_tool.__name__}': {response}")

    # except Exception as e:
    #     print(f"Error during MCP STDIN/STDOUT tool test: {e}")
    # finally:
    #     await manager.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main_test())
