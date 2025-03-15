from typing import Dict, Any, Optional
import json
from datetime import datetime, timedelta
import requests

class LoanDataFetcher:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache data for 1 hour

    def get_loan_data(self, loan_type: str) -> Dict[str, Any]:
        """Get real-time loan data with caching."""
        now = datetime.now()
        
        # Check cache first
        if loan_type in self.cache:
            data, timestamp = self.cache[loan_type]
            if now - timestamp < self.cache_duration:
                return data

        # Fetch fresh data
        try:
            data = self._fetch_loan_data(loan_type)
            self.cache[loan_type] = (data, now)
            return data
        except Exception as e:
            print(f"Error fetching loan data: {e}")
            return self._get_fallback_data(loan_type)

    def _fetch_loan_data(self, loan_type: str) -> Dict[str, Any]:
        """Fetch real-time loan data from various sources."""
        # This would typically involve API calls to banks or financial data providers
        # For now, we'll use default data with real-time updates where possible
        
        # Example API call (commented out as it requires API key)
        # response = requests.get(
        #     "https://api.example.com/loan-rates",
        #     params={"type": loan_type},
        #     headers={"Authorization": "Bearer YOUR_API_KEY"}
        # )
        # return response.json()

        return self._get_fallback_data(loan_type)

    def _get_fallback_data(self, loan_type: str) -> Dict[str, Any]:
        """Get fallback data when real-time data is unavailable."""
        default_data = {
            "education": {
                "interest_range": "8.15% - 15.20%",
                "processing_fee": "0.5% - 1%",
                "loan_amount": "Up to ₹75 lakhs",
                "tenure": "Up to 15 years",
                "eligibility": {
                    "age": "18-35 years",
                    "course_type": "Recognized full-time courses",
                    "collateral": "Required for loans above ₹7.5 lakhs",
                    "co_applicant": "Required (Usually parent/guardian)"
                },
                "documents": [
                    "Identity proof",
                    "Address proof",
                    "Academic records",
                    "Admission letter",
                    "Course fee structure",
                    "Co-applicant documents"
                ],
                "top_banks": [
                    {"name": "SBI", "rate": "8.15%"},
                    {"name": "HDFC", "rate": "8.35%"},
                    {"name": "ICICI", "rate": "8.50%"},
                    {"name": "Bank of Baroda", "rate": "8.80%"},
                    {"name": "Axis Bank", "rate": "9.00%"}
                ]
            },
            "business": {
                "interest_range": "10.50% - 18.00%",
                "processing_fee": "1% - 2%",
                "loan_amount": "Up to ₹50 lakhs",
                "tenure": "Up to 15 years",
                "eligibility": {
                    "business_age": "Minimum 2 years",
                    "turnover": "Minimum ₹10 lakhs per year",
                    "credit_score": "Above 700",
                    "collateral": "Required for loans above ₹25 lakhs"
                },
                "documents": [
                    "Business registration proof",
                    "GST returns",
                    "Income tax returns",
                    "Bank statements",
                    "KYC documents",
                    "Business plan"
                ],
                "top_banks": [
                    {"name": "SBI", "rate": "10.50%"},
                    {"name": "HDFC", "rate": "11.20%"},
                    {"name": "ICICI", "rate": "11.50%"},
                    {"name": "Axis Bank", "rate": "12.00%"},
                    {"name": "Bank of Baroda", "rate": "12.50%"}
                ]
            },
            "home": {
                "interest_range": "8.40% - 9.80%",
                "processing_fee": "0.5% - 1%",
                "loan_amount": "Up to ₹5 crores",
                "tenure": "Up to 30 years",
                "eligibility": {
                    "age": "23-65 years",
                    "income": "Minimum ₹25,000 per month",
                    "credit_score": "Above 750",
                    "property": "Clear title and approvals"
                },
                "documents": [
                    "Identity proof",
                    "Address proof",
                    "Income proof",
                    "Property documents",
                    "Bank statements",
                    "Employment proof"
                ],
                "top_banks": [
                    {"name": "SBI", "rate": "8.40%"},
                    {"name": "HDFC", "rate": "8.50%"},
                    {"name": "ICICI", "rate": "8.60%"},
                    {"name": "LIC Housing", "rate": "8.65%"},
                    {"name": "Axis Bank", "rate": "8.75%"}
                ]
            },
            "personal": {
                "interest_range": "10.50% - 18.00%",
                "processing_fee": "1% - 3%",
                "loan_amount": "Up to ₹40 lakhs",
                "tenure": "Up to 5 years",
                "eligibility": {
                    "age": "21-60 years",
                    "income": "Minimum ₹20,000 per month",
                    "credit_score": "Above 700",
                    "employment": "Minimum 2 years"
                },
                "documents": [
                    "Identity proof",
                    "Address proof",
                    "Income proof",
                    "Bank statements",
                    "Employment proof"
                ],
                "top_banks": [
                    {"name": "SBI", "rate": "10.50%"},
                    {"name": "HDFC", "rate": "10.75%"},
                    {"name": "ICICI", "rate": "11.00%"},
                    {"name": "Axis Bank", "rate": "11.25%"},
                    {"name": "Bajaj Finserv", "rate": "11.50%"}
                ]
            },
            "vehicle": {
                "interest_range": "7.75% - 12.50%",
                "processing_fee": "0.5% - 1.5%",
                "loan_amount": "Up to ₹1 crore",
                "tenure": "Up to 8 years",
                "eligibility": {
                    "age": "21-65 years",
                    "income": "Minimum ₹15,000 per month",
                    "credit_score": "Above 650",
                    "down_payment": "10-20% of vehicle cost"
                },
                "documents": [
                    "Identity proof",
                    "Address proof",
                    "Income proof",
                    "Bank statements",
                    "Vehicle quotation",
                    "Driving license"
                ],
                "top_banks": [
                    {"name": "SBI", "rate": "7.75%"},
                    {"name": "HDFC", "rate": "8.00%"},
                    {"name": "ICICI", "rate": "8.25%"},
                    {"name": "Axis Bank", "rate": "8.50%"},
                    {"name": "Bank of Baroda", "rate": "8.75%"}
                ]
            }
        }
        
        return default_data.get(loan_type, {})

    def get_emi_calculation(self, principal: float, rate: float, tenure_years: float) -> Dict[str, Any]:
        """Calculate EMI and loan details."""
        rate_monthly = rate / (12 * 100)  # Convert annual rate to monthly
        tenure_months = tenure_years * 12
        
        emi = (principal * rate_monthly * (1 + rate_monthly)**tenure_months) / ((1 + rate_monthly)**tenure_months - 1)
        
        total_amount = emi * tenure_months
        total_interest = total_amount - principal
        
        return {
            "emi": round(emi, 2),
            "total_amount": round(total_amount, 2),
            "total_interest": round(total_interest, 2),
            "interest_rate": rate,
            "tenure_years": tenure_years,
            "tenure_months": tenure_months
        } 