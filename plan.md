
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