"""Alpaca MCP Tools Module

This module contains utility functions for making requests to the Alpaca API
and formatting the responses.
"""

from typing import Any, Dict, Optional, List, Union
import httpx
import os
from datetime import datetime
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

# Get API keys from environment variables
API_KEY = os.getenv('ALPACA_API_KEY')
API_SECRET = os.getenv('ALPACA_API_SECRET')

# Initialize clients
def get_crypto_client() -> CryptoHistoricalDataClient:
    """Get a crypto historical data client.
    
    If API credentials are provided, use them for higher rate limits.
    Otherwise, create a client without credentials (still works for crypto).
    
    Returns:
        A CryptoHistoricalDataClient instance
    """
    if API_KEY and API_SECRET:
        return CryptoHistoricalDataClient(API_KEY, API_SECRET)
    return CryptoHistoricalDataClient()


def format_crypto_bars(bars_data: Dict[str, Any], symbol: str, limit: int = 10) -> str:
    """Format crypto bars data into a concise string.
    
    Args:
        bars_data: The response data from the Alpaca CryptoBarsRequest
        symbol: The cryptocurrency symbol
        limit: Maximum number of bars to display (default: 10)
        
    Returns:
        A formatted string containing the cryptocurrency bars information
    """
    try:
        if not bars_data or not isinstance(bars_data, dict) or symbol not in bars_data:
            return "No bars data available in the response"

        bars = bars_data[symbol]
        if not bars:
            return f"No data available for {symbol}"
        
        # Limit the number of bars to display
        bars_to_display = bars[:limit] if len(bars) > limit else bars
        
        formatted_data = []
        
        for bar in bars_to_display:
            bar_date = bar.timestamp.strftime("%Y-%m-%d")
            formatted_data.append(
                f"Date: {bar_date}\n"
                f"Open: ${bar.open:.2f}\n"
                f"High: ${bar.high:.2f}\n"
                f"Low: ${bar.low:.2f}\n"
                f"Close: ${bar.close:.2f}\n"
                f"Volume: {bar.volume:.2f}\n"
                "---\n"
            )
        
        if len(bars) > limit:
            formatted_data.append(f"\n... and {len(bars) - limit} more bars")
            
        return "".join(formatted_data)
    except Exception as e:
        return f"Error formatting bars data: {str(e)}"


def parse_timeframe(timeframe_str: str) -> TimeFrame:
    """Parse a timeframe string into a TimeFrame enum.
    
    Args:
        timeframe_str: String representation of the timeframe
        
    Returns:
        The corresponding TimeFrame enum value
    """
    timeframe_map = {
        "1Min": TimeFrame.Minute,
        "5Min": TimeFrame.Minute,
        "15Min": TimeFrame.Minute,
        "30Min": TimeFrame.Minute,
        "1Hour": TimeFrame.Hour,
        "1Day": TimeFrame.Day,
        "1Week": TimeFrame.Week,
        "1Month": TimeFrame.Month
    }
    
    if timeframe_str in timeframe_map:
        return timeframe_map[timeframe_str]
    else:
        # Default to daily timeframe if not recognized
        return TimeFrame.Day
