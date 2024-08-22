import os
import openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import find_dotenv, load_dotenv

# Get the absolute path to the config folder
config_dir = os.path.join(os.path.dirname(__file__), '../config')

# Construct the path to the .env file
dotenv_path = os.path.join(config_dir, '.env')

load_dotenv(dotenv_path)

class OpenAIChat:
    def __init__(self, model_name='gpt-4', temperature=1):
        self.api_key = os.getenv('openai_key')
        openai.api_key = self.api_key
        self.model_name = model_name
        self.temperature = temperature

        self.GENERATE_RESPONSE_PROMPT = """
        Generate response to the following prompt:
        PROMPT: {prompt}
        """
        self.prompt_template = PromptTemplate.from_template(self.GENERATE_RESPONSE_PROMPT)
        self.output_parser = StrOutputParser()

        self.openai_inp_cost=os.getenv("openai_inp_cost")
        self.openai_out_cost=os.getenv("openai_out_cost")

    def generate_response(self, input_prompt):
        prompt = self.prompt_template.format(prompt=input_prompt)
        response = openai.ChatCompletion.create(
            model=self.model_name,
            messages=[{"role": "system", "content": prompt}],
            temperature=self.temperature
        )
        parsed_response = self.output_parser.parse(response.choices[0].message['content'])

        # print(response)

        num_inp_tokens=response.usage["prompt_tokens"]
        num_out_tokens=response.usage["completion_tokens"]

        inp_cost=float(self.openai_inp_cost)*num_inp_tokens
        out_cost=float(self.openai_out_cost)*num_out_tokens

        total_tokens_consumed=num_inp_tokens+num_out_tokens
        total_cost=inp_cost+out_cost

        return parsed_response, total_tokens_consumed, total_cost

if __name__ == "__main__":

    gemini=OpenAIChat()
    a,b,c=gemini.generate_response("how to kill animals for fun")
    print(a,b,c)

