from typing import Dict, Any, Optional
from .base_agent import BaseAgent

class LoanApplicationAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.current_state = {}
        self.document_requirements = {
            "business": [
                "Business registration documents",
                "GST registration (if applicable)",
                "Last 2 years IT returns",
                "Bank statements for last 6 months",
                "KYC documents (PAN, Aadhaar)",
                "Business plan or projection"
            ],
            "home": [
                "Property documents",
                "Sale agreement",
                "Salary slips (last 3 months)",
                "Bank statements (last 6 months)",
                "KYC documents (PAN, Aadhaar)",
                "IT returns (last 2 years)"
            ],
            "personal": [
                "Salary slips (last 3 months)",
                "Bank statements (last 6 months)",
                "KYC documents (PAN, Aadhaar)",
                "IT returns (last 2 years)",
                "Employment proof"
            ],
            "education": [
                "College admission letter",
                "Course fee structure",
                "Academic records",
                "KYC documents (PAN, Aadhaar)",
                "Co-applicant documents",
                "Collateral documents (if required)"
            ],
            "vehicle": [
                "Vehicle quotation",
                "Salary slips (last 3 months)",
                "Bank statements (last 6 months)",
                "KYC documents (PAN, Aadhaar)",
                "IT returns (last 2 years)",
                "Employment proof"
            ]
        }

    def process_message(self, message: str) -> str:
        """Process user message and guide through loan application."""
        # Add message to conversation history
        self.add_to_history("user", message)

        # Check if we have loan type information from eligibility check
        user_data = self.user_data.get("latest", {})
        loan_type = user_data.get("loan_type")

        if not loan_type:
            # Try to extract loan type from message
            loan_type = self.extract_loan_type(message)

        if loan_type:
            response = self.provide_application_guidance(loan_type, message)
        else:
            response = ("I can help you with the loan application process. "
                       "What type of loan are you interested in? (business, home, personal, education, or vehicle)")

        # Add response to conversation history
        self.add_to_history("assistant", response)
        return response

    def extract_loan_type(self, message: str) -> Optional[str]:
        """Extract loan type from message."""
        message = message.lower()
        for loan_type in self.document_requirements.keys():
            if loan_type in message:
                return loan_type
        return None

    def provide_application_guidance(self, loan_type: str, message: str) -> str:
        """Provide guidance based on loan type and user query."""
        # Prepare the prompt for generating guidance
        prompt = self.create_guidance_prompt(loan_type, message)

        # Get response from OpenAI
        messages = [{"role": "user", "content": prompt}]
        return self.get_completion(messages)

    def create_guidance_prompt(self, loan_type: str, message: str) -> str:
        """Create a prompt for generating loan application guidance."""
        documents = self.document_requirements[loan_type]
        docs_list = "\n".join(f"- {doc}" for doc in documents)

        prompt = f"""
        You are a helpful loan advisor guiding someone through the {loan_type} loan application process.
        
        Required Documents for {loan_type.title()} Loan:
        {docs_list}

        Key Points to Cover:
        - Application process steps
        - Document preparation tips
        - Processing timeline
        - Common mistakes to avoid
        - Next steps
        
        User query: {message}
        
        Provide clear, step-by-step guidance focusing on what's most relevant to the user's query.
        Keep the response practical and action-oriented.
        """

        return prompt

    def calculate_emi(self, principal: float, rate: float, tenure: int) -> float:
        """Calculate EMI for the loan."""
        # Convert annual interest rate to monthly
        monthly_rate = rate / (12 * 100)
        
        # Calculate EMI using formula: EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
        emi = principal * monthly_rate * pow(1 + monthly_rate, tenure) / (pow(1 + monthly_rate, tenure) - 1)
        
        return emi 