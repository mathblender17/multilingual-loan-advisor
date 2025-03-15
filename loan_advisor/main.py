import os
from typing import Dict, Any
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from dotenv import load_dotenv

# Import agents - using relative imports
from agents.intent_classifier import IntentClassifierAgent
from agents.loan_eligibility import LoanEligibilityAgent
from agents.loan_application import LoanApplicationAgent
from agents.financial_literacy import LoanInfoAgent

# Load environment variables
load_dotenv()

# For testing/demo purposes, we can temporarily bypass the API key requirement
# Remove this for production
os.environ["GROQ_API_KEY"] = os.environ.get("GROQ_API_KEY", "dummy_api_key_for_testing")

class LoanAdvisor:
    def __init__(self):
        self.console = Console()
        self.agents = {
            "intent_classifier": IntentClassifierAgent(),
            "education_loan": LoanEligibilityAgent(),
            "loan_application": LoanApplicationAgent(),
            "loan_info": LoanInfoAgent()
        }
        self.current_agent = "intent_classifier"
        self.conversation_history = []
        
        # Print successful initialization for debugging
        print("LoanAdvisor initialized successfully")

    def display_welcome_message(self):
        """Display welcome message and instructions."""
        welcome_text = """
        Welcome to the Loan Advisor!
        
        I can help you with:
        • Learning about different loan types (education, home, business, personal, vehicle)
        • Checking your eligibility 
        • Understanding the application process
        • Calculating EMI and comparing options
        
        What type of loan are you interested in?
        
        Type 'help' anytime to see these options again.
        """
        self.console.print(Panel(welcome_text, title="💰 Loan Advisor", border_style="blue"))

    def process_user_input(self, user_input: str) -> str:
        """Process user input and return appropriate response."""
        # Save user input to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Check for help command
        if user_input.lower() == "help":
            return self._get_help_message()
            
        # Check for specific commands
        if user_input.lower() in ["options", "menu"]:
            return self._get_options_menu()
            
        if self.current_agent == "intent_classifier":
            # Classify intent and route to appropriate agent
            intent, context_data = self.agents["intent_classifier"].process_message(user_input)
            # Map intent to agent and set context
            self.current_agent = self.map_intent_to_agent(intent)
            
            # Process with appropriate agent
            if self.current_agent == "education_loan":
                # For loan eligibility, we first give information before asking personal questions
                response = self._get_loan_info(context_data.get("loan_type", "personal"))
            else:
                # For other agents, process normally
                response = self.agents[self.current_agent].process_message(user_input)
        else:
            # Process message with current agent
            response = self.agents[self.current_agent].process_message(user_input)
        
        # Ensure the response includes next steps
        if not any(phrase in response for phrase in ["Would you like", "Do you want", "Can I help", "What would you like", "next steps", "options", "?"]):
            response += "\n\nWhat would you like to do next? Type 'options' to see available actions."
            
        # Save response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def _get_help_message(self) -> str:
        """Return a helpful message with available commands."""
        return """
        Here's how I can help you:
        
        • Type the loan type you're interested in (education, business, home, personal, vehicle)
        • Ask specific questions about loan details, eligibility, or application process
        • Type 'calculate' to use our loan calculator
        • Type 'compare' to compare different loan options
        • Type 'options' to see specific actions for your current topic
        • Type 'reset' to start over
        
        How can I assist you today?
        """
        
    def _get_options_menu(self) -> str:
        """Return context-sensitive options based on current agent."""
        if self.current_agent == "education_loan":
            return """
            Options for Education Loans:
            
            1. "Tell me about education loans" - Get general information
            2. "Check my eligibility" - Find out if you qualify
            3. "How to apply" - Learn about the application process
            4. "Calculate EMI" - Estimate your monthly payments
            5. "Documents required" - See what paperwork you need
            
            What would you like to know about?
            """
        elif self.current_agent == "loan_application":
            return """
            Options for Loan Application:
            
            1. "Documents required" - See what paperwork you need
            2. "Application steps" - Get a step-by-step guide
            3. "Online vs offline" - Compare application methods
            4. "Processing time" - Learn how long it takes
            5. "Common mistakes" - Avoid application pitfalls
            
            What would you like to know about?
            """
        elif self.current_agent == "loan_info":
            return """
            Options for Loan Information:
            
            1. "Interest rates" - Get current interest rates
            2. "EMI calculation" - Understand monthly payments
            3. "Loan terms" - Learn about repayment periods
            4. "Fees and charges" - Understand all costs involved
            5. "Compare banks" - See which banks offer the best deals
            
            What would you like to know about?
            """
        else:
            return """
            General Options:
            
            1. "Education loan" - Learn about student loans
            2. "Business loan" - Financing for your business
            3. "Home loan" - Buy or renovate property
            4. "Personal loan" - General purpose loans
            5. "Vehicle loan" - Finance a car or bike
            
            Which topic interests you?
            """
            
    def _get_loan_info(self, loan_type: str) -> str:
        """Provide general loan information before asking personal questions."""
        loan_info = {
            "education": """
            📚 Education Loan Information:
            
            Education loans help students finance their higher education expenses including tuition fees, books, equipment, and sometimes living expenses.
            
            💰 Key Features:
            • Loan amounts: ₹50,000 to ₹75 lakhs depending on the course and institution
            • Interest rates: 8.15% to 15.20% (with concessions for female students)
            • Repayment period: Up to 15 years after course completion
            • Moratorium period: Course duration + 6 months to 1 year
            • Tax benefits under Section 80E of Income Tax Act
            
            ✅ Eligibility:
            • Indian citizen with admission to recognized institution
            • For loans up to ₹4 lakhs: No collateral required
            • For loans above ₹4 lakhs: Collateral and/or guarantor required
            
            Would you like to:
            1. Check your specific eligibility
            2. Learn about the application process
            3. Calculate your potential EMI
            4. See documents required
            
            Please type your choice or ask any questions you have about education loans.
            """,
            
            "business": """
            💼 Business Loan Information:
            
            Business loans provide funding for starting or expanding businesses, purchasing equipment, managing cash flow, or other business needs.
            
            💰 Key Features:
            • Loan amounts: ₹1 lakh to ₹50 lakhs (unsecured), higher for secured loans
            • Interest rates: 10.50% to 18.00% depending on business profile
            • Repayment period: 1 to 15 years based on loan amount
            • Processing fees: 1% to 2% of loan amount
            • Flexible repayment options available
            
            ✅ Eligibility:
            • Business age: Typically 2+ years in operation
            • Minimum turnover requirements (varies by bank)
            • Good credit score (usually 700+)
            • Profitability for at least 1-2 years
            
            Would you like to:
            1. Check your business loan eligibility
            2. Learn about the application process
            3. Calculate potential EMI
            4. See documents required
            
            Please type your choice or ask any specific questions about business loans.
            """,
            
            "home": """
            🏠 Home Loan Information:
            
            Home loans help finance the purchase, construction, or renovation of residential property.
            
            💰 Key Features:
            • Loan amounts: Up to ₹5 crores depending on property value
            • Interest rates: 8.40% to 9.80% (may vary based on credit score)
            • Repayment period: Up to 30 years
            • Loan-to-Value ratio: Up to 80% of property value
            • Tax benefits under Section 80C and 24(b)
            
            ✅ Eligibility:
            • Age: 23-65 years
            • Income stability: Regular income source
            • Credit score: Typically 750+ for best rates
            • Property: Clear title and proper approvals
            
            Would you like to:
            1. Check your home loan eligibility
            2. Learn about the application process
            3. Calculate your potential EMI
            4. See documents required
            
            Please type your choice or ask any questions you have about home loans.
            """,
            
            "personal": """
            💳 Personal Loan Information:
            
            Personal loans are unsecured loans that can be used for any legitimate personal purpose such as medical expenses, travel, wedding, or debt consolidation.
            
            💰 Key Features:
            • Loan amounts: ₹50,000 to ₹40 lakhs
            • Interest rates: 10.50% to 18.00%
            • Repayment period: 1 to 5 years
            • Quick approval: Often within 2-3 days
            • No collateral required
            
            ✅ Eligibility:
            • Age: 21-60 years
            • Income stability: Regular income source
            • Credit score: Typically 700+ for approval
            • Employment: Usually 2+ years of work experience
            
            Would you like to:
            1. Check your personal loan eligibility
            2. Learn about the application process
            3. Calculate your potential EMI
            4. See documents required
            
            Please type your choice or ask any questions you have about personal loans.
            """,
            
            "vehicle": """
            🚗 Vehicle Loan Information:
            
            Vehicle loans help finance the purchase of cars, bikes, or other vehicles.
            
            💰 Key Features:
            • Loan amounts: Up to ₹1 crore depending on vehicle
            • Interest rates: 7.75% to 12.50%
            • Repayment period: Up to 8 years
            • Loan-to-Value ratio: Up to 90% of vehicle cost
            • Quick approval: Often within 1-2 days
            
            ✅ Eligibility:
            • Age: 21-65 years
            • Income: Minimum income requirements vary by bank
            • Credit score: Typically 650+ for approval
            • Down payment: 10-20% of vehicle cost
            
            Would you like to:
            1. Check your vehicle loan eligibility
            2. Learn about the application process
            3. Calculate your potential EMI
            4. See documents required
            
            Please type your choice or ask any questions you have about vehicle loans.
            """
        }
        
        return loan_info.get(loan_type, loan_info["personal"])

    def map_intent_to_agent(self, intent: str) -> str:
        """Map intent to appropriate agent."""
        intent_map = {
            "loan_query": "education_loan",
            "loan_application": "loan_application",
            "loan_info": "loan_info"
        }
        return intent_map.get(intent, "intent_classifier")  # Default to intent classifier

    def run(self):
        """Run the main application loop."""
        # Check if Groq API key is set
        if not os.getenv("GROQ_API_KEY"):
            self.console.print("[red]Error: GROQ_API_KEY environment variable is not set.[/red]")
            self.console.print("Please create a .env file with your Groq API key:")
            self.console.print("GROQ_API_KEY=your-api-key-here")
            return

        self.display_welcome_message()

        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[blue]You[/blue]")
                
                # Check for exit command
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self.console.print("\n[green]Thank you for using the Loan Advisor. Goodbye![/green]")
                    break

                # Check for reset command
                if user_input.lower() in ["reset", "restart", "start over"]:
                    self.current_agent = "intent_classifier"
                    self.conversation_history = []
                    self.console.print("\n[green]Advisor[/green]: Let's start fresh! How can I help you with loans today?")
                    continue
                    
                # Check for eligibility request - direct to loan eligibility agent
                if any(phrase in user_input.lower() for phrase in ["check eligibility", "eligible", "qualify", "check if"]) and not self.current_agent == "education_loan":
                    # First determine loan type from query
                    _, context_data = self.agents["intent_classifier"].process_message(user_input)
                    self.current_agent = "education_loan"
                    
                # Process user input and get response
                response = self.process_user_input(user_input)
                
                # Display response
                self.console.print(f"\n[green]Advisor[/green]: {response}")

            except KeyboardInterrupt:
                self.console.print("\n[green]Thank you for using the Loan Advisor. Goodbye![/green]")
                break
            except Exception as e:
                self.console.print(f"[red]An error occurred: {str(e)}[/red]")
                self.current_agent = "intent_classifier"  # Reset to initial state

if __name__ == "__main__":
    advisor = LoanAdvisor()
    advisor.run() 