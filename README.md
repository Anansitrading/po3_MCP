# Poe o3 MCP Server

A lightweight Model Context Protocol (MCP) server implementation that provides access to OpenAI's o3 model and other models via Poe's API. This server allows you to integrate Poe's AI capabilities into any MCP-compatible application.

## Features

- Simple MCP server implementation using FastMCP
- Direct integration with Poe's API to access the o3 model and other models
- Model selection via command-line style flags in prompts
- Asynchronous request handling for efficient processing
- Comprehensive error handling and logging
- Easy setup and configuration

## Prerequisites

- Python 3.8+
- A Poe API key (obtainable from [https://poe.com/api_key](https://poe.com/api_key))

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Anansitrading/po3_MCP.git
   cd po3_MCP
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   ```bash
   cp sample.env .env
   ```
   
5. Edit the `.env` file and add your Poe API key:
   ```
   POE_API_KEY=your_poe_api_key_here
   ```

## Usage

### Running the MCP Server

Run the server with:

```bash
python poe_o3_mcp_server.py
```

The server will start and listen for MCP protocol messages on standard input/output.

### Model Selection via Flags

You can select different models available on Poe by adding a flag to your prompt:

```
--Claude-3.5-Sonnet Tell me about quantum computing
```

This will route your query to the Claude-3.5-Sonnet model instead of the default o3 model.

The flag can be placed anywhere in the message:
- At the beginning: `--GPT-4 What is the capital of France?`
- In the middle: `Tell me --Claude-3-Opus about the history of Rome`
- At the end: `What are the three laws of robotics? --Claude-3.5-Sonnet`

The flag will be automatically removed from the message before it's sent to the model.

If no flag is specified, the server defaults to using the "o3" model.

### Integrating with MCP Clients

This server provides two tools:

1. `o3_query` - Send a query to the o3 model (or another model via flags) and get a response
2. `ping` - A simple test tool that returns "pong"

Example of using the server with an MCP client:

```python
from mcp.client import MCPClient

# Connect to the MCP server
client = MCPClient(server_command=["python", "path/to/poe_o3_mcp_server.py"])

# Call the o3_query tool with the default o3 model
response = client.call_tool("o3_query", {"message": "Tell me about quantum computing"})
print(response)

# Call the o3_query tool with a different model using a flag
response = client.call_tool("o3_query", {"message": "--Claude-3.5-Sonnet Tell me about quantum computing"})
print(response)

# Test the connection with ping
ping_response = client.call_tool("ping", {})
print(ping_response)  # Should print "pong"
```

You can also run the included example script:

```bash
python example.py
```

## Configuration

The server uses the following environment variables:

- `POE_API_KEY`: Your Poe API key (required)
- `LOG_LEVEL`: Logging level (optional, defaults to DEBUG)

## Troubleshooting

If you encounter issues:

1. Check that your Poe API key is valid and correctly set in the `.env` file
2. Ensure you have the correct dependencies installed
3. Check the server logs for detailed error messages
4. Verify that you have an active internet connection
5. If using a model flag, make sure the model name is correct and available on Poe

## License

MIT

## Acknowledgements

- [Model Context Protocol](https://github.com/anthropics/model-context-protocol)
- [FastMCP](https://github.com/anthropics/fastmcp)
- [Poe API](https://poe.com/api_docs)