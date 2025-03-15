from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LanguageDetectionTool(BaseTool):
    name: str = "Language Detection"
    description: str = "Detects the language of the user's input"

    def _run(self, query: str) -> str:
        return "Detect language of input"

class IntentClassificationTool(BaseTool):
    name: str = "Intent Classification"
    description: str = "Classifies the user's intent into categories"

    def _run(self, query: str) -> str:
        return "Classify user intent"

class IncomeAnalysisTool(BaseTool):
    name: str = "Income Analysis"
    description: str = "Analyzes user's income information"

    def _run(self, query: str) -> str:
        return "Analyze income information"

class CreditScoreTool(BaseTool):
    name: str = "Credit Score Evaluation"
    description: str = "Evaluates user's credit score"

    def _run(self, query: str) -> str:
        return "Evaluate credit score"

class DocumentChecklistTool(BaseTool):
    name: str = "Document Checklist"
    description: str = "Generates a checklist of required documents"

    def _run(self, query: str) -> str:
        return "Generate document checklist"

class ApplicationStepsTool(BaseTool):
    name: str = "Application Steps"
    description: str = "Provides step-by-step application guidance"

    def _run(self, query: str) -> str:
        return "Provide application steps"

class FinancialEducationTool(BaseTool):
    name: str = "Financial Education"
    description: str = "Provides educational content about financial concepts"

    def _run(self, query: str) -> str:
        return "Provide financial education"

class PersonalizedAdviceTool(BaseTool):
    name: str = "Personalized Advice"
    description: str = "Generates personalized financial advice"

    def _run(self, query: str) -> str:
        return "Generate personalized advice"

class LoanAdvisorAgents:
    def __init__(self):
        # Initialize the Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def create_intent_classifier_agent(self) -> Agent:
        return Agent(
            role='Intent Classifier & Router',
            goal='Accurately identify user intent and language, then route to appropriate specialized agent',
            backstory="""You are an expert in natural language processing and multilingual communication.
            Your primary responsibility is to understand user queries, identify their intent, and ensure they
            are directed to the most appropriate specialized agent.""",
            tools=[LanguageDetectionTool(), IntentClassificationTool()],
            llm=self.llm,
            verbose=True
        )

    def create_eligibility_checker_agent(self) -> Agent:
        return Agent(
            role='Loan Eligibility Checker',
            goal='Evaluate user eligibility for various loan types and provide preliminary assessment',
            backstory="""You are a financial expert specializing in loan eligibility assessment.
            You analyze user information to determine their eligibility for different types of loans
            and provide detailed feedback.""",
            tools=[IncomeAnalysisTool(), CreditScoreTool()],
            llm=self.llm,
            verbose=True
        )

    def create_application_guide_agent(self) -> Agent:
        return Agent(
            role='Loan Application Guide',
            goal='Guide users through the loan application process and explain required documentation',
            backstory="""You are an experienced loan application specialist who helps users
            navigate the complex loan application process. You provide clear, step-by-step guidance
            and explain all required documentation.""",
            tools=[DocumentChecklistTool(), ApplicationStepsTool()],
            llm=self.llm,
            verbose=True
        )

    def create_financial_literacy_agent(self) -> Agent:
        return Agent(
            role='Financial Literacy Coach',
            goal='Educate users about financial concepts and provide personalized financial advice',
            backstory="""You are a financial education expert who helps users understand
            financial concepts and make informed decisions. You provide personalized advice
            and educational resources.""",
            tools=[FinancialEducationTool(), PersonalizedAdviceTool()],
            llm=self.llm,
            verbose=True
        )

    def create_crew(self, user_query: str) -> Crew:
        # Create all agents
        intent_classifier = self.create_intent_classifier_agent()
        eligibility_checker = self.create_eligibility_checker_agent()
        application_guide = self.create_application_guide_agent()
        financial_literacy = self.create_financial_literacy_agent()

        # Create tasks
        tasks = [
            Task(
                description=f"Analyze the following user query and identify intent and language: {user_query}",
                agent=intent_classifier
            ),
            Task(
                description="Based on the intent classification, evaluate loan eligibility",
                agent=eligibility_checker
            ),
            Task(
                description="Provide loan application guidance based on eligibility assessment",
                agent=application_guide
            ),
            Task(
                description="Offer relevant financial education and advice",
                agent=financial_literacy
            )
        ]

        # Create and return the crew
        return Crew(
            agents=[intent_classifier, eligibility_checker, application_guide, financial_literacy],
            tasks=tasks,
            verbose=True
        ) 