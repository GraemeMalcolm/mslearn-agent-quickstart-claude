"""
Agent Client - Handles interaction with the managed Computing History agent.

This module contains the core logic for the client. The agent itself (model,
instructions, and tools) is defined and hosted in the Claude Platform as a
*managed agent*. This client starts a *session* with that agent, sends the
user's messages to the session as events, and streams the agent's response
events back. Anthropic runs the agent loop and keeps the conversation state,
so the client doesn't need to track history or run a tool loop.
"""

import os
import logging
from dotenv import load_dotenv

# Import the Anthropic client library


# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class AgentClient:
    """Client for interacting with the managed computing historian agent."""

    def __init__(self):
        """Initialize the agent client with authentication and agent details."""
        if not os.getenv("ANTHROPIC_API_KEY"):
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.agent_id = os.getenv("AGENT_ID")
        self.environment_id = os.getenv("ENVIRONMENT_ID")
        if not self.agent_id or not self.environment_id:
            raise ValueError("AGENT_ID and ENVIRONMENT_ID must be set in the .env file")

        # Create the Anthropic client


        # Start a session with the managed agent
        self.session_id = None
        self._start_session()

    def _start_session(self):
        """Create a new session; the session holds the conversation state."""
        # Create a session that uses the managed agent and environment


    def send_message(self, user_message: str) -> str:
        """
        Send a message to the agent and return the response.

        Args:
            user_message: The text message from the user

        Returns:
            The agent's response text
        """
        try:
            # Initialize assistant message variable
            assistant_message = ""

            # Stream events from the session, send the user's message, and collect the response


            return assistant_message.strip() or "The agent didn't return a response."

        except Exception as e:
            logger.exception("Error communicating with agent")
            return "An internal error occurred while communicating with the agent."

    def reset_conversation(self):
        """Start a new session, discarding the previous conversation."""
        self._start_session()
