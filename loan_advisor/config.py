from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LLM_MODEL = "mixtral-8x7b-32768"  # Groq's Mixtral model

# Storage Configuration
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
USER_DATA_FILE = DATA_DIR / "user_data.json"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Loan Types
LOAN_TYPES = ["business", "home", "personal", "education", "vehicle"]

# Minimum Credit Score Requirements
MIN_CREDIT_SCORES = {
    "business": 700,
    "home": 650,
    "personal": 600,
    "education": 650,
    "vehicle": 600
}

# Minimum Income Requirements (Monthly in INR)
MIN_INCOME = {
    "business": 50000,
    "home": 40000,
    "personal": 25000,
    "education": 30000,
    "vehicle": 25000
} 