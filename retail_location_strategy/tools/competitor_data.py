from .searxng_search import SearXNGConnector
from .web_scraper import scrape_urls

async def competitor_data(query: str):
    """
    Acts as a competitor_data tool by combining internet search and web_scraper.
    Returns raw data for competitor analysis.
    """
    # 1. Search for candidates
    connector = SearXNGConnector()
    search_results = await connector.search(
        query=query,
        max_results=10
    )
    
    urls = search_results.get("urls",[])
    print(f"Found {len(urls)} URLs.")

    # 2. Scrape in parallel (handling semaphore)
    scraped_results = await scrape_urls(urls)
    
    # 3. Return a combined blob for the LLM to analyze
    return {"competitors_raw_data": scraped_results}