import asyncio
import re
from typing import List, Dict, Any
from playwright.async_api import async_playwright, TimeoutError


CONCURRENCY_LIMIT = 5
MAX_RETRIES = 2
PAGE_TIMEOUT = 15000  # 15 seconds


def clean_text(text: str) -> str:
    """Normalize whitespace for LLM ingestion while preserving paragraph breaks."""
    # Replace multiple horizontal spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)
    # Replace 3 or more newlines with exactly 2 newlines (paragraph break)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


async def scrape_page(context, url: str, semaphore: asyncio.Semaphore) -> Dict[str, Any]:
    """Scrape a single URL with Playwright, handling timeouts and errors gracefully."""
    async with semaphore:
        for attempt in range(MAX_RETRIES + 1):
            page = await context.new_page()
            try:
                print(f"[Attempt {attempt+1}] Scraping: {url}")

                print(f"[Attempt {attempt+1}] Going to URL: {url}...")
                # Wait for domcontentloaded to handle most JS rendering without hanging on analytics
                await page.goto(url, wait_until="domcontentloaded", timeout=PAGE_TIMEOUT)
                print(f"[Attempt {attempt+1}] Navigation complete for {url}. Waiting for hydration...")

                # Wait a tiny bit extra for Next.js/React hydration
                await page.wait_for_timeout(1500)
                print(f"[Attempt {attempt+1}] Hydration wait complete for {url}. Extracting text...")

                # Let Playwright's native engine calculate visible text
                # inner_text() automatically respects CSS visibility and display rules
                body_locator = page.locator("body")
                text = await body_locator.inner_text()
                text = clean_text(text)

                await page.close()

                return {
                    "url": url,
                    "text": text,
                    "length": len(text),
                }

            except TimeoutError:
                print(f"Timeout scraping {url}")
            except Exception as e:
                print(f"Error scraping {url}: {e}")

            finally:
                await page.close()

        return {"url": url, "error": "Failed after retries"}


async def scrape_urls(urls: List[str]) -> List[Dict[str, Any]]:
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)

    print("Starting playwright...")
    async with async_playwright() as p:
        print("Launching chromium...")
        browser = await p.chromium.launch(
            headless=True
        )
        print("Creating context...")
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
        )
        print("Context created. Gathering tasks...")

        tasks = [
            scrape_page(context, url, semaphore)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

        await browser.close()
        return results


if __name__ == "__main__":
    urls = [
        "https://example.com",
        "https://www.python.org",
    ]

    results = asyncio.run(scrape_urls(urls))

    for r in results:
        print("\n---")
        print(f"URL: {r['url']}")
        if "text" in r:
            print("TEXT PREVIEW:")
            print(r["text"][:500])  # preview first 500 chars
            print(f"... (Length: {r['length']})")
        else:
            print(f"ERROR: {r['error']}")