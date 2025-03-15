from typing import Dict, Any, Optional
from .base_agent import BaseAgent

# Define default values for constants that would be imported from config
DEFAULT_MIN_CREDIT_SCORES = {"education": 0, "business": 700, "home": 750, "personal": 700, "vehicle": 650}
DEFAULT_MIN_INCOME = {"education": 0, "business": 50000, "home": 30000, "personal": 20000, "vehicle": 15000}
DEFAULT_LOAN_TYPES = ["education", "business", "home", "personal", "vehicle"]

# Try to import from config, use defaults if it fails
try:
    from ..config import MIN_CREDIT_SCORES, MIN_INCOME, LOAN_TYPES
except ImportError:
    # Use default values if import fails
    MIN_CREDIT_SCORES = DEFAULT_MIN_CREDIT_SCORES
    MIN_INCOME = DEFAULT_MIN_INCOME
    LOAN_TYPES = DEFAULT_LOAN_TYPES
    print("Using default config values for loan eligibility")

class LoanEligibilityAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.current_state = {}
        self.required_fields = {
            "education": [
                "student_name",
                "course_name",
                "course_duration",
                "college_name",
                "course_fee",
                "parent_details"
            ],
            "business": [
                "business_name",
                "business_type",
                "years_in_business",
                "annual_turnover",
                "loan_amount",
                "collateral_details"
            ],
            "home": [
                "applicant_name",
                "property_value",
                "property_location",
                "loan_amount",
                "income",
                "employment_details"
            ],
            "personal": [
                "applicant_name",
                "income",
                "employment_details",
                "loan_amount",
                "purpose",
                "existing_loans"
            ],
            "vehicle": [
                "applicant_name",
                "vehicle_type",
                "vehicle_cost",
                "down_payment",
                "income",
                "employment_details"
            ]
        }

    def process_message(self, message: str) -> str:
        """Process user message with a direct, helpful approach focused on loans."""
        try:
            # Validate and clean input
            if not isinstance(message, str):
                message = str(message)
                
            message_lower = message.lower()
            
            # Check if this is a reset request
            if any(word in message_lower for word in ["reset", "start over", "restart", "new"]):
                self.current_state = {}
                return """Let's start fresh with your loan inquiry. What type of loan information would you like?
                (Education, Business, Home, Personal, or Vehicle loan)"""
            
            # Check if user explicitly wants to check eligibility
            check_eligibility = any(word in message_lower for word in ["check eligibility", "am i eligible", "do i qualify", "eligibility check"])
            
            # If we're already in an eligibility check process
            if self.current_state and "step" in self.current_state and self.current_state["step"] > 0:
                response = self.update_state(message)
                if response:
                    return response
                return self.get_next_question()
            
            # If this is a new request or starting an eligibility check
            loan_type = self._detect_loan_type(message)
            
            if check_eligibility:
                # Start eligibility check process
                self.current_state = {"step": 0, "loan_type": loan_type}
                return f"""
                To check your eligibility for a {loan_type} loan, I'll need some information from you.
                
                Do you want to proceed with the eligibility check? (Yes/No)
                """
            else:
                # Provide loan information without asking personal questions
                return self._get_loan_information(loan_type, message)
                
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return """I apologize for the confusion. Let me know what type of loan you're interested in, 
            and I can provide information or check your eligibility if you'd like."""

    def _detect_loan_type(self, message: str) -> str:
        """Detect loan type from message."""
        try:
            if not isinstance(message, str):
                message = str(message)
                
            message = message.lower()
            
            # Check for future year mentions and handle appropriately
            future_years = ["2025", "2026", "2027", "2028", "2029", "2030"]
            has_future_year = any(year in message for year in future_years)
            
            loan_keywords = {
                "education": ["education", "study", "college", "university", "school"],
                "business": ["business", "startup", "company", "enterprise"],
                "home": ["home", "house", "property", "flat", "apartment"],
                "personal": ["personal", "individual", "emergency", "medical"],
                "vehicle": ["vehicle", "car", "bike", "auto"]
            }

            for loan_type, keywords in loan_keywords.items():
                if any(keyword in message for keyword in keywords):
                    return loan_type
                    
            return "personal"  # Default to personal loan if unclear
            
        except Exception as e:
            print(f"Error detecting loan type: {str(e)}")
            return "personal"  # Safe default

    def _get_loan_information(self, loan_type: str, message: str) -> str:
        """Provide information about loans without asking personal questions."""
        message_lower = message.lower() if isinstance(message, str) else ""
        
        # Check for specific information requests
        if any(word in message_lower for word in ["interest", "rate"]):
            return self._get_interest_info(loan_type)
        elif any(word in message_lower for word in ["document", "paperwork"]):
            return self._get_document_info(loan_type)
        elif any(word in message_lower for word in ["process", "apply", "procedure", "how to"]):
            return self._get_process_info(loan_type)
        elif any(word in message_lower for word in ["emi", "installment", "payment", "calculate"]):
            return self._get_emi_info(loan_type)
        else:
            # Provide general information
            return self._get_general_info(loan_type)

    def _get_interest_info(self, loan_type: str) -> str:
        """Provide interest rate information."""
        info = {
            "education": """
            📊 Current Education Loan Interest Rates (2024):
            
            • SBI: 8.65% - 10.15%
            • HDFC: 9.55% - 11.70%
            • Bank of Baroda: 7.35% - 9.85%
            • PNB: 8.35% - 9.90%
            • Axis Bank: 10.70% - 11.70%
            
            These rates may vary based on:
            • Loan amount
            • Course and institution
            • Your co-applicant's profile
            • Collateral provided
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "business": """
            📊 Current Business Loan Interest Rates (2024):
            
            • SBI: 10.50% - 16.25%
            • HDFC: 14.00% - 19.00%
            • ICICI: 16.00% - 18.00%
            • Axis Bank: 16.00% - 21.00%
            • Bank of Baroda: 10.50% - 15.50%
            
            These rates may vary based on:
            • Business vintage
            • Annual turnover
            • Credit score
            • Collateral provided
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "home": """
            📊 Current Home Loan Interest Rates (2024):
            
            • SBI: 8.40% - 9.10%
            • HDFC: 8.45% - 9.25%
            • ICICI: 8.50% - 9.25%
            • LIC Housing: 8.40% - 8.95%
            • Bank of Baroda: 8.40% - 9.30%
            
            These rates may vary based on:
            • Loan amount
            • Property value
            • Your credit score
            • Employment type
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "personal": """
            📊 Current Personal Loan Interest Rates (2024):
            
            • SBI: 10.50% - 16.50%
            • HDFC: 10.50% - 21.00%
            • ICICI: 10.50% - 18.49%
            • Axis Bank: 10.49% - 22.00%
            • Bank of Baroda: 10.15% - 15.90%
            
            These rates may vary based on:
            • Loan amount
            • Your credit score
            • Income and employment stability
            • Existing relationship with bank
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "vehicle": """
            📊 Current Vehicle Loan Interest Rates (2024):
            
            • SBI: 7.70% - 8.45% (new cars)
            • HDFC: 7.80% - 8.80% (new cars)
            • ICICI: 7.50% - 9.00% (new cars)
            • Axis Bank: 7.70% - 11.75% (new/used)
            • Bank of Baroda: 7.35% - 8.85% (new cars)
            
            These rates may vary based on:
            • Vehicle type (new/used)
            • Loan tenure
            • Your credit score
            • Employment type
            
            Would you like to check your eligibility or learn about the application process?
            """
        }
        return info.get(loan_type, info["personal"])

    def _get_document_info(self, loan_type: str) -> str:
        """Provide document information."""
        info = {
            "education": """
            📋 Documents Required for Education Loans:
            
            Student Documents:
            • Identity & Address proof (Aadhaar, PAN, etc.)
            • Academic records (10th, 12th, graduation)
            • Admission letter from institution
            • Course fee structure
            • Photographs
            
            Co-Applicant Documents:
            • Identity & Address proof
            • Income proof (salary slips, tax returns)
            • Bank statements (6 months)
            • Employment details
            
            For Loans Above ₹4 Lakhs (Additional):
            • Collateral documents (property papers, etc.)
            • Guarantor documents
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "business": """
            📋 Documents Required for Business Loans:
            
            Personal Documents:
            • Identity & Address proof (Aadhaar, PAN, etc.)
            • Photographs
            
            Business Documents:
            • Business registration certificate
            • GST registration (if applicable)
            • Business license/permits
            • Business address proof
            
            Financial Documents:
            • Income tax returns (2 years)
            • Financial statements (2 years)
            • Bank statements (12 months)
            • GST returns (if applicable)
            
            For Secured Loans (Additional):
            • Collateral documents
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "home": """
            📋 Documents Required for Home Loans:
            
            Personal Documents:
            • Identity & Address proof (Aadhaar, PAN, etc.)
            • Photographs
            
            Income Documents:
            • Salary slips (3 months)
            • Form 16 / Income tax returns
            • Bank statements (6 months)
            • Employment verification
            
            Property Documents:
            • Sale deed/agreement
            • Property valuation report
            • NOC from builder/society
            • Approved building plan
            • Property insurance
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "personal": """
            📋 Documents Required for Personal Loans:
            
            Personal Documents:
            • Identity proof (Aadhaar, PAN, passport)
            • Address proof (utility bill, passport)
            • Photographs
            
            Income Documents:
            • Salary slips (3 months)
            • Form 16 / Income tax returns
            • Bank statements (6 months)
            • Employment verification
            
            Additional Documents (if applicable):
            • Existing loan statements
            • Credit card statements
            
            Would you like to check your eligibility or learn about the application process?
            """,
            "vehicle": """
            📋 Documents Required for Vehicle Loans:
            
            Personal Documents:
            • Identity proof (Aadhaar, PAN, passport)
            • Address proof (utility bill, passport)
            • Photographs
            • Driving license
            
            Income Documents:
            • Salary slips (3 months)
            • Form 16 / Income tax returns
            • Bank statements (6 months)
            • Employment verification
            
            Vehicle Documents:
            • Vehicle quotation from dealer
            • Proforma invoice
            • Registration certificate (for used vehicles)
            
            Would you like to check your eligibility or learn about the application process?
            """
        }
        return info.get(loan_type, info["personal"])

    def _get_process_info(self, loan_type: str) -> str:
        """Provide application process information."""
        info = {
            "education": """
            🔄 Education Loan Application Process:
            
            1. Pre-Application:
               • Secure admission to your institution
               • Research banks and compare offers
               • Check eligibility requirements
            
            2. Application:
               • Visit bank branch with co-applicant
               • Fill application form
               • Submit required documents
               • Pay application fee (if any)
            
            3. Verification:
               • Bank verifies documents
               • Check of co-applicant's credentials
               • Verification of institution
            
            4. Approval & Disbursement:
               • Receive approval letter
               • Sign loan agreement
               • Loan amount disbursed directly to institution
            
            Timeline: Usually 1-2 weeks from complete application
            
            Would you like to check your eligibility or learn about the documents required?
            """,
            "business": """
            🔄 Business Loan Application Process:
            
            1. Pre-Application:
               • Prepare business plan and projections
               • Research banks and compare offers
               • Check eligibility requirements
            
            2. Application:
               • Visit bank branch or apply online
               • Fill application form
               • Submit required documents
               • Pay application fee (if any)
            
            3. Verification:
               • Bank verifies documents
               • Business site visit (in some cases)
               • Assessment of business viability
            
            4. Approval & Disbursement:
               • Receive approval letter
               • Sign loan agreement
               • Loan amount disbursed to business account
            
            Timeline: Usually 1-3 weeks from complete application
            
            Would you like to check your eligibility or learn about the documents required?
            """,
            "home": """
            🔄 Home Loan Application Process:
            
            1. Pre-Application:
               • Select property
               • Research banks and compare offers
               • Check eligibility and pre-approval
            
            2. Application:
               • Visit bank branch or apply online
               • Fill application form
               • Submit required documents
               • Pay application fee
            
            3. Verification:
               • Bank verifies documents
               • Legal verification of property
               • Technical valuation of property
            
            4. Approval & Disbursement:
               • Receive approval letter
               • Sign loan agreement
               • Loan amount disbursed to seller/builder
            
            Timeline: Usually 2-4 weeks from complete application
            
            Would you like to check your eligibility or learn about the documents required?
            """,
            "personal": """
            🔄 Personal Loan Application Process:
            
            1. Pre-Application:
               • Check your credit score
               • Research banks and compare offers
               • Check eligibility requirements
            
            2. Application:
               • Visit bank branch or apply online
               • Fill application form
               • Submit required documents
               • Pay application fee (if any)
            
            3. Verification:
               • Bank verifies documents
               • Income and employment verification
               • Credit assessment
            
            4. Approval & Disbursement:
               • Receive approval letter
               • Sign loan agreement
               • Loan amount disbursed to your account
            
            Timeline: Usually 2-5 business days from complete application
            
            Would you like to check your eligibility or learn about the documents required?
            """,
            "vehicle": """
            🔄 Vehicle Loan Application Process:
            
            1. Pre-Application:
               • Select vehicle and dealer
               • Research banks and compare offers
               • Check eligibility requirements
            
            2. Application:
               • Visit bank, dealership, or apply online
               • Fill application form
               • Submit required documents
               • Pay application fee (if any)
            
            3. Verification:
               • Bank verifies documents
               • Income and employment verification
               • Vehicle inspection (for used vehicles)
            
            4. Approval & Disbursement:
               • Receive approval letter
               • Sign loan agreement
               • Loan amount disbursed to dealer
            
            Timeline: Usually 1-3 business days from complete application
            
            Would you like to check your eligibility or learn about the documents required?
            """
        }
        return info.get(loan_type, info["personal"])

    def _get_emi_info(self, loan_type: str) -> str:
        """Provide EMI calculation information."""
        from math import pow
        
        # Default loan parameters by loan type
        defaults = {
            "education": {"amount": 500000, "rate": 9.0, "years": 7},
            "business": {"amount": 1000000, "rate": 12.0, "years": 5},
            "home": {"amount": 3000000, "rate": 8.5, "years": 20},
            "personal": {"amount": 500000, "rate": 12.0, "years": 3},
            "vehicle": {"amount": 700000, "rate": 9.0, "years": 5}
        }
        
        # Get defaults for the loan type
        params = defaults.get(loan_type, defaults["personal"])
        
        # Calculate EMI
        p = params["amount"]  # principal
        r = params["rate"] / (12 * 100)  # monthly interest rate
        n = params["years"] * 12  # number of installments
        
        # EMI formula: P * r * (1+r)^n / ((1+r)^n - 1)
        emi = p * r * pow(1 + r, n) / (pow(1 + r, n) - 1)
        
        # Total calculations
        total_payment = emi * n
        total_interest = total_payment - p
        
        return f"""
        💰 Sample {loan_type.title()} Loan EMI Calculation:
        
        For a loan of ₹{p:,.2f} at {params["rate"]}% for {params["years"]} years:
        
        • Monthly EMI: ₹{emi:,.2f}
        • Total Payment: ₹{total_payment:,.2f}
        • Total Interest: ₹{total_interest:,.2f}
        
        Factors affecting your EMI:
        • Loan amount: Higher amount → higher EMI
        • Interest rate: Higher rate → higher EMI
        • Loan tenure: Longer tenure → lower EMI but more total interest
        
        To calculate EMI for different parameters:
        EMI = P × r × (1+r)^n / ((1+r)^n-1)
        where:
        P = Principal, r = monthly interest rate, n = number of installments
        
        Would you like to check your eligibility or learn about the application process?
        """

    def _get_general_info(self, loan_type: str) -> str:
        """Provide general information about loan types."""
        info = {
            "education": """
            📚 Education Loan Information:
            
            Education loans help fund higher education expenses including tuition fees, books, equipment, accommodation, and other study-related costs.
            
            💰 Key Features:
            • Loan amounts: ₹50,000 to ₹75 lakhs
            • Interest rates: 8.15% to 15.20%
            • Repayment period: Up to 15 years
            • Moratorium period: Course duration + 6-12 months
            • Tax benefits under Section 80E
            
            ✅ General Eligibility:
            • Indian citizen
            • Admission to recognized institution
            • For loans above ₹4 lakhs: Collateral typically required
            
            🏦 Top Banks for Education Loans:
            • SBI
            • Bank of Baroda
            • HDFC Bank
            • Axis Bank
            • Punjab National Bank
            
            Would you like specific information about interest rates, documents required, or the application process? Or would you like to check your eligibility?
            """,
            "business": """
            💼 Business Loan Information:
            
            Business loans provide financing for business expansion, equipment purchase, working capital needs, and other business requirements.
            
            💰 Key Features:
            • Loan amounts: ₹1 lakh to ₹50 lakhs (unsecured)
            • Interest rates: 10.50% to 18.00%
            • Repayment period: 1 to 7 years (typically)
            • Processing fee: 1-2% of loan amount
            • Flexible repayment options
            
            ✅ General Eligibility:
            • Business age: Minimum 1-2 years of operation
            • Minimum annual turnover requirements
            • Good credit score (typically 700+)
            
            🏦 Top Banks for Business Loans:
            • SBI
            • HDFC Bank
            • ICICI Bank
            • Axis Bank
            • Bank of Baroda
            
            Would you like specific information about interest rates, documents required, or the application process? Or would you like to check your eligibility?
            """,
            "home": """
            🏠 Home Loan Information:
            
            Home loans finance the purchase, construction, or renovation of residential property.
            
            💰 Key Features:
            • Loan amounts: Up to ₹5 crores
            • Interest rates: 8.40% to 9.80%
            • Repayment period: Up to 30 years
            • Loan-to-Value ratio: Up to 80% of property value
            • Tax benefits under Section 80C and 24(b)
            
            ✅ General Eligibility:
            • Age: 23-65 years
            • Stable income source
            • Good credit score (typically 750+)
            • Property with clear title
            
            🏦 Top Banks for Home Loans:
            • SBI
            • HDFC Bank
            • ICICI Bank
            • LIC Housing Finance
            • Axis Bank
            
            Would you like specific information about interest rates, documents required, or the application process? Or would you like to check your eligibility?
            """,
            "personal": """
            💳 Personal Loan Information:
            
            Personal loans are unsecured loans for various personal needs like medical expenses, travel, weddings, or debt consolidation.
            
            💰 Key Features:
            • Loan amounts: ₹50,000 to ₹40 lakhs
            • Interest rates: 10.50% to 18.00%
            • Repayment period: 1 to 5 years
            • Processing fee: 1-3% of loan amount
            • No collateral required
            
            ✅ General Eligibility:
            • Age: 21-60 years
            • Minimum income requirements
            • Good credit score (typically 700+)
            • Employment stability (1-2 years)
            
            🏦 Top Banks for Personal Loans:
            • SBI
            • HDFC Bank
            • ICICI Bank
            • Axis Bank
            • Bajaj Finserv
            
            Would you like specific information about interest rates, documents required, or the application process? Or would you like to check your eligibility?
            """,
            "vehicle": """
            🚗 Vehicle Loan Information:
            
            Vehicle loans help finance the purchase of cars, two-wheelers, or other vehicles.
            
            💰 Key Features:
            • Loan amounts: Up to 90% of vehicle cost
            • Interest rates: 7.75% to 12.50%
            • Repayment period: Up to 7 years
            • Processing fee: 0.5-1.5% of loan amount
            • Quick approval process
            
            ✅ General Eligibility:
            • Age: 21-65 years
            • Minimum income requirements
            • Good credit score (typically 650+)
            • Employment stability
            
            🏦 Top Banks for Vehicle Loans:
            • SBI
            • HDFC Bank
            • ICICI Bank
            • Axis Bank
            • Bank of Baroda
            
            Would you like specific information about interest rates, documents required, or the application process? Or would you like to check your eligibility?
            """
        }
        return info.get(loan_type, info["personal"])

    def get_next_question(self) -> str:
        """Get the next question based on loan type and current step."""
        loan_type = self.current_state.get("loan_type", "personal")
        step = self.current_state.get("step", 0)

        questions = {
            "education": {
                1: "What's your name?",
                2: "Which course do you want to study? (Like B.Tech, MBA, BBA, etc.)",
                3: "How long is this course? (For example: 2 years, 4 years)",
                4: "Which college or university are you planning to attend?",
                5: "What's the total course fee? Just the amount in rupees is fine.",
                6: "Who will be your co-applicant for this loan? (Usually a parent - please share their name and job)"
            },
            "business": {
                1: "What's your business name?",
                2: "What type of business is it? (Manufacturing, Service, Retail, etc.)",
                3: "How long has your business been operating?",
                4: "What's your annual turnover?",
                5: "How much loan amount are you looking for?",
                6: "Do you have any collateral to offer? Please provide details."
            },
            "home": {
                1: "What's your name?",
                2: "What's the value of the property you're interested in?",
                3: "Where is the property located?",
                4: "How much loan amount are you looking for?",
                5: "What's your monthly income?",
                6: "Please share your employment details (company name and years of experience)."
            },
            "personal": {
                1: "What's your name?",
                2: "What's your monthly income?",
                3: "Please share your employment details (company name and years of experience).",
                4: "How much loan amount are you looking for?",
                5: "What's the purpose of the loan?",
                6: "Do you have any existing loans? Please provide details."
            },
            "vehicle": {
                1: "What's your name?",
                2: "Which vehicle are you planning to purchase? (Car/Bike/Make/Model)",
                3: "What's the on-road price of the vehicle?",
                4: "How much down payment can you make?",
                5: "What's your monthly income?",
                6: "Please share your employment details (company name and years of experience)."
            }
        }

        return questions.get(loan_type, {}).get(step, "Thanks! Let me check everything for you.")

    def update_state(self, message: str) -> Optional[str]:
        """Update state based on user response."""
        try:
            if not isinstance(message, str):
                message = str(message)
                
            message_lower = message.lower()
            loan_type = self.current_state.get("loan_type", "personal")
            step = self.current_state.get("step", 0)

            # Handle user declining to proceed with eligibility check
            if step == 0 and any(word in message_lower for word in ["no", "nope", "don't", "dont", "not now", "later"]):
                self.current_state = {}
                return f"""No problem! I can provide general information about {loan_type} loans instead.
                
                {self._get_loan_information(loan_type, "")}
                """
                
            # User agrees to proceed with eligibility check
            if step == 0:
                if any(word in message_lower for word in ["yes", "yeah", "sure", "proceed", "ok", "okay", "go ahead"]):
                    self.current_state["step"] = 1
                    return self.get_next_question()
                else:
                    return f"""Do you want to proceed with checking your eligibility for a {loan_type} loan? 
                    Please reply with Yes or No."""

            # Process information for eligibility check
            field = self.required_fields[loan_type][step - 1]
            self.current_state[field] = message
            
            if step < len(self.required_fields[loan_type]):
                self.current_state["step"] = step + 1
                return None
            
            return self.evaluate_loan_eligibility()
            
        except Exception as e:
            print(f"Error updating state: {str(e)}")
            self.current_state = {}
            return """I apologize, but I encountered an issue. Let's start over.
            What type of loan are you interested in?"""

    def evaluate_loan_eligibility(self) -> str:
        """Evaluate loan eligibility with organized response."""
        try:
            loan_type = self.current_state.get("loan_type", "personal")
            
            # Save application data
            self.update_user_data("latest", self.current_state)

            # Get real-time loan data
            try:
                search_query = f"current {loan_type} loan interest rates india banks 2024"
                messages = [{"role": "user", "content": f"Find current {loan_type} loan details in India including interest rates and eligibility criteria. Format as JSON."}]
                loan_data = self.get_completion(messages, temperature=0.2)
            except Exception as e:
                print(f"Error fetching loan data: {str(e)}")
                loan_data = {}

            # Format response based on loan type
            responses = {
                "education": self._format_education_response,
                "business": self._format_business_response,
                "home": self._format_home_response,
                "personal": self._format_personal_response,
                "vehicle": self._format_vehicle_response
            }

            return responses.get(loan_type, self._format_personal_response)()
            
        except Exception as e:
            print(f"Error evaluating eligibility: {str(e)}")
            return """I apologize, but I encountered an issue while evaluating your loan eligibility.
            This could be due to missing or invalid information. Would you like to:
            1. Try again with the same loan type
            2. Start over with a different loan type
            Please let me know your preference."""

    def _format_education_response(self) -> str:
        """Format education loan response."""
        name = self.current_state.get("student_name", "")
        course = self.current_state.get("course_name", "")
        college = self.current_state.get("college_name", "")
        fee = self.current_state.get("course_fee", 0)

        return f"""
        Great news, {name}! 🎓 Based on what you've shared:

        • Course: {course}
        • College: {college}
        • Fee: ₹{fee:,.2f}

        You're eligible to apply for an education loan! Here's what you need to know:

        📋 Documents needed:
           • Your ID proof (Aadhar card)
           • School/college marksheets
           • College admission letter
           • College fee structure
           • Your parent's ID and income proof

        💰 Loan benefits:
           • Up to 100% of your course fee covered
           • Extra money for books and laptop (up to ₹50,000)
           • No full EMI payments during your studies
           • Interest rates from 8% to 12% depending on the bank

        🏦 Next steps:
           1. Visit any bank with your parent/guardian
           2. Bring all documents listed above
           3. Fill out the application form
           4. The bank will process your application in 7-14 days

        Do you have any specific questions about your education loan? I'm here to help! 😊
        """

    def _format_business_response(self) -> str:
        """Format business loan response."""
        name = self.current_state.get("business_name", "")
        amount = self.current_state.get("loan_amount", 0)
        turnover = self.current_state.get("annual_turnover", 0)

        return f"""
        Good news about your business loan request for {name}! 💼

        Based on your details:
        • Annual Turnover: ₹{turnover:,.2f}
        • Requested Amount: ₹{amount:,.2f}

        Here's what you need to know:

        📋 Required Documents:
           • Business registration documents
           • Last 2 years' financial statements
           • GST returns
           • Bank statements (12 months)
           • KYC documents
           • Collateral documents (if applicable)

        💰 Loan Details:
           • Loan amount up to 75% of annual turnover
           • Interest rates from 11% to 16%
           • Flexible repayment terms up to 15 years
           • Processing fee: 1-2% of loan amount

        🏦 Next Steps:
           1. Prepare all documents
           2. Visit preferred bank's business branch
           3. Submit application with documents
           4. Business verification (2-3 working days)
           5. Loan approval (7-14 working days)

        Need help with the application process? Just ask! 😊
        """

    def _format_home_response(self) -> str:
        """Format home loan response."""
        name = self.current_state.get("applicant_name", "")
        property_value = self.current_state.get("property_value", 0)
        loan_amount = self.current_state.get("loan_amount", 0)
        location = self.current_state.get("property_location", "")

        return f"""
        Excellent news about your home loan request, {name}! 🏠

        Property Details:
        • Location: {location}
        • Value: ₹{property_value:,.2f}
        • Loan Amount: ₹{loan_amount:,.2f}

        Here's what you need to know:

        📋 Required Documents:
           • Identity & Address proof
           • Income proof (salary slips/ITR)
           • 6 months' bank statements
           • Property documents
           • Employment proof
           • Processing fee cheque

        💰 Loan Features:
           • Up to 80% of property value
           • Interest rates from 8.40% to 9.80%
           • Tenure up to 30 years
           • Tax benefits under Section 80C & 24(b)

        🏦 Next Steps:
           1. Document submission
           2. Property legal verification
           3. Technical verification
           4. Final approval
           5. Loan disbursement

        Want to calculate your EMI or know more about the process? Just ask! 🏠
        """

    def _format_personal_response(self) -> str:
        """Format personal loan response."""
        name = self.current_state.get("applicant_name", "")
        income = self.current_state.get("income", 0)
        amount = self.current_state.get("loan_amount", 0)
        purpose = self.current_state.get("purpose", "")

        return f"""
        Good news about your personal loan request, {name}! 💰

        Loan Details:
        • Purpose: {purpose}
        • Amount Requested: ₹{amount:,.2f}
        • Monthly Income: ₹{income:,.2f}

        Here's what you need to know:

        📋 Required Documents:
           • Identity proof (Aadhar/PAN)
           • Address proof
           • 3 months' salary slips
           • 6 months' bank statements
           • Form 16/ITR
           • Processing fee cheque

        💰 Loan Features:
           • Quick approval process
           • No collateral required
           • Interest rates from 10.50% to 18%
           • Flexible tenure options (1-5 years)
           • No prepayment charges after 12 months

        🏦 Next Steps:
           1. Document submission
           2. Income verification
           3. Credit score check
           4. Loan approval (2-3 working days)
           5. Amount disbursement

        Need help calculating your EMI or understanding the terms? Just ask! 💳
        """

    def _format_vehicle_response(self) -> str:
        """Format vehicle loan response."""
        name = self.current_state.get("applicant_name", "")
        vehicle = self.current_state.get("vehicle_type", "")
        cost = self.current_state.get("vehicle_cost", 0)
        down_payment = self.current_state.get("down_payment", 0)

        loan_amount = cost - down_payment

        return f"""
        Great news about your vehicle loan request, {name}! 🚗

        Vehicle Details:
        • Type: {vehicle}
        • Cost: ₹{cost:,.2f}
        • Down Payment: ₹{down_payment:,.2f}
        • Loan Amount: ₹{loan_amount:,.2f}

        Here's what you need to know:

        📋 Required Documents:
           • Identity proof
           • Address proof
           • Income proof
           • Bank statements (3 months)
           • Vehicle quotation
           • Processing fee cheque

        💰 Loan Features:
           • Up to 90% of vehicle cost
           • Interest rates from 7.75% to 12.50%
           • Tenure up to 7 years
           • Quick approval process
           • Flexible EMI options

        🏦 Next Steps:
           1. Document submission
           2. Vehicle evaluation
           3. Loan approval (1-2 working days)
           4. Vehicle registration
           5. Loan disbursement

        Want to calculate your EMI or know more about insurance options? Just ask! 🚗
        """ 