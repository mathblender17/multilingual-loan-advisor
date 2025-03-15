from agents import LoanAdvisorAgents

def main():
    # Initialize the loan advisor agents
    loan_advisor = LoanAdvisorAgents()
    
    print("Welcome to the Multilingual Conversational Loan Advisor!")
    print("You can ask questions in any language about loans, eligibility, application process, or financial advice.")
    print("Type 'exit' to quit.")
    
    while True:
        # Get user input
        user_query = input("\nYour question: ")
        
        if user_query.lower() == 'exit':
            print("Thank you for using the Loan Advisor. Goodbye!")
            break
            
        # Create and run the crew
        crew = loan_advisor.create_crew(user_query)
        result = crew.kickoff()
        
        # Display the result
        print("\nResponse:")
        print(result)

if __name__ == "__main__":
    main() 