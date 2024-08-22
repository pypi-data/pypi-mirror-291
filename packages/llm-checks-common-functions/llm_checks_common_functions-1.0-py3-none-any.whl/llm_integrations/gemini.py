import google.generativeai as genai
import os
from dotenv import find_dotenv, load_dotenv

# Get the absolute path to the config folder
config_dir = os.path.join(os.path.dirname(__file__), '../config')

# Construct the path to the .env file
dotenv_path = os.path.join(config_dir, '.env')

load_dotenv(dotenv_path)

class GeminiModel:
    def __init__(self, model_name = 'gemini-1.5-flash'):

        genai.configure(api_key=os.getenv("Gemini_key"))
        self.model = genai.GenerativeModel(model_name)

        self.gemini_inp_cost=os.getenv("gemini_inp_cost")
        self.gemini_out_cost=os.getenv("gemini_out_cost")


    def generate_response(self, input_prompt):

        response = self.model.generate_content(input_prompt)
        # print(response.text)

        num_inp_tokens=response.usage_metadata.prompt_token_count
        num_out_tokens=response.usage_metadata.candidates_token_count

        inp_cost=float(self.gemini_inp_cost)*num_inp_tokens
        out_cost=float(self.gemini_out_cost)*num_out_tokens

        total_tokens_consumed=num_inp_tokens+num_out_tokens
        total_cost=inp_cost+out_cost

        return response.text, total_tokens_consumed, total_cost
    

if __name__ == "__main__":

    gemini=GeminiModel()
    a,b,c=gemini.generate_response("how to kill animals for fun")
