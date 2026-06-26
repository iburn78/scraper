from urllib.parse import quote, urlparse
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import asyncio
import re
import feedparser
from playwright.async_api import async_playwright 

# sites that detect crawling
BANNED_DOMAINS = {
    "msn.com",
    "bing.com",
    "daum.net",
    "naver.com",
}

async def get_google_news_feed(
    query,
    kr_title: bool, # Korean words have to be included in title if True
    cutoff_months: int, # recent n months
    max_result: int,
    show_res: bool,
):

    if kr_title:
        hl, gl, ceid = "ko", "KR", "KR:ko"
    else:
        hl, gl, ceid = "en", "US", "US:en"

    rss_url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}"
        f"&hl={hl}"
        f"&gl={gl}"
        f"&ceid={ceid}"
    )

    feed = feedparser.parse(rss_url)

    cutoff = (
        datetime.now(ZoneInfo("Asia/Seoul"))
        - timedelta(days=30 * cutoff_months)
    )

    # preprocess
    entries = []

    for e in feed.entries:

        if not hasattr(e, "published_parsed"):
            continue

        pub_dt = (
            datetime(
                *e.published_parsed[:6],
                tzinfo=timezone.utc
            )
            .astimezone(ZoneInfo("Asia/Seoul"))
        )

        if pub_dt < cutoff:
            continue

        if kr_title and not re.search(r"[가-힣]", e.title):
            continue

        entries.append({
            "title": e.title,
            "link": e.link,
            "published": pub_dt,
        })

    # newest first
    entries.sort(
        key=lambda x: x["published"],
        reverse=True
    )

    items = []

    batch_size = int(max_result*1.5)
    finished = False
    for start in range(0, len(entries), batch_size):
        batch = entries[start:start + batch_size]

        urls = await asyncio.gather(
            *[
                _resolve_google_news_url(e["link"])
                for e in batch
            ]
        )

        for e, url in zip(batch, urls):

            if url is None:
                continue

            items.append({
                "title": e["title"],
                "url": url,
                "published": e["published"],
            })

            if len(items) >= max_result:
                finished = True
                break

        if finished: break

    if show_res:
        print("---------------------------------------------------------------------------")
        print(f'Google news search for: {query}')
        print("---------------------------------------------------------------------------")
        for i, item in enumerate(items):
            print(f'[{i+1}] {item["title"]}')
            print(f'[{i+1}] {item["url"]}')
            print(f'[{i+1}] {item["published"]}')

    return items

async def _resolve_google_news_url(link):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        try:
            page = await browser.new_page()

            await page.goto(
                link,
                wait_until="commit",
                timeout=10000,
            )

            try:
                await page.wait_for_url(
                    lambda u: "news.google.com" not in u,
                    timeout=5000,
                )
            except:
                pass

            if not _is_banned(page.url):
                return page.url
        finally:
            await browser.close()

        return None

def _is_banned(url: str) -> bool:
    try:
        domain = urlparse(url).netloc.lower()
        return any(b in domain for b in BANNED_DOMAINS)
    except:
        return True
