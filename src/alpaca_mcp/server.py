"""Alpaca MCP Server Module

This module implements the MCP server for the Alpaca API.
"""

from typing import Any, List, Dict, Optional, Union
import asyncio
import os
from datetime import datetime
import dotenv

from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.timeframe import TimeFrame

# Import functions from tools.py
from .tools import (
    get_crypto_client,
    format_crypto_bars,
    parse_timeframe
)

# Load environment variables from .env file if it exists
dotenv.load_dotenv()

# Initialize the server
server = Server("alpaca_crypto")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """
    List available tools.
    Each tool specifies its arguments using JSON Schema validation.
    """
    return [
        types.Tool(
            name="get-crypto-bars",
            description="Get historical bar/candle data for cryptocurrencies",
            inputSchema={
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "Cryptocurrency symbol (e.g., BTC/USD, ETH/USD)",
                    },
                    "timeframe": {
                        "type": "string",
                        "description": "Timeframe for bars (e.g., 1Day, 1Hour, 1Min)",
                        "default": "1Day"
                    },
                    "start": {
                        "type": "string",
                        "description": "Start date in YYYY-MM-DD format",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of bars to return",
                        "default": 10
                    },
                },
                "required": ["symbol", "start"],
            },
        ),
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """
    Handle tool execution requests.
    Tools can fetch crypto data and notify clients of changes.
    """
    if not arguments:
        return [types.TextContent(type="text", text="Missing arguments for the request")]

    if name == "get-crypto-bars":
        symbol = arguments.get("symbol")
        timeframe_str = arguments.get("timeframe", "1Day")
        start_date = arguments.get("start")
        limit = arguments.get("limit", 10)
        
        if not symbol:
            return [types.TextContent(type="text", text="Missing symbol parameter")]
            
        if not start_date:
            return [types.TextContent(type="text", text="Missing start parameter")]

        # Parse start date
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError:
            return [types.TextContent(
                type="text", 
                text="Invalid start date format. Please use YYYY-MM-DD format.")
            ]

        # Parse timeframe
        timeframe = parse_timeframe(timeframe_str)

        try:
            # Get client
            client = get_crypto_client()
            
            # Create request parameters
            request_params = CryptoBarsRequest(
                symbol_or_symbols=symbol,
                timeframe=timeframe,
                start=start_date
            )
            
            # Get bars data
            bars = client.get_crypto_bars(request_params)
            
            # Format the response
            formatted_bars = format_crypto_bars(bars, symbol, limit)
            bars_text = f"Cryptocurrency bars for {symbol} ({timeframe_str}):\n\n{formatted_bars}"
            
            return [types.TextContent(type="text", text=bars_text)]
            
        except Exception as e:
            error_text = f"Error fetching crypto bars: {str(e)}"
            return [types.TextContent(type="text", text=error_text)]
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main function to run the server."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="alpaca_crypto",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

# This is needed if you'd like to connect to a custom client
if __name__ == "__main__":
    asyncio.run(main())
