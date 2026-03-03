import asyncio
import json
from searxng_search import SearXNGConnector
from web_scraper import scrape_urls  # your async function

OUTPUT_FILE = "my_results.txt"

async def main():
    # 1️⃣ Perform search using SearXNGConnector
    connector = SearXNGConnector()
    search_results = await connector.search(
        query="What are the best cafes in worcester ma",
        max_results=10
    )
    urls = search_results.get("urls",[])
    print(f"Found {len(urls)} URLs.")

    # 2️⃣ Scrape URLs using your web_scraper
    scraped_results = await scrape_urls(urls)
    print(scraped_results)

    # # 3️⃣ Aggregate results
    # aggregated_results = {
    #     "query": "What are the best cafes in worcester ma",
    #     "urls": urls,
    #     "results": scraped_results,
    #     "suggestions": search_results[0].get("suggestions", []) if search_results else [],
    #     "infoboxes": search_results[0].get("infoboxes", []) if search_results else [],
    # }

    # # 4️⃣ Save to file
    # with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    #     json.dump(aggregated_results, f, ensure_ascii=False, indent=2)

    # print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())