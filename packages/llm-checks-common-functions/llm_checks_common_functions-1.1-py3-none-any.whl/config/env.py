import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

azure_openai_url = os.getenv('Azure_openai_url')
azure_openai_key = os.getenv('Azure_openai_key')

NVidia_trial_url = os.getenv('NVidia_trial_url')
NVidia_trial_key = os.getenv('NVidia_trial_key')

openai_key = os.getenv('openai_key')

Gemini_key = os.getenv('Gemini_key')



cosmos_db_connection_string = os.getenv('cosmos_db_connection_string')