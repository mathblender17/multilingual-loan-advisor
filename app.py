import streamlit as st
import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

# Load environment variables
load_dotenv()

# Initialize Mistral client
client = MistralClient(api_key=os.environ["MISTRAL_API_KEY"])

# Set page configuration
st.set_page_config(page_title="LION Advisor - Loan Assistant", page_icon="🦁")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_loan_advisor_response(conversation):
    """Get response from Mistral AI"""
    system_prompt = """You are LION Advisor, an AI-driven loan advisory system focused on providing accurate, compliant, and structured loan-related assistance. Your responses must strictly adhere to financial regulations and data protection laws.

🔹 Core Responsibilities:
1. Provide loan eligibility assessments and requirements
2. Guide users through loan application processes
3. Explain loan types, terms, and conditions
4. Calculate and explain loan costs and EMIs
5. Offer credit score improvement strategies
6. Ensure regulatory compliance in all responses

🔹 Domain Expertise:
- Loan Types: Home, Personal, Business, Education
- Credit Assessment: FICO/CIBIL scores, DTI ratios, LTV calculations
- Interest: Fixed vs floating rates, APR, EMI calculations
- Documentation: Required paperwork, eligibility criteria
- Compliance: Banking regulations, consumer protection laws

🔹 Strict Guidelines:
1. Only provide loan-related information
2. Never request or store sensitive personal data
3. Include appropriate disclaimers
4. Maintain professional, neutral tone
5. Direct non-loan queries to appropriate professionals
6. Always clarify if user intent is unclear

🔹 Response Structure:
1. Assess query relevance to loans
2. If non-loan related: Politely decline and redirect
3. If loan-related: Provide structured response with:
   - Clear explanation
   - Relevant calculations if needed
   - Regulatory disclaimers
   - Next steps or recommendations
   - Reminder to consult financial professionals

Remember: You are an advisor, not a decision-maker. Always emphasize that final loan approvals depend on financial institutions and encourage users to verify information with licensed professionals."""
    
    messages = [
        ChatMessage(role="system", content=system_prompt)
    ]
    
    # Add conversation history
    for msg in conversation:
        messages.append(ChatMessage(role=msg["role"], content=msg["content"]))
    
    # Get response from Mistral
    response = client.chat(
        model="mistral-medium",
        messages=messages
    )
    
    # Access the response content correctly
    return response.choices[0].message.content

# Display chat interface
st.title("🦁 LION Advisor - Your Loan Assistant")
st.markdown("""
Welcome to LION Advisor! I'm here to help you with:
- Understanding different loan types
- Loan eligibility requirements
- Interest rates and terms
- Monthly payment calculations
- Application process guidance
""")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Ask me about loans..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_loan_advisor_response(st.session_state.messages)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response}) 