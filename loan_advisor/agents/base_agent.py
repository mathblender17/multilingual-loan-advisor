from abc import ABC, abstractmethod
from typing import Dict, Any
import json
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "mixtral-8x7b-32768"  # Groq's Mixtral model

# Storage Configuration
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
USER_DATA_FILE = DATA_DIR / "user_data.json"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Define a mock LLM for testing
class MockLLM:
    def __init__(self, **kwargs):
        self.temperature = kwargs.get('temperature', 0.7)
        print(f"MockLLM initialized with temperature={self.temperature}")
    
    def invoke(self, messages):
        # Simple mock response
        content = "This is a mock response for testing purposes only."
        return type('obj', (object,), {'content': content})

class BaseAgent(ABC):
    def __init__(self):
        self.conversation_history = []
        self.user_data = self.load_user_data()
        
        # Try to import langchain_groq, fall back to mock if not available
        try:
            from langchain_groq import ChatGroq
            from langchain.schema import HumanMessage, SystemMessage
            self.HumanMessage = HumanMessage
            self.SystemMessage = SystemMessage
            
            self.llm = ChatGroq(
                groq_api_key=GROQ_API_KEY or "dummy_key_for_testing",
                model_name=LLM_MODEL,
                temperature=0.7,
                max_tokens=1024
            )
            print("Using real ChatGroq LLM")
        except ImportError:
            # Use mock LLM if langchain_groq is not available
            self.llm = MockLLM(temperature=0.7)
            
            # Mock message classes
            self.HumanMessage = lambda content: type('obj', (object,), {'content': content})
            self.SystemMessage = lambda content: type('obj', (object,), {'content': content})
            print("Using MockLLM - langchain_groq not available")

    @abstractmethod
    def process_message(self, message: str) -> str:
        """Process the user message and return a response."""
        pass

    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_completion(self, messages: list, temperature: float = 0.7) -> str:
        """Get completion from Groq API using Langchain."""
        try:
            # Convert messages to Langchain format
            langchain_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    langchain_messages.append(self.SystemMessage(content=msg["content"]))
                else:
                    langchain_messages.append(self.HumanMessage(content=msg["content"]))

            # Override temperature if different from default
            if temperature != 0.7:
                self.llm.temperature = temperature

            # Get response
            response = self.llm.invoke(langchain_messages)
            
            # Reset temperature to default if it was changed
            if temperature != 0.7:
                self.llm.temperature = 0.7

            return response.content
        except Exception as e:
            print(f"Error getting completion: {str(e)}")
            return f"I'm currently having trouble accessing my knowledge base. Can you try a simpler question or try again later? (Error: {str(e)})"

    def load_user_data(self) -> Dict[str, Any]:
        """Load user data from JSON file."""
        if Path(USER_DATA_FILE).exists():
            with open(USER_DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    def save_user_data(self):
        """Save user data to JSON file."""
        try:
            with open(USER_DATA_FILE, 'w') as f:
                json.dump(self.user_data, f, indent=4)
        except Exception as e:
            print(f"Warning: Could not save user data: {str(e)}")

    def update_user_data(self, user_id: str, data: Dict[str, Any]):
        """Update user data for a specific user."""
        if user_id not in self.user_data:
            self.user_data[user_id] = {}
        self.user_data[user_id].update(data)
        self.save_user_data() 