# import os
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from openai import OpenAI


# class NvidiaModel:
#     def __init__(self):
#         self.base_url = "https://integrate.api.nvidia.com/v1"
#         self.api_key = os.getenv('NVIDIA_API_KEY')

#         self.client = OpenAI(
#           base_url = self.base_url,
#           api_key = self.api_key
#         )

#         self.GENERATE_RESPONSE_PROMPT = """
#                 Generate response to the following prompt:
#                 PROMPT: {prompt}
#                 """
#         self.prompt_template = PromptTemplate.from_template(self.GENERATE_RESPONSE_PROMPT)

#     def generate_response(self, input_prompt):
#         response=""
#         prompt_formatted_str = self.prompt_template.format(prompt=input_prompt)
    
#         completion = self.client.chat.completions.create(
#             model="nvidia/nemotron-4-340b-instruct",
#             messages=[{"role":"user","content":prompt_formatted_str}],
#             temperature=0,
#             top_p=0.7,
#             max_tokens=1024,
#             stream=False
#         )
#         response=completion.choices[0].message.content
#         return response



import os
import tiktoken
from langchain_core.prompts import PromptTemplate
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import find_dotenv, load_dotenv

# Get the absolute path to the config folder
config_dir = os.path.join(os.path.dirname(__file__), '../config')

# Construct the path to the .env file
dotenv_path = os.path.join(config_dir, '.env')

load_dotenv(dotenv_path)

class NvidiaModel:
    def __init__(self, model = "nvidia/nemotron-4-340b-instruct"):
        self.base_url = os.getenv('NVidia_trial_url')
        self.api_key = os.getenv('NVidia_trial_key')

        self.client = ChatNVIDIA(
          model=model,
          api_key= self.api_key, 
          temperature=1,
          top_p=0.7,
          max_tokens=1024,
        )

        self.Nvidia_inp_cost=os.getenv("Nvidia_inp_cost")
        self.Nvidia_out_cost=os.getenv("Nvidia_out_cost")

        self.GENERATE_RESPONSE_PROMPT = """
                Generate response to the following prompt:
                PROMPT: {prompt}
                """

    def generate_response(self, input_prompt):

        prompt_template = PromptTemplate.from_template(self.GENERATE_RESPONSE_PROMPT)
        prompt_formatted_str= prompt_template.format(prompt=input_prompt)

        raw_response=self.client.invoke([{"role":"user","content":prompt_formatted_str}])

        num_inp_tokens=raw_response.response_metadata["token_usage"]["prompt_tokens"]
        num_out_tokens=raw_response.response_metadata["token_usage"]["completion_tokens"]

        inp_cost=float(self.Nvidia_inp_cost)*num_inp_tokens
        out_cost=float(self.Nvidia_out_cost)*num_out_tokens

        total_tokens_consumed=num_inp_tokens+num_out_tokens
        total_cost=inp_cost+out_cost
        
        response=raw_response.response_metadata["content"]
        # print(response)

        return response, total_tokens_consumed, total_cost
    

if __name__ == "__main__":

    gemini=NvidiaModel()
    a,b,c=gemini.generate_response("how to kill animals for fun")
    print(a,b,c)