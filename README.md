# Multilingual Conversational Loan Advisor

This project implements a multilingual conversational loan advisor system using CrewAI and Google's Gemini model. The system consists of four specialized agents working together to provide comprehensive loan advisory services.

## Agents

1. **Intent Classifier & Router Agent**
   - Identifies user intent and language
   - Routes queries to appropriate specialized agents
   - Handles multilingual communication

2. **Loan Eligibility Checker Agent**
   - Evaluates user's loan eligibility
   - Analyzes financial information
   - Provides preliminary assessment

3. **Loan Application Guide Agent**
   - Guides users through loan application process
   - Explains required documentation
   - Provides step-by-step assistance

4. **Financial Literacy Coach Agent**
   - Educates users about financial concepts
   - Provides personalized financial advice
   - Offers tips for better financial management

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python main.py
   ```

## Usage

The system accepts user queries in multiple languages and provides comprehensive loan advisory services. Each agent specializes in a specific aspect of the loan advisory process, working together to deliver a complete solution. 