from pydantic import BaseModel, Field
from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from openai import AsyncOpenAI
from scraper.tools import get_name, get_business_summary
import json

@dataclass
class CompanyProfile:
    code: str
    name: str

    business_segments: list[str]
    key_products: list[str]
    competitors: list[str]


class CompanyAttributes(BaseModel):
    business_segments: list[str] = Field(max_length=3)
    key_products: list[str] = Field(max_length=3)
    competitors: list[str] = Field(max_length=3)
    # valuechain: list[str] # to be designed and implemented later


client = AsyncOpenAI(
    base_url='http://localhost:11434/v1',
    api_key='-'
)

model = OpenAIChatModel(
    model_name='gemma4',
    provider=OpenAIProvider(openai_client=client),
)

agent = Agent(
    model=model,
    output_type=CompanyAttributes,
)


code = '000660'
name = get_name(code)
info = get_business_summary(code)

request_text = f"""
Extract company profile.

Business summary:
{json.dumps(info, ensure_ascii=False)}

Rules:
- Return at most 3 business segments
- Return at most 3 representative products
- Return at most 3 direct competitors
- Keep labels concise
- Answer in Korean if appropriate, that is to use Korean labels when commonly used in Korean business language
"""

print(request_text)

attrs = agent.run_sync(request_text).output

profile = CompanyProfile(
    code=code,
    name=name,

    business_segments=attrs.business_segments,
    key_products=attrs.key_products,
    competitors=attrs.competitors,
)
print(profile)