from setuptools import setup, find_packages

setup(
    name='llm_checks_common_functions',
    version='1.1',
    packages=find_packages(),
    install_requires=["langchain==0.2.11", "langchain-community", "openpyxl==3.1.2", "pandas==2.2.1", "PyYAML", "tqdm==4.66.2",
                      "azure-cosmos", "azure-storage-blob", "python-dotenv", "openai==0.28", "langchain-nvidia-ai-endpoints", 
                      "google-generativeai", "boto3", "SQLAlchemy==2.0.29", "mysql-connector", "xlsxwriter", "tiktoken"],
    author='Karthik M',
    author_email='karthik.manne@centific.com',
    description='common functions, utilities using multiple DB and LLM options.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://pactera1us.visualstudio.com/DefaultCollection/LLM_CoE/_git/redteaming_service',  # Update this to your repository URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
