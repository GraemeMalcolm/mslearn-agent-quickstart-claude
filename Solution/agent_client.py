"""
Agent Client - Handles interaction with the Claude-based computing historian agent.

This module contains the core logic for the agent. It uses the Anthropic SDK
to call the Claude Messages API, running an agent loop that submits prompts
(with conversation history), lets Claude use the web search tool, and returns
the final response.
"""

import os
import base64
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import the Anthropic client library
from anthropic import Anthropic

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# Define the agent's instructions (system prompt) and tools
SYSTEM_PROMPT = (
    "You are an expert in the history of computing and AI. "
    "You only answer questions about significant people and events in the development "
    "of computing, and about notable vintage computers. "
    "Do not engage in conversations on any topic that is unrelated to computing history."
)

TOOLS = [
    {"type": "web_search_20260209", "name": "web_search", "max_uses": 5}
]


class AgentClient:
    """Client for interacting with the computing historian agent."""

    def __init__(self):
        """Initialize the agent client with authentication and model."""
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-opus-5-5")

        # Create the Anthropic client
        self.client = Anthropic()

        # Maintain conversation history (last 3 exchanges)
        self.conversation_history: List[Dict[str, Any]] = []
        self.max_history = 3

        # Safety limit on the number of model calls in a single agent loop
        self.max_turns = 5

    def send_message(self, user_message: str, image_data: bytes = None,
                     image_media_type: str = None) -> str:
        """
        Send a message to the agent and return the response.

        Args:
            user_message: The text message from the user
            image_data: Optional raw bytes of an image to submit with the message
            image_media_type: The media type of the image (for example, "image/png")

        Returns:
            The agent's response text
        """
        # Build the user message content - text only, or an image block followed by a text block
        content: Any = user_message
        if image_data:
            content = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": base64.standard_b64encode(image_data).decode("utf-8")
                    }
                },
                {"type": "text", "text": user_message}
            ]
        
        # Add current user message to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": content
        })

        try:
            # Initialize assistant message variable
            assistant_message = ""



            # Run the agent loop
            messages = list(self.conversation_history)
            for _ in range(self.max_turns):
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=16000,
                    system=SYSTEM_PROMPT,
                    tools=TOOLS,
                    messages=messages
                )

                # If Claude paused while using a server-side tool, send its progress back so it can continue
                if response.stop_reason == "pause_turn":
                    messages.append({"role": "assistant", "content": response.content})
                    continue

                # Otherwise, Claude has finished
                break

            # The response contains multiple content blocks (for example, web searches and results);
            # the text blocks make up the answer
            assistant_message = "".join(
                block.text for block in response.content if block.type == "text"
            )

            if response.stop_reason == "refusal":
                assistant_message = "I'm unable to help with that request."

            # Add assistant response to conversationhistory
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            # Count user messages in history to enforce max_history limit
            user_message_count = sum(1 for msg in self.conversation_history
                                    if isinstance(msg, dict) and msg.get("role") == "user")

            # Remove oldest exchanges if we have more than max_history
            while user_message_count > self.max_history:
                # Find and remove the first user message and its assistant response
                for i, msg in enumerate(self.conversation_history):
                    if isinstance(msg, dict) and msg.get("role") == "user":
                        self.conversation_history.pop(i)
                        if i < len(self.conversation_history) and self.conversation_history[i].get("role") == "assistant":
                            self.conversation_history.pop(i)
                        user_message_count -= 1
                        break

            return assistant_message

        except Exception as e:
            logger.exception("Error communicating with agent")
            return "An internal error occurred while communicating with the agent."

    def reset_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
