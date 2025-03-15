import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class LoanBot:
    def __init__(self):
        # Use gemini-1.5-pro model
        self.model = genai.GenerativeModel('models/gemini-1.5-pro')
        self.context = """
        You are a specialized loan assistant. Your role is to provide accurate, helpful information about loans and financial services.
        
        Focus on:
        1. Different types of loans (personal, home, education, business)
        2. Loan eligibility criteria
        3. Interest rates and EMI calculations
        4. Documentation requirements
        5. Loan application processes
        6. Credit score impact
        7. Loan repayment strategies
        
        Guidelines:
        - Provide specific, actionable information
        - Include numerical examples when relevant
        - Explain financial terms in simple language
        - If unsure, acknowledge limitations
        - Only answer loan and banking related queries
        - For non-loan questions, politely redirect to loan topics
        
        Remember to be helpful while maintaining accuracy in financial information.
        """
        
    def get_loan_response(self, user_query):
        try:
            # Combine context and user query
            prompt = f"{self.context}\n\nUser Query: {user_query}\n\nProvide a detailed, helpful response focusing on loan-related information:"
            
            # Get response from the model with safety settings
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                prompt,
                safety_settings=safety_settings,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    top_p=0.8,
                    top_k=40,
                    max_output_tokens=2048
                )
            )
            
            # Extract the response
            if response.text:
                return response.text.strip()
            
            return "I apologize, but I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            return f"I encountered an error: {str(e)}. Please try again."

    def is_loan_related(self, query):
        loan_keywords = [
            'loan', 'credit', 'borrow', 'lending', 'mortgage', 'emi', 'interest',
            'repayment', 'debt', 'finance', 'bank', 'collateral', 'principal',
            'education loan', 'home loan', 'personal loan', 'business loan',
            'eligibility', 'documents', 'application', 'approval', 'tenure',
            'rate', 'payment', 'installment', 'security', 'guarantee'
        ]
        return any(keyword in query.lower() for keyword in loan_keywords)

def main():
    print("Initializing Loan Assistant...")
    try:
        bot = LoanBot()
        print("\n🏦 Welcome to the Loan Assistant!")
        print("I can help you with loan-related questions. Type 'exit' to end the conversation.")
        print("\nExample questions you can ask:")
        print("- What documents do I need for a home loan?")
        print("- How is loan EMI calculated?")
        print("- What factors affect loan interest rates?")
        print("- How can I improve my credit score?")
        print("- What types of business loans are available?")
        
        while True:
            user_input = input("\nYour question: ").strip()
            
            if user_input.lower() == 'exit':
                print("Thank you for using the Loan Assistant. Goodbye!")
                break
            
            if not user_input:
                print("Please enter a question.")
                continue
                
            if not bot.is_loan_related(user_input):
                print("I apologize, but I can only assist with loan-related questions. Please ask something about loans, credit, or financing.")
                continue
            
            response = bot.get_loan_response(user_input)
            print("\nAssistant:", response)

    except Exception as e:
        print(f"An error occurred while initializing the bot: {str(e)}")
        print("Please make sure your API key is correct and try again.")

if __name__ == "__main__":
    main()
