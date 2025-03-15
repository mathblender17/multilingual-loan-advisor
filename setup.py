from setuptools import setup, find_packages

setup(
    name="loan_advisor",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "langchain==0.1.12",
        "langchain-groq==0.0.1",
        "python-dotenv==1.0.1",
        "pydantic==2.6.3",
        "rich==13.7.0"
    ],
    python_requires=">=3.8",
) 