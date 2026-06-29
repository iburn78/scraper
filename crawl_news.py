import re
import asyncio
from datetime import datetime
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from ggl_news_feed import get_google_news_feed

def _set_filename(keywords=None):
    exctime = datetime.now().strftime('%Y-%m-%d_%H%M%S_%f_')[:-3] 
    if keywords:
        safe_keywords = re.sub(r'[\\/*?:"<>|]', "_", keywords)
        filename = f"{exctime}_{'_'.join(safe_keywords.split()[:3])}.md"
    else: 
        filename = f"{exctime}_untitled.md"
    return filename

async def _crawl_url_and_save(crawler, url, title=None, published=None):
    prune_filter = PruningContentFilter(
        # higher for more content pruned [0, 1]
        threshold=0.99,
        # dynamic adjustment of threshold
        threshold_type="dynamic",  
        # Ignore nodes with <10 words
        min_word_threshold=10
    )

    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
    config = CrawlerRunConfig(markdown_generator=md_generator)

    result = await crawler.arun(url=url, config=config)
    if not result.success:
        print("Error:", result.error_message)
        return None

    title_ = result.metadata.get("title") or title
    filename = _set_filename(title_)

    if published: 
        pdate = published.strftime("%Y-%m-%d") 
    else: 
        pdate = "-----"

    with open(filename, "w", encoding="utf-8") as f:
        if title_:
            f.write(f"# {title_}\n\n")
        f.write(f"source: {url}\n")
        f.write(f"published: {pdate}\n\n")
        f.write(result.markdown.fit_markdown)
        print(f'{filename} is written')

async def _crawl_news(query, kr, cutoff_months, max_result, show_res):
    items = await get_google_news_feed(
        query,
        kr_title=kr,
        cutoff_months=cutoff_months,
        max_result=max_result, 
        show_res=show_res,
        )

    async with AsyncWebCrawler() as crawler:
        tasks = [
            _crawl_url_and_save(crawler, i['url'], i['title'], i['published'])
            for i in items
            if items
        ]
    
        await asyncio.gather(*tasks)

def crawl_news(
        query, 
        kr=True, 
        cutoff_months=6, 
        max_result=10, 
        show_res=True,
    ):
    asyncio.run(_crawl_news(query, kr=kr, cutoff_months=cutoff_months, max_result=max_result, show_res=show_res))

if __name__ == "__main__":
    # crawl_news('SOOP 실적')
    # crawl_news('롯데에너지머티리얼즈 실적')
    crawl_news('아이지넷 실적')

###_ Categorization required for mds... 
###_ study sequence of what to get first, and then next... 