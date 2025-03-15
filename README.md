# Multilingual Conversational Loan Advisor

A Python-based conversational AI system that helps users with loan-related queries, eligibility checks, and financial advice. The system uses OpenAI's GPT models for natural language processing and provides context-aware responses.

## Features

- **Intent Classification**: Automatically routes user queries to the appropriate specialized agent
- **Loan Eligibility Check**: Evaluates loan eligibility based on Indian banking sector rules
- **Loan Application Guide**: Provides step-by-step guidance through the loan application process
- **Financial Literacy Coach**: Offers simple financial advice and explanations
- **Local Data Storage**: Stores user interactions and preferences in JSON format
- **Rich Terminal Interface**: User-friendly command-line interface with colored output

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd loan-advisor
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Start the Loan Advisor:
```bash
python -m loan_advisor.main
```

2. Follow the interactive prompts to:
- Check loan eligibility
- Get guidance on loan applications
- Learn about financial concepts
- Receive personalized financial advice

3. Type 'exit', 'quit', or 'bye' to end the session

## Example Interactions

```
You: I need a business loan
Advisor: Sure! Let's check your eligibility first. What is your employment status?

You: I own a small shop
Advisor: Great! What is your approximate monthly income?

You: Around 50,000 INR
Advisor: Thanks! Do you know your credit score?
```

## Project Structure

```
loan_advisor/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── intent_classifier.py
│   ├── loan_eligibility.py
│   ├── loan_application.py
│   └── financial_literacy.py
├── data/
│   └── user_data.json
├── config.py
└── main.py
```

## Future Enhancements

- Web-based interface
- MongoDB integration for data storage
- Multilingual support (Hindi, Tamil, etc.)
- Integration with credit score APIs
- Real-time interest rate updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 