#!/usr/bin/env python3
"""
Poe API Client

This module provides a client for accessing the Poe API using fastapi_poe.
It supports both synchronous and asynchronous methods for getting bot responses.
"""

import os
import asyncio
from typing import List, AsyncGenerator, Generator, Optional
import fastapi_poe as fp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class PoeClient:
    """Client for interacting with the Poe API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Poe client.
        
        Args:
            api_key: The Poe API key. If not provided, it will be loaded from the POE_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("POE_API_KEY")
        if not self.api_key:
            raise ValueError("API key not provided and POE_API_KEY environment variable not set")
    
    def get_response_sync(
        self, 
        messages: List[fp.ProtocolMessage], 
        bot_name: str = "GPT-3.5-Turbo"
    ) -> Generator[str, None, None]:
        """
        Get a bot response synchronously.
        
        Args:
            messages: List of protocol messages to send to the bot.
            bot_name: Name of the bot to query.
            
        Returns:
            Generator yielding response chunks.
        """
        for partial in fp.get_bot_response_sync(
            messages=messages,
            bot_name=bot_name,
            api_key=self.api_key
        ):
            yield partial
    
    async def get_response(
        self, 
        messages: List[dict], 
        bot_name: str = "GPT-3.5-Turbo"
    ) -> AsyncGenerator[str, None]:
        """
        Get a bot response asynchronously.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            bot_name: Name of the bot to query.
            
        Returns:
            AsyncGenerator yielding response chunks.
        """
        protocol_messages = [
            fp.ProtocolMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]
        
        async for partial in fp.get_bot_response(
            messages=protocol_messages,
            bot_name=bot_name,
            api_key=self.api_key
        ):
            yield partial.text

    def send_message_sync(self, content: str, bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a message to a bot and get the full response synchronously.
        
        Args:
            content: The message content.
            bot_name: Name of the bot to query.
            
        Returns:
            The complete response as a string.
        """
        message = fp.ProtocolMessage(role="user", content=content)
        response_parts = []
        for partial in self.get_response_sync(messages=[message], bot_name=bot_name):
            response_parts.append(partial)
        return "".join(response_parts)
    
    async def send_message(self, content: str, bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a message to a bot and get the full response asynchronously.
        
        Args:
            content: The message content.
            bot_name: Name of the bot to query.
            
        Returns:
            The complete response as a string.
        """
        messages = [{"role": "user", "content": content}]
        response_parts = []
        async for partial_text in self.get_response(messages=messages, bot_name=bot_name):
            response_parts.append(partial_text)
        full_response = "".join(response_parts)
        # Ensure we're returning a string
        if not isinstance(full_response, str):
            raise TypeError(f"Expected string response, got {type(full_response)}")
        return full_response
    
    def send_conversation_sync(self, messages: List[dict], bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a conversation to a bot and get the full response synchronously.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            bot_name: Name of the bot to query.
            
        Returns:
            The complete response as a string.
        """
        protocol_messages = [
            fp.ProtocolMessage(role=msg["role"], content=msg["content"])
            for msg in messages
        ]
        response_parts = []
        for partial in self.get_response_sync(messages=protocol_messages, bot_name=bot_name):
            response_parts.append(partial)
        return "".join(response_parts)
    
    async def send_conversation(self, messages: List[dict], bot_name: str = "GPT-3.5-Turbo") -> str:
        """
        Send a conversation to a bot and get the full response asynchronously.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            bot_name: Name of the bot to query.
            
        Returns:
            The complete response as a string.
        """
        response_parts = []
        async for partial in self.get_response(messages=messages, bot_name=bot_name):
            response_parts.append(partial)
        return "".join(response_parts)