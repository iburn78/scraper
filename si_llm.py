import os
from openai import OpenAI
import pandas as pd

pd_ = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # .   
df_krx = pd.read_feather(os.path.join(pd_, "trader/data_collect/data/df_krx.feather"))

client = OpenAI(
    base_url="http://localhost:11434/v1", # ollama
    api_key= "-", 
)

def get_LLM_response(prompt):
    chat_completion = client.chat.completions.create(
        model="gemma4", 
        messages=[
            {
                "role": "user",
                "content": (
                    prompt
                )
            }
        ],
    )
    
    response = chat_completion.choices[0].message.content
    return response

if __name__ == "__main__":
    code ='020150'
    name = df_krx.loc[code, "Name"]
    print(get_LLM_response(f'{name}: key businesses?'))
