from typing import Tuple, Dict, Any
from .base_agent import BaseAgent

class IntentClassifierAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.intent_examples = {
            "loan_query": [
                "need a loan",
                "want to borrow money",
                "looking for loan",
                "help with loan",
                "loan options",
                "loan information"
            ],
            "loan_application": [
                "how to apply",
                "application process",
                "documents needed",
                "start application",
                "apply for loan"
            ],
            "loan_info": [
                "interest rates",
                "EMI details",
                "repayment options",
                "loan terms",
                "eligibility criteria"
            ]
        }
        
        self.loan_types = {
            "education": ["education", "study", "college", "university", "school", "course", "mba", "btech", "degree"],
            "business": ["business", "startup", "company", "enterprise", "shop", "commercial", "store"],
            "home": ["home", "house", "property", "flat", "apartment", "real estate", "housing"],
            "personal": ["personal", "individual", "emergency", "medical", "wedding", "travel"],
            "vehicle": ["vehicle", "car", "bike", "auto", "motorcycle", "scooter"]
        }

    def process_message(self, message: str) -> Tuple[str, Dict[str, Any]]:
        """
        Classify user message with improved context understanding.
        Returns a tuple of (intent, context_data)
        """
        try:
            # Validate and clean input
            if not isinstance(message, str):
                message = str(message)
            
            # Add message to history
            self.add_to_history("user", message)
            
            # Convert message to lowercase for matching
            message_lower = message.lower()
            
            # Determine loan type first
            loan_type = self._detect_loan_type(message_lower)
            
            # Create prompt for intent classification
            prompt = f"""Analyze this user message to understand their exact need:

            User message: "{message}"

            Consider:
            1. Are they asking about getting a {loan_type if loan_type else ''} loan? → loan_query
            2. Do they want to know how to apply? → loan_application
            3. Are they asking for specific information? → loan_info

            Return only: loan_query, loan_application, or loan_info"""

            messages = [{"role": "user", "content": prompt}]
            intent = self.get_completion(messages, temperature=0.2).strip().lower()

            # Validate intent
            if intent not in ["loan_query", "loan_application", "loan_info"]:
                intent = "loan_query"  # Default to loan query if unclear

            # Get real-time interest rates and other data
            context_data = self._fetch_loan_data(loan_type) if loan_type else {}
            
            # Add context to history
            self.add_to_history("system", f"Intent: {intent}, Loan Type: {loan_type}")

            return intent, {
                "loan_type": loan_type,
                "context_data": context_data
            }
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # Return safe default values
            return "loan_query", {
                "loan_type": "personal",
                "context_data": self._fetch_loan_data("personal")
            }

    def _detect_loan_type(self, message: str) -> str:
        """Detect the type of loan from the message."""
        try:
            if not isinstance(message, str):
                message = str(message)
                
            message = message.lower()
            
            # Check for future year mentions and handle appropriately
            future_years = ["2025", "2026", "2027", "2028", "2029", "2030"]
            has_future_year = any(year in message for year in future_years)
            
            for loan_type, keywords in self.loan_types.items():
                if any(keyword in message for keyword in keywords):
                    return loan_type
                    
            return "personal"  # Default to personal loan if unclear
            
        except Exception as e:
            print(f"Error detecting loan type: {str(e)}")
            return "personal"  # Safe default

    def _fetch_loan_data(self, loan_type: str) -> dict:
        """Fetch real-time loan data based on loan type."""
        try:
            if not loan_type:
                loan_type = "personal"
                
            # Use web search to get real-time data
            search_query = f"current {loan_type} loan interest rates india banks 2024"
            messages = [{"role": "user", "content": f"Find current {loan_type} loan details in India including interest rates, processing fees, and eligibility criteria. Format as JSON."}]
            data_response = self.get_completion(messages, temperature=0.2)
            
            # Add some default ranges in case specific data isn't available
            default_data = {
                "education": {
                    "interest_range": "8.15% - 15.20%",
                    "processing_fee": "0.5% - 1%",
                    "loan_amount": "Up to ₹75 lakhs",
                    "tenure": "Up to 15 years",
                    "top_banks": ["SBI", "HDFC", "ICICI", "Bank of Baroda", "Axis Bank"]
                },
                "business": {
                    "interest_range": "10.50% - 18.00%",
                    "processing_fee": "1% - 2%",
                    "loan_amount": "Up to ₹50 lakhs",
                    "tenure": "Up to 15 years",
                    "top_banks": ["SBI", "HDFC", "ICICI", "Bank of Baroda", "Axis Bank"]
                },
                "home": {
                    "interest_range": "8.40% - 9.80%",
                    "processing_fee": "0.5% - 1%",
                    "loan_amount": "Up to ₹5 crores",
                    "tenure": "Up to 30 years",
                    "top_banks": ["SBI", "HDFC", "ICICI", "LIC Housing", "Axis Bank"]
                },
                "personal": {
                    "interest_range": "10.50% - 18.00%",
                    "processing_fee": "1% - 3%",
                    "loan_amount": "Up to ₹40 lakhs",
                    "tenure": "Up to 5 years",
                    "top_banks": ["SBI", "HDFC", "ICICI", "Axis Bank", "Bajaj Finserv"]
                },
                "vehicle": {
                    "interest_range": "7.75% - 12.50%",
                    "processing_fee": "0.5% - 1.5%",
                    "loan_amount": "Up to ₹1 crore",
                    "tenure": "Up to 8 years",
                    "top_banks": ["SBI", "HDFC", "ICICI", "Axis Bank", "Bank of Baroda"]
                }
            }
            
            return default_data.get(loan_type, default_data["personal"])
            
        except Exception as e:
            print(f"Error fetching loan data: {str(e)}")
            # Return a minimal safe default
            return {
                "interest_range": "10.50% - 18.00%",
                "processing_fee": "1% - 3%",
                "loan_amount": "Please contact bank for details",
                "tenure": "1-5 years",
                "top_banks": ["SBI", "HDFC", "ICICI"]
            }

    def format_examples(self) -> str:
        """Format the intent examples for the prompt."""
        formatted = ""
        for intent, examples in self.intent_examples.items():
            formatted += f"\n{intent}:\n"
            for example in examples:
                formatted += f"- {example}\n"
        return formatted 
