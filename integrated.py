import streamlit as st
import os
from dotenv import load_dotenv
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import google.generativeai as genai
import re
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize API clients
mistral_client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "loan_details" not in st.session_state:
    st.session_state.loan_details = {}
if "current_question_id" not in st.session_state:
    st.session_state.current_question_id = 0
if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = set()
if "application_stage" not in st.session_state:
    st.session_state.application_stage = None
if "application_answers" not in st.session_state:
    st.session_state.application_answers = {}
if "current_section" not in st.session_state:
    st.session_state.current_section = None
if "conversation_mode" not in st.session_state:
    st.session_state.conversation_mode = None
if "loan_type" not in st.session_state:
    st.session_state.loan_type = None
if "confirmation_stage" not in st.session_state:
    st.session_state.confirmation_stage = None

# Quick actions for sidebar
st.session_state.quick_actions = {
    "📚 Loan Types": "Learn about different types of loans",
    "💰 Interest Rates": "Current interest rates for various loans",
    "📋 Required Documents": "List of required documents for loan application",
    "📊 EMI Calculator": "Calculate your EMI",
    "❓ FAQs": "Frequently asked questions"
}
# Define loan application questions for each loan type
LOAN_APPLICATION_QUESTIONS = {
    "car_loan": {
        "personal_information": {
            "full_name": {"type": "text", "required": True},
            "date_of_birth": {"type": "date", "required": True},
            "email": {"type": "email", "required": True},
            "phone_number": {"type": "tel", "required": True},
            "aadhaar_number": {"type": "aadhaar", "required": True, "sensitive": True},
            "pan_number": {"type": "text", "required": True, "sensitive": True},
            "current_address": {"type": "text", "required": True}
        },
        "employment_information": {
            "employment_type": {"type": "text", "required": True},
            "employer_name": {"type": "text", "required": True},
            "work_experience": {"type": "number", "required": True},
            "annual_income": {"type": "indian_currency", "required": True},
            "job_title": {"type": "text", "required": True}
        },
        "financial_information": {
            "cibil_score": {"type": "cibil", "required": True},
            "existing_loans": {"type": "boolean", "required": True},
            "monthly_expenses": {"type": "indian_currency", "required": True},
            "bank_name": {"type": "text", "required": True},
            "account_number": {"type": "text", "required": True, "sensitive": True}
        },
        "vehicle_information": {
            "car_model": {"type": "text", "required": True},
            "car_cost": {"type": "indian_currency", "required": True},
            "down_payment": {"type": "indian_currency", "required": True},
            "loan_term": {"type": "number", "required": True}
        }
    },
    "personal_loan": {
        "personal_information": {
            "full_name": {"type": "text", "required": True},
            "date_of_birth": {"type": "date", "required": True},
            "email": {"type": "email", "required": True},
            "phone_number": {"type": "tel", "required": True},
            "aadhaar_number": {"type": "aadhaar", "required": True, "sensitive": True},
            "pan_number": {"type": "text", "required": True, "sensitive": True},
            "current_address": {"type": "text", "required": True}
        },
        "employment_information": {
            "employment_type": {"type": "text", "required": True},
            "employer_name": {"type": "text", "required": True},
            "work_experience": {"type": "number", "required": True},
            "annual_income": {"type": "indian_currency", "required": True},
            "job_title": {"type": "text", "required": True}
        },
        "financial_information": {
            "loan_amount": {"type": "indian_currency", "required": True},
            "loan_purpose": {"type": "text", "required": True},
            "loan_term": {"type": "number", "required": True},
            "cibil_score": {"type": "cibil", "required": True},
            "existing_loans": {"type": "boolean", "required": True},
            "monthly_expenses": {"type": "indian_currency", "required": True},
            "bank_name": {"type": "text", "required": True},
            "account_number": {"type": "text", "required": True, "sensitive": True}
        }
    },
    "business_loan": {
        "personal_information": {
            "full_name": {"type": "text", "required": True},
            "date_of_birth": {"type": "date", "required": True},
            "email": {"type": "email", "required": True},
            "phone_number": {"type": "tel", "required": True},
            "aadhaar_number": {"type": "aadhaar", "required": True, "sensitive": True},
            "pan_number": {"type": "text", "required": True, "sensitive": True},
            "current_address": {"type": "text", "required": True}
        },
        "business_information": {
            "business_name": {"type": "text", "required": True},
            "business_type": {"type": "text", "required": True},
            "business_age": {"type": "number", "required": True},
            "gst_number": {"type": "text", "required": True},
            "annual_turnover": {"type": "indian_currency", "required": True},
            "profit_last_year": {"type": "indian_currency", "required": True}
        },
        "loan_details": {
            "loan_amount": {"type": "indian_currency", "required": True},
            "loan_purpose": {"type": "text", "required": True},
            "loan_term": {"type": "number", "required": True},
            "collateral_available": {"type": "boolean", "required": True},
            "collateral_type": {"type": "text", "required": False}
        },
        "financial_information": {
            "cibil_score": {"type": "cibil", "required": True},
            "existing_loans": {"type": "boolean", "required": True},
            "monthly_revenue": {"type": "indian_currency", "required": True},
            "monthly_expenses": {"type": "indian_currency", "required": True},
            "bank_name": {"type": "text", "required": True},
            "account_number": {"type": "text", "required": True, "sensitive": True}
        }
    },
    "education_loan": {
        "personal_information": {
            "full_name": {"type": "text", "required": True},
            "date_of_birth": {"type": "date", "required": True},
            "email": {"type": "email", "required": True},
            "phone_number": {"type": "tel", "required": True},
            "aadhaar_number": {"type": "aadhaar", "required": True, "sensitive": True},
            "pan_number": {"type": "text", "required": True, "sensitive": True},
            "current_address": {"type": "text", "required": True}
        },
        "education_information": {
            "institution_name": {"type": "text", "required": True},
            "course_name": {"type": "text", "required": True},
            "course_duration": {"type": "number", "required": True},
            "course_country": {"type": "text", "required": True},
            "admission_status": {"type": "text", "required": True},
            "previous_qualification": {"type": "text", "required": True}
        },
        "financial_information": {
            "loan_amount": {"type": "indian_currency", "required": True},
            "course_fee": {"type": "indian_currency", "required": True},
            "living_expenses": {"type": "indian_currency", "required": True},
            "collateral_available": {"type": "boolean", "required": True},
            "collateral_type": {"type": "text", "required": False},
            "bank_name": {"type": "text", "required": True},
            "account_number": {"type": "text", "required": True, "sensitive": True}
        },
        "co_applicant_information": {
            "co_applicant_name": {"type": "text", "required": True},
            "relationship": {"type": "text", "required": True},
            "co_applicant_income": {"type": "indian_currency", "required": True},
            "co_applicant_occupation": {"type": "text", "required": True}
        }
    }
}
# Learning flow for different loan types
LEARNING_FLOW = {
    "car_loan": [
        {
            "question": "What would you like to know about car loans?",
            "topics": [
                "Interest rates and EMI calculation",
                "Documentation required",
                "Eligibility criteria",
                "Loan tenure options",
                "Processing fees and charges"
            ]
        }
    ],
    "personal_loan": [
        {
            "question": "What aspect of personal loans interests you?",
            "topics": [
                "Interest rates and processing fees",
                "Eligibility requirements",
                "Documentation needed",
                "Loan amount limits",
                "Repayment flexibility"
            ]
        }
    ],
    "business_loan": [
        {
            "question": "What would you like to learn about business loans?",
            "topics": [
                "Types of business loans",
                "Collateral requirements",
                "Interest rates and charges",
                "Eligibility criteria",
                "Documentation process"
            ]
        }
    ],
    "education_loan": [
        {
            "question": "What would you like to know about education loans?",
            "topics": [
                "Covered expenses",
                "Interest rates and repayment",
                "Moratorium period",
                "Collateral requirements",
                "Tax benefits"
            ]
        }
    ]
}

# Utility functions
def convert_indian_currency(amount_str):
    """Convert Indian currency format to float"""
    if not amount_str:
        return 0
    # Remove commas and spaces
    amount_str = str(amount_str).replace(',', '').replace(' ', '')
    # Remove any currency symbols
    amount_str = re.sub(r'[₹$]', '', amount_str)
    try:
        return float(amount_str)
    except ValueError:
        return 0

def convert_to_number(amount_str):
    """Convert various number formats to float"""
    if not amount_str:
        return 0
    
    amount_str = str(amount_str).lower().strip()
    amount_str = re.sub(r'[₹$]', '', amount_str)
    
    # Handle "lacs" or "lakhs"
    if 'lac' in amount_str or 'lakh' in amount_str:
        number = float(re.findall(r'[\d.]+', amount_str)[0])
        return number
    
    # Handle "k" or "thousand"
    if 'k' in amount_str or 'thousand' in amount_str:
        number = float(re.findall(r'[\d.]+', amount_str)[0])
        return number / 100
    
    # Handle regular numbers
    amount_str = amount_str.replace(',', '')
    try:
        return float(amount_str)
    except ValueError:
        return 0

def calculate_emi(principal, interest_rate, tenure_years):
    """Calculate EMI for a loan"""
    rate = interest_rate / (12 * 100)  # Monthly interest rate
    tenure_months = tenure_years * 12
    emi = (principal * rate * (1 + rate)**tenure_months) / ((1 + rate)**tenure_months - 1)
    return round(emi, 2)

def validate_aadhaar(aadhaar_number):
    """Validate Aadhaar number format"""
    if not aadhaar_number:
        return False
    aadhaar_str = str(aadhaar_number).replace(' ', '')
    return bool(re.match(r'^\d{12}$', aadhaar_str))

def validate_cibil(score):
    """Validate CIBIL score"""
    try:
        score = int(score)
        return 300 <= score <= 900
    except ValueError:
        return False

def validate_pan(pan):
    """Validate PAN number format"""
    if not pan:
        return False
    return bool(re.match(r'^[A-Z]{5}[0-9]{4}[A-Z]$', pan.upper()))

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
    phone_str = str(phone).replace(' ', '')
    return bool(re.match(r'^\d{10}$', phone_str))

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

def validate_date(date_str):
    """Validate date format (YYYY-MM-DD)"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_answer(answer, question_type):
    """Validate user answer based on question type"""
    if not answer:
        return False
        
    if question_type == "text":
        return len(str(answer).strip()) > 0
    elif question_type == "email":
        return validate_email(answer)
    elif question_type == "date":
        return validate_date(answer)
    elif question_type == "number":
        try:
            float(str(answer))
            return True
        except ValueError:
            return False
    elif question_type == "boolean":
        return answer.lower() in ['yes', 'no', 'true', 'false']
    elif question_type == "aadhaar":
        return validate_aadhaar(answer)
    elif question_type == "cibil":
        return validate_cibil(answer)
    elif question_type == "indian_currency":
        try:
            amount = convert_indian_currency(answer)
            return amount > 0
        except:
            return False
    elif question_type == "tel":
        return validate_phone(answer)
    return True

def get_loan_type_info(loan_type):
    """Get information about specific loan type"""
    loan_info = {
        "car_loan": {
            "interest_rates": "8.5% - 12.5% per annum",
            "processing_fee": "0.5% - 1% of loan amount",
            "tenure": "1 to 7 years",
            "loan_to_value": "Up to 90% of car value",
            "documents": [
                "Identity Proof (Aadhaar/PAN)",
                "Address Proof",
                "Income Proof",
                "Bank Statements (3 months)",
                "Car quotation"
            ]
        },
        "personal_loan": {
            "interest_rates": "10.5% - 24% per annum",
            "processing_fee": "1% - 3% of loan amount",
            "tenure": "1 to 5 years",
            "max_amount": "Up to 30 lakhs",
            "documents": [
                "Identity Proof (Aadhaar/PAN)",
                "Address Proof",
                "Income Proof",
                "Bank Statements (6 months)",
                "Salary Slips (3 months)"
            ]
        },
        "business_loan": {
            "interest_rates": "11% - 24% per annum",
            "processing_fee": "1% - 3% of loan amount",
            "tenure": "1 to 10 years",
            "max_amount": "Up to 50 lakhs",
            "documents": [
                "Business Registration Proof",
                "GST Returns",
                "Income Tax Returns",
                "Bank Statements (12 months)",
                "Business Financial Statements"
            ]
        },
        "education_loan": {
            "interest_rates": "8% - 15% per annum",
            "processing_fee": "0.5% - 1% of loan amount",
            "tenure": "5 to 15 years",
            "max_amount": "Based on course and institution",
            "documents": [
                "Admission Letter",
                "Course Fee Structure",
                "Academic Records",
                "Co-applicant Documents",
                "Collateral Documents (if applicable)"
            ]
        }
    }
    return loan_info.get(loan_type, {})

def get_next_learning_question(loan_type):
    """Get next question for learning mode based on loan type"""
    if not loan_type or loan_type not in LEARNING_FLOW:
        return "Which type of loan would you like to learn about?\n1. Car Loan\n2. Personal Loan\n3. Business Loan\n4. Education Loan"
    
    current_flow = LEARNING_FLOW[loan_type]
    if not st.session_state.current_question_id < len(current_flow):
        return "Would you like to apply for this loan now? (Type 'yes' to proceed with application)"
    
    question = current_flow[st.session_state.current_question_id]
    topics_list = "\n".join([f"{i+1}. {topic}" for i, topic in enumerate(question["topics"])])
    return f"{question['question']}\n\n{topics_list}"

def get_next_application_question():
    """Get next question for application mode"""
    loan_type = st.session_state.loan_type
    if not loan_type:
        return "Which type of loan would you like to apply for?\n1. Car Loan\n2. Personal Loan\n3. Business Loan\n4. Education Loan"
    
    if not st.session_state.current_section:
        sections = list(LOAN_APPLICATION_QUESTIONS[loan_type].keys())
        st.session_state.current_section = sections[0]
    
    current_section = st.session_state.current_section
    section_questions = LOAN_APPLICATION_QUESTIONS[loan_type][current_section]
    
    # Find first unanswered question in current section
    for field, details in section_questions.items():
        if field not in st.session_state.application_answers.get(current_section, {}):
            question_text = get_question_text(field, details["type"])
            return question_text
    
    # If all questions in current section are answered, move to next section
    sections = list(LOAN_APPLICATION_QUESTIONS[loan_type].keys())
    current_index = sections.index(current_section)
    
    if current_index + 1 < len(sections):
        st.session_state.current_section = sections[current_index + 1]
        return get_next_application_question()
    
    # If all sections are complete, move to confirmation
    return "application_complete"

def get_question_text(field, question_type):
    """Generate appropriate question text based on field and type"""
    field_name = field.replace('_', ' ').title()
    
    if question_type == "indian_currency":
        return f"Please enter your {field_name} (in INR, e.g., 20,00,000):"
    elif question_type == "date":
        return f"Please enter your {field_name} (YYYY-MM-DD):"
    elif question_type == "boolean":
        return f"{field_name}? (Yes/No):"
    elif question_type == "cibil":
        return f"Please enter your {field_name} (300-900):"
    elif question_type == "aadhaar":
        return f"Please enter your {field_name} (12 digits):"
    elif question_type == "tel":
        return f"Please enter your {field_name} (10 digits):"
    else:
        return f"Please enter your {field_name}:"

def process_learning_response(user_input):
    """Process responses during learning mode"""
    if not st.session_state.loan_type:
        loan_types = {
            "1": "car_loan",
            "2": "personal_loan",
            "3": "business_loan",
            "4": "education_loan"
        }
        st.session_state.loan_type = loan_types.get(user_input.strip())
        if not st.session_state.loan_type:
            return "Please select a valid loan type (1-4)"
        return get_next_learning_question(st.session_state.loan_type)
    
    current_flow = LEARNING_FLOW[st.session_state.loan_type]
    if st.session_state.current_question_id < len(current_flow):
        try:
            topic_index = int(user_input.strip()) - 1
            if 0 <= topic_index < len(current_flow[st.session_state.current_question_id]["topics"]):
                selected_topic = current_flow[st.session_state.current_question_id]["topics"][topic_index]
                loan_info = get_loan_type_info(st.session_state.loan_type)
                st.session_state.current_question_id += 1
                
                # Generate response based on selected topic and loan type
                response = generate_topic_response(st.session_state.loan_type, selected_topic, loan_info)
                next_question = get_next_learning_question(st.session_state.loan_type)
                return f"{response}\n\n{next_question}"
            else:
                return "Please select a valid option number"
        except ValueError:
            return "Please enter a valid number"
    
    if user_input.lower() == "yes":
        st.session_state.conversation_mode = "apply"
        st.session_state.application_stage = "started"
        return "Great! Let's proceed with your loan application. " + get_next_application_question()
    else:
        return "Would you like to learn about another type of loan? (Type 'yes' to continue)"

def generate_topic_response(loan_type, topic, loan_info):
    """Generate detailed response for selected learning topic"""
    responses = {
        "car_loan": {
            "Interest rates and EMI calculation": f"Current car loan interest rates range from {loan_info['interest_rates']}. The EMI amount depends on the loan amount, interest rate, and tenure. For example, for a 10 lakh loan at 10% interest for 5 years, the EMI would be approximately ₹21,247.",
            "Documentation required": f"Required documents include:\n" + "\n".join([f"• {doc}" for doc in loan_info['documents']]),
            "Eligibility criteria": "Eligibility depends on:\n• Age: 21-65 years\n• Income: Minimum ₹25,000 per month\n• Employment: At least 2 years of experience\n• Credit Score: Minimum 700",
            "Loan tenure options": f"Loan tenure typically ranges from {loan_info['tenure']}. Longer tenure means lower EMIs but higher total interest paid.",
            "Processing fees and charges": f"Processing fee is {loan_info['processing_fee']}. Additional charges may include:\n• Documentation charges\n• Insurance premium\n• Foreclosure charges"
        },
        "personal_loan": {
            "Interest rates and processing fees": f"Personal loans come with interest rates of {loan_info['interest_rates']} and processing fees of {loan_info['processing_fee']}.",
            "Eligibility requirements": "Key eligibility criteria:\n• Age: 21-60 years\n• Income: Minimum ₹20,000 per month\n• Credit Score: Minimum 750\n• Employment: Minimum 1 year with current employer",
            "Documentation needed": f"Required documents include:\n" + "\n".join([f"• {doc}" for doc in loan_info['documents']]),
            "Loan amount limits": f"Maximum loan amount is {loan_info['max_amount']}, subject to income and credit score.",
            "Repayment flexibility": "Flexible repayment options including:\n• Auto-debit facility\n• Choose suitable EMI date\n• Part-payment options\n• Prepayment facility"
        },
        "business_loan": {
            "Types of business loans": "Common types include:\n• Term Loans\n• Working Capital Loans\n• Equipment Financing\n• Invoice Financing\n• Overdraft Facility",
            "Collateral requirements": "Collateral requirements vary by loan type and amount. Secured loans offer better interest rates.",
            "Interest rates and charges": f"Interest rates range from {loan_info['interest_rates']} with processing fees of {loan_info['processing_fee']}.",
            "Eligibility criteria": "Business should be:\n• Operational for minimum 2 years\n• Profitable for last 1 year\n• Have good credit score\n• Regular GST filing",
            "Documentation process": f"Required documents include:\n" + "\n".join([f"• {doc}" for doc in loan_info['documents']])
        },
        "education_loan": {
            "Covered expenses": "Education loans cover:\n• Tuition fees\n• Living expenses\n• Books and equipment\n• Travel expenses\n• Insurance premium",
            "Interest rates and repayment": f"Interest rates range from {loan_info['interest_rates']}. {loan_info['processing_fee']} processing fee applies.",
            "Moratorium period": "Interest-only payments during study period plus 6-12 months after course completion or job placement.",
            "Collateral requirements": "Collateral may be required for loans above ₹7.5 lakhs. Options include:\n• Property\n• Fixed Deposits\n• Insurance policies",
            "Tax benefits": "Tax benefits under Section 80E for interest paid on education loan. No limit on deduction amount."
        }
    }
    return responses[loan_type].get(topic, "Information not available for this topic.")

def process_application_response(user_input):
    """Process responses during application phase"""
    if not st.session_state.loan_type:
        loan_types = {
            "1": "car_loan",
            "2": "personal_loan",
            "3": "business_loan",
            "4": "education_loan"
        }
        st.session_state.loan_type = loan_types.get(user_input.strip())
        if not st.session_state.loan_type:
            return "Please select a valid loan type (1-4)"
        return get_next_application_question()
    
    if st.session_state.confirmation_stage == "pending":
        if user_input.lower() == "yes":
            # Reset all states and return to home
            st.session_state.messages = []
            st.session_state.loan_details = {}
            st.session_state.current_question_id = 0
            st.session_state.answered_questions = set()
            st.session_state.application_stage = None
            st.session_state.application_answers = {}
            st.session_state.current_section = None
            st.session_state.conversation_mode = None
            st.session_state.loan_type = None
            st.session_state.confirmation_stage = None
            return "Thank you for your application! Our team will review it and contact you soon. Returning to home page..."
        elif user_input.lower() == "no":
            return "Would you like to stay and review your application or quit? (Type 'stay' or 'quit')"
        elif user_input.lower() == "stay":
            st.session_state.confirmation_stage = None
            return "You can review your application. Type 'submit' when you're ready to proceed."
        elif user_input.lower() == "quit":
            # Reset all states and return to home
            st.session_state.messages = []
            st.session_state.loan_details = {}
            st.session_state.current_question_id = 0
            st.session_state.answered_questions = set()
            st.session_state.application_stage = None
            st.session_state.application_answers = {}
            st.session_state.current_section = None
            st.session_state.conversation_mode = None
            st.session_state.loan_type = None
            st.session_state.confirmation_stage = None
            return "Returning to home page..."
        else:
            return "Please answer 'yes' to confirm submission, 'no' to review options, 'stay' to review application, or 'quit' to return to home page."

    current_section = st.session_state.current_section
    section_questions = LOAN_APPLICATION_QUESTIONS[st.session_state.loan_type][current_section]
    
    # Handle submission request
    if user_input.lower() == "submit":
        st.session_state.confirmation_stage = "pending"
        return "Are you sure you want to submit this application? (Type 'yes' to confirm)"
    
    # Find current question
    current_field = None
    for field, details in section_questions.items():
        if field not in st.session_state.application_answers.get(current_section, {}):
            current_field = field
            break
    
    if current_field:
        # Validate answer
        if validate_answer(user_input, section_questions[current_field]["type"]):
            store_application_answer(user_input)
            next_question = get_next_application_question()
            
            if next_question == "application_complete":
                return generate_application_summary() + "\n\nType 'submit' to proceed with your application."
            return next_question
        else:
            if section_questions[current_field]["type"] == "aadhaar":
                return "Invalid Aadhaar number. Please enter a valid 12-digit Aadhaar number."
            elif section_questions[current_field]["type"] == "cibil":
                return "Invalid CIBIL score. Please enter a score between 300 and 900."
            elif section_questions[current_field]["type"] == "indian_currency":
                return "Invalid amount format. Please enter amount like 20,00,000 or 2000000."
            elif section_questions[current_field]["type"] == "tel":
                return "Invalid phone number. Please enter a 10-digit number."
            else:
                return f"Invalid input. Please provide a valid {section_questions[current_field]['type']}."

def store_application_answer(answer):
    """Store the answer in the application answers"""
    current_section = st.session_state.current_section
    if current_section not in st.session_state.application_answers:
        st.session_state.application_answers[current_section] = {}
    
    # Find the current question field
    current_questions = LOAN_APPLICATION_QUESTIONS[st.session_state.loan_type][current_section]
    for field, details in current_questions.items():
        if field not in st.session_state.application_answers[current_section]:
            # Convert Indian currency format if needed
            if details["type"] == "indian_currency":
                answer = convert_indian_currency(answer)
            st.session_state.application_answers[current_section][field] = answer
            break

def generate_application_summary():
    """Generate a summary of the completed application"""
    loan_type_display = st.session_state.loan_type.replace('_', ' ').title()
    summary = f"Application Summary for {loan_type_display}:\n\n"
    
    for section, answers in st.session_state.application_answers.items():
        summary += f"{section.replace('_', ' ').title()}:\n"
        for field, value in answers.items():
            # Skip sensitive information in summary
            if not any(details.get("sensitive", False) 
                      for details in LOAN_APPLICATION_QUESTIONS[st.session_state.loan_type][section].values() 
                      if field in LOAN_APPLICATION_QUESTIONS[st.session_state.loan_type][section]):
                formatted_field = field.replace('_', ' ').title()
                if field in ["annual_income", "loan_amount", "monthly_expenses", "car_cost", "down_payment"]:
                    formatted_value = f"₹{value:,.2f}"
                elif field == "cibil_score":
                    formatted_value = f"{value} (Good)" if int(value) >= 750 else f"{value} (Fair)"
                else:
                    formatted_value = value
                summary += f"• {formatted_field}: {formatted_value}\n"
        summary += "\n"
    
    return summary

def process_response(user_input):
    """Process user response and determine next action"""
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Handle initial mode selection
    if not st.session_state.conversation_mode:
        if "1" in user_input or "learn" in user_input.lower():
            st.session_state.conversation_mode = "learn"
            response = "What type of loan would you like to learn about?\n1. Car Loan\n2. Personal Loan\n3. Business Loan\n4. Education Loan"
        elif "2" in user_input or "apply" in user_input.lower():
            st.session_state.conversation_mode = "apply"
            st.session_state.application_stage = "started"
            response = "What type of loan would you like to apply for?\n1. Car Loan\n2. Personal Loan\n3. Business Loan\n4. Education Loan"
        else:
            response = "Please choose:\n1. Learn about loans\n2. Apply for a loan"
    
    # Handle learning mode
    elif st.session_state.conversation_mode == "learn":
        response = process_learning_response(user_input)
    
    # Handle application mode
    elif st.session_state.conversation_mode == "apply":
        response = process_application_response(user_input)
    
    # Display response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

def handle_quick_action(action):
    """Handle quick action button clicks"""
    if action == "📚 Loan Types":
        return """Available Loan Types:
1. Car Loan - For vehicle purchases
2. Personal Loan - For personal expenses
3. Business Loan - For business needs
4. Education Loan - For higher education

Would you like to learn more about any specific type? (Enter 1-4)"""
    
    elif action == "💰 Interest Rates":
        return """Current Interest Rates:
• Car Loans: 8.5% - 12.5% p.a.
• Personal Loans: 10.5% - 24% p.a.
• Business Loans: 11% - 24% p.a.
• Education Loans: 8% - 15% p.a.

Rates may vary based on credit score and other factors."""
    
    elif action == "📋 Required Documents":
        return """Common Required Documents:
• Identity Proof (Aadhaar/PAN)
• Address Proof
• Income Proof
• Bank Statements
• Credit Score Report

Additional documents may be required based on loan type."""
    
    elif action == "📊 EMI Calculator":
        return """EMI Calculation Example:
For a loan of ₹10,00,000:
• At 10% interest for 5 years: ₹21,247/month
• At 12% interest for 5 years: ₹22,244/month
• At 8% interest for 5 years: ₹20,276/month

Would you like to calculate EMI for a specific amount?"""
    
    elif action == "❓ FAQs":
        return """Frequently Asked Questions:
1. How is my loan eligibility determined?
   - Based on income, credit score, and existing obligations
   
2. Can I prepay my loan?
   - Yes, most loans allow prepayment (charges may apply)
   
3. How long does approval take?
   - Typically 2-7 working days
   
4. What affects interest rates?
   - Credit score, income, loan amount, and tenure
   
5. Is collateral always required?
   - Depends on loan type and amount

Need more specific information? Just ask!"""
    
    return "Please select a valid quick action."

# Streamlit UI
st.title("🏦 Loan Assistant")

# Sidebar with quick actions
with st.sidebar:
    st.header("Quick Actions")
    if st.button("🔄 Start New Chat"):
        st.session_state.messages = []
        st.session_state.loan_details = {}
        st.session_state.current_question_id = 0
        st.session_state.answered_questions = set()
        st.session_state.application_stage = None
        st.session_state.application_answers = {}
        st.session_state.current_section = None
        st.session_state.conversation_mode = None
        st.session_state.loan_type = None
        st.session_state.confirmation_stage = None
        st.rerun()
    
    # Display quick actions
    st.subheader("Helpful Resources")
    for action, description in st.session_state.quick_actions.items():
        if st.button(f"{action}", help=description):
            with st.chat_message("assistant"):
                response = handle_quick_action(action)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# Initial welcome message only if no messages exist
if not st.session_state.messages:
    initial_message = """👋 Welcome to the Loan Assistant! I can help you:
1. Learn about different types of loans
2. Apply for a loan

Please choose an option (1 or 2)."""
    with st.chat_message("assistant"):
        st.markdown(initial_message)
    st.session_state.messages.append({"role": "assistant", "content": initial_message})

# Display chat history
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get user input
if prompt := st.chat_input("Type your message here..."):
    process_response(prompt)

instead of listing out and asking what kind of loan i want to just input a loan name when asked what kind of loan. the list shouldnt be there. the rest code should be same. print the entire code
