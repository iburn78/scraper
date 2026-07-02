
- get stock code and name in Korean from the user
- below will use gemma4:ollama as local llm
- ask llm keywords for this company's main businesses (use pydantic to enforce max top 3), and main competitors (the most close / market leader top 1)
    - if there is no sufficient knowledge within llm, then make it admit by like saying None instead of saying garbage

- use crawl_engine that I made (which takes a request sentence and does google rss news search, then crawl main article using crawl4ai, finally saves them as md file locally)
    - construct request sentences like following
        - name + '실적' 
        - name + business_seg1
        - name + business_seg2
        - name + business_seg3
        - name + competitor
    - crawl each of these (top 5 articles each) to md files saved locally
- make the llm accessible to these and previous report on the same company, and generate the following report
- report:
    [qualitative]
    - explanation on the main businesses (top 3)
    - recent financial performance (overall and/or for each business segs) and reasons behind
    - main competitor and compared to the competitor on (1) why financial performances are differ and (2) what are differences in competitve advantages
    - key issues that this company is facing: overall and/or for each business segs
    [quantitative]
- format:
    - qualitative part: formats to be defined as above, but will be like section title and plain text (no modifications like bold etc), and make sentences are concise
    - quantitative part: for some questions to enfore Literal['best', 'top-tier', '2nd-tier', 'else'] etc.



queries = [
 f"{name} 실적",
 f"{name} 전망",
 f"{name} {seg}",
 f"{name} {seg} 수익성",
 f"{name} 경쟁사 {competitor}",
]

max queries = 8
max docs/query = 5


class ArticleInsight(BaseModel):
    topic: str
    key_points: list[str]
    financial_signal: str | None
    business_segment: str | None
    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ]

current: 
feed previous report
might be risky

Risk:
Model repeats old conclusions.

Safer:

Store:

class HistoricalFinding(BaseModel):
    statement: str
    confidence: float
    evidence_date: str

Then prompt:

Treat previous reports as historical hypotheses.
Current news overrides old conclusions.


-------------


Report generation

I would make the report itself structured.

Example:

class QualitativeReport(BaseModel):

    main_businesses: list[str]

    performance_summary: str

    business_analysis: list[
        BusinessSegment
    ]

    competitor_analysis: str

    key_issues: list[str]

Quantitative:

class QuantitativeRating(BaseModel):

    profitability:
        Literal[
            "best",
            "top-tier",
            "2nd-tier",
            "else"
        ]

    growth:
        Literal[
            "best",
            "top-tier",
            "2nd-tier",
            "else"
        ]

    competitiveness:
        Literal[
            "best",
            "top-tier",
            "2nd-tier",
            "else"
        ]

    confidence: float

Add:

evidence_count: int


--------------


7. Biggest improvement: make retrieval iterative

Instead of:

extract →
crawl →
report

Do:

extract
↓
crawl
↓
summarize
↓
missing information?
↓
extra retrieval
↓
report

Example:

Need:
- margins
- China exposure

→ search again

This gives much better analyst-like reports.

8. One concern: Gemma4 knowledge

Your assumption:

Gemma4 already knows most Korean listed companies

Partially true.

Likely:

Large caps → decent prior knowledge
Mid caps → mixed
Small caps → unreliable
Latest business changes → weak

So your design decision:

allow None

is exactly right.

Do not force completion.

If implementing today, I would build:

orchestrator
├── profile_agent
├── retrieval_agent
├── article_summarizer
├── report_generator
├── report_memory
└── evaluator

That separation will keep it maintainable when the prompt count starts growing.