# test_fastmcp.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Test")
print(dir(mcp.run))  # Inspect available attributes
help(mcp.run)  # Print method documentation