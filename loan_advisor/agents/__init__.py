"""
Loan Advisor Agents Package

This package contains the different AI agents used in the Loan Advisor system:
- Intent Classifier Agent: Routes user queries to appropriate agents
- Loan Eligibility Agent: Checks loan eligibility based on user criteria
- Loan Application Agent: Guides users through the loan application process
- Financial Literacy Agent: Provides financial advice and explanations
"""

# Empty __init__.py file to avoid circular imports
# Let each module import what it needs directly

__all__ = [
    'BaseAgent',
    'IntentClassifierAgent',
    'LoanEligibilityAgent',
    'LoanApplicationAgent',
    'LoanInfoAgent'  # Updated to match the new class name
] 