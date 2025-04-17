# Alpaca MCP Server

A Model Context Protocol (MCP) server that provides real-time access to cryptocurrency market data through the [Alpaca API](https://docs.alpaca.markets/). This server implements a standardized interface for retrieving cryptocurrency data.

## Features

- Daily, weekly, and monthly cryptocurrency time series data
- Latest crypto exchange rates
- Historical bar/candle data
- Built-in error handling and rate limit management

## Installation

### Using Claude Desktop

#### Installing via Docker

- Clone the repository and build a local image to be utilized by your Claude desktop client

```sh
cd alpaca-mcp
docker build -t mcp/alpaca .
```

- Change your `claude_desktop_config.json` to match the following, replacing `REPLACE_API_KEY` and `REPLACE_API_SECRET` with your actual keys:

 > `claude_desktop_config.json` path
 >
 > - On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
 > - On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "alpaca": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "-e",
        "ALPACA_API_KEY",
        "-e",
        "ALPACA_API_SECRET",
        "mcp/alpaca"
      ],
      "env": {
        "ALPACA_API_KEY": "REPLACE_API_KEY",
        "ALPACA_API_SECRET": "REPLACE_API_SECRET"
      }
    }
  }
}
```

#### Development Setup

```bash
# Clone the repository
git clone https://github.com/berlinbra/alpaca-mcp.git
cd alpaca-mcp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .
```

## Available Tools

Currently, the server implements the following tool:

- `get-crypto-bars`: Get historical bar/candle data for cryptocurrencies

More tools will be added in the future.

### get-crypto-bars

**Input Schema:**
```json
{
    "symbol": {
        "type": "string",
        "description": "Cryptocurrency symbol (e.g., BTC/USD, ETH/USD)"
    },
    "timeframe": {
        "type": "string",
        "description": "Timeframe for bars (e.g., 1Day, 1Hour, 1Min)",
        "default": "1Day"
    },
    "start": {
        "type": "string",
        "description": "Start date in YYYY-MM-DD format"
    },
    "limit": {
        "type": "integer",
        "description": "Maximum number of bars to return",
        "default": 10
    }
}
```

**Example Response:**
```
Cryptocurrency bars for BTC/USD (1Day):

Date: 2025-04-10
Open: $68750.12
High: $69200.45
Low: $67900.78
Close: $68900.32
Volume: 12345.67
---
Date: 2025-04-11
Open: $68900.32
High: $70100.55
Low: $68400.21
Close: $69800.44
Volume: 15678.90
```

## Error Handling

The server includes comprehensive error handling for various scenarios:

- Rate limit exceeded
- Invalid API key
- Network connectivity issues
- Timeout handling
- Malformed responses

Error messages are returned in a clear, human-readable format.

## Prerequisites

- Python 3.12 or higher
- httpx
- mcp
- alpaca-py

## License
This MCP server is licensed under the MIT License.
