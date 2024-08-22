import yaml

from openai import OpenAI



def load_config(file_path='./config/config.yaml'):
   with open(file_path, 'r') as file:
       config = yaml.safe_load(file)
   return config
    
config = load_config()


def get_nvidia_model():

   client = OpenAI(
   base_url = "https://integrate.api.nvidia.com/v1",
   api_key = "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"
   )

   return client
