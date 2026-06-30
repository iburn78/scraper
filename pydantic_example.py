#%% -----------------------------------------------------------------------
# BASIC PYDANTIC USAGE
from pydantic import BaseModel

# Pydantic model (similar to dataclass, but with runtime validation)
class User(BaseModel):
    # field definitions via type annotations
    name: str
    age: int
    active: bool = True   # default value

# Pydantic will:
# - validate input types
# - coerce types when possible
# - raise ValidationError if invalid

u = User(name="Andy", age=35)

print(u)                  # parsed model object
print(type(u.age))       # <class 'int'>

# serialization helpers
print(u.model_dump())       # dict form
print(u.model_dump_json())  # JSON string


#%% -----------------------------------------------------------------------
# AI type validation use cases
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from openai import AsyncOpenAI

# connect to local Ollama server
client = AsyncOpenAI(
    base_url='http://localhost:11434/v1',
    api_key='-'
)

# define model
model = OpenAIChatModel(
    model_name='gemma4',
    provider=OpenAIProvider(openai_client=client),
)

# structured output schema
from typing import Literal
from typing import Annotated
from pydantic import StringConstraints

# uppercases, letters, 1 to 5 chars, exactly one token(word)
# pattern=r'^[A-Z]{1,5}$' 
# include dots/dashes  
# pattern=r'^[A-Z.\-]{1,10}$'
# include / 
# pattern=r'^[A-Z0-9.\-\/]{1,15}$'

TickerStr = Annotated[
    str,
    StringConstraints(pattern=r'^[A-Z]{1,5}$')
]

class StockAnalysis(BaseModel):
    ticker: TickerStr
    sentiment: Literal['bullish', 'bearish', 'neutral'] # or 'str' 
    confidence: float

# agent with enforced output type
agent = Agent(
    model=model,
    output_type=StockAnalysis,
)

request_text = 'Analyze NVDA stock sentiment.'

# result = await agent.run(request_text) # when run in notebook:
result = agent.run_sync(request_text) # run in terminal

# type validated output
print(result.output)
# normal python object access
print(result.output.ticker)
print(result.output.sentiment)
print(result.output.confidence)
