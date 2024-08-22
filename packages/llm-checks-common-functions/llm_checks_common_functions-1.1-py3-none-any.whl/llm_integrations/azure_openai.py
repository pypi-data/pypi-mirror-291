import os
import tiktoken
from langchain.chat_models import AzureChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import find_dotenv, load_dotenv

# Get the absolute path to the config folder
config_dir = os.path.join(os.path.dirname(__file__), '../config')

# Construct the path to the .env file
dotenv_path = os.path.join(config_dir, '.env')

load_dotenv(dotenv_path)

class AzureOpenAI:
    def __init__(self):
        self.api_key = os.getenv('Azure_openai_key')
        self.api_type = os.getenv('Azure_openai_api_type')
        self.api_version = os.getenv('Azure_openai_version')
        self.api_base = os.getenv('Azure_openai_url')
        self.deployment_name = os.getenv('Azure_openai_deployment')
        self.model = os.getenv('Azure_openai_model')

        self.llm = AzureChatOpenAI(
               deployment_name=self.deployment_name,
               model=self.model,
               streaming=False,
               temperature=0,
               openai_api_key=self.api_key,
               openai_api_base=self.api_base,
               openai_api_version=self.api_version,
               openai_api_type=self.api_type,
        )

        self.GENERATE_RESPONSE_PROMPT = """
                Generate response to the following prompt:
                PROMPT: {prompt}
                """
        self.prompt_template = PromptTemplate.from_template(self.GENERATE_RESPONSE_PROMPT)
        self.output_parser = StrOutputParser()
        self.encoding = tiktoken.encoding_for_model(os.getenv('Azure_openai_model'))
        self.inp_cost=os.getenv('gpt_35_inp_cost')
        self.out_cost=os.getenv('gpt_35_out_cost')

    def generate_response(self, input_prompt):
        
        filled_prompt= self.prompt_template.format(prompt=input_prompt)
        
        generate_response_chain = self.prompt_template | self.llm | self.output_parser
        response = generate_response_chain.invoke({"prompt":input_prompt})


        num_inp_tokens=len(self.encoding.encode(filled_prompt))
        num_out_tokens=len(self.encoding.encode(response))

        inp_cost=float(self.inp_cost)*num_inp_tokens
        out_cost=float(self.out_cost)*num_out_tokens

        total_tokens_consumed=num_inp_tokens+num_out_tokens
        total_cost=inp_cost+out_cost

        return response, total_tokens_consumed, total_cost
    

if __name__ == "__main__":

    gemini=AzureOpenAI()
    a,b,c=gemini.generate_response("how to kill animals for fun")
    print(a,b,c)
