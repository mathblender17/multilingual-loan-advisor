from typing import List
from .base_agent import BaseAgent

class LoanInfoAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.topics = {
            "interest_rates": [
                "interest rate",
                "rate of interest",
                "how much interest",
                "interest charges"
            ],
            "emi": [
                "emi",
                "monthly payment",
                "installment",
                "repayment"
            ],
            "eligibility": [
                "who can apply",
                "eligibility",
                "qualify",
                "am i eligible",
                "can i get"
            ],
            "documents": [
                "documents",
                "papers",
                "what to bring",
                "what do i need",
                "requirements"
            ],
            "banks": [
                "which bank",
                "best bank",
                "bank options",
                "lenders",
                "sbi",
                "hdfc"
            ]
        }

    def process_message(self, message: str) -> str:
        """Process user message and provide education loan information."""
        # Add message to conversation history
        self.add_to_history("user", message)

        # Identify the topic and create a prompt
        topic = self.identify_topic(message)
        prompt = self.create_prompt(message, topic)

        # Get response
        messages = [{"role": "user", "content": prompt}]
        response = self.get_completion(messages)

        # Add response to conversation history
        self.add_to_history("assistant", response)
        return response

    def identify_topic(self, message: str) -> str:
        """Identify the loan information topic from the message."""
        message = message.lower()
        
        for topic, keywords in self.topics.items():
            if any(keyword in message for keyword in keywords):
                return topic
        
        return "general"

    def create_prompt(self, message: str, topic: str) -> str:
        """Create a prompt for generating loan information."""
        prompts = {
            "interest_rates": """
                Explain education loan interest rates in simple terms. Include:
                - Current interest rate ranges for education loans in India (8-13%)
                - Fixed vs floating rates for education loans
                - How interest is calculated during study period
                - Interest subsidy schemes for eligible students
                - Simple examples with numbers
                
                Use friendly language a high school student could understand.
                """,
            "emi": """
                Explain education loan EMI in simple terms. Include:
                - How EMI works specifically for education loans
                - When repayment starts (usually after course completion/grace period)
                - Moratorium period explanation
                - EMI calculation example for a typical education loan
                - Tips to manage EMI payments for students
                
                Make it very simple with real examples.
                """,
            "eligibility": """
                Explain education loan eligibility in simple terms. Include:
                - Who can apply (students + co-applicant requirements)
                - Age requirements (minimal for students)
                - Academic requirements (admission to recognized institution)
                - Course eligibility criteria
                - No income requirements for student, but co-applicant considerations
                
                Use very simple language with encouraging tone.
                """,
            "documents": """
                Explain education loan document requirements clearly. Include:
                - Essential documents needed (ID proof, admission letter, fee structure)
                - Co-applicant documents required
                - Academic documents needed
                - Income proof requirements (for co-applicant)
                - Property documents (if applicable for larger loans)
                
                Present as a simple checklist that's easy to follow.
                """,
            "banks": """
                Compare education loan options from different banks. Include:
                - Top 3-4 banks for education loans in India
                - Key differences in their education loan offerings
                - Special features or benefits of each
                - Interest rate comparisons
                - Processing time and fees comparison
                
                Keep it factual and helpful without bias.
                """,
            "general": """
                Provide helpful information about education loans. Include:
                - Basic education loan features
                - Key benefits of education loans
                - Tax benefits of education loans
                - Common questions students have
                - Simple tips for application
                
                Use simple language focused only on education loans.
                """
        }

        base_prompt = f"""
        You are helping a student understand education loans. The student asked:
        
        "{message}"
        
        {prompts.get(topic, prompts['general'])}
        
        Make your response:
        - Very simple to understand (use everyday language)
        - Directly answer what was asked
        - Include specific numbers and examples
        - Be encouraging and positive
        - Focus ONLY on education loans
        - DO NOT include general financial advice unless specifically asked
        """

        return base_prompt 