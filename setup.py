from setuptools import setup, find_packages

setup(
    name="multi_agent_system",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9,<3.12",
    install_requires=[
        # LangChain core dependencies
        "langchain==0.3.25",
        "langchain-core==0.3.65",
        "langchain-community==0.3.25",
        "langchain-experimental==0.3.0",
        "langchain-openai==0.3.23",
        # Graph dependencies
        "neo4j>=5.14.0",
        "networkx>=3.2.0",
        # LLM dependencies
        "openai>=1.0.0",
        # Data processing
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "matplotlib>=3.7.0",
        "scikit-learn>=1.3.0",
        # Async support
        "aiohttp>=3.9.0",
        "asyncio>=3.4.3",
    ],
    extras_require={
        "develop": [
            "ruff>=0.1.0",
            "black>=23.0.0",
            "pre-commit>=3.0.0",
            "pytest>=7.0.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.12.0",
            "uv>=0.1.0",
            "ipykernel>=6.0.0",
            "jupyter>=1.0.0",
        ]
    },
)
