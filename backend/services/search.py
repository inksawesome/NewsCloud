import time
from duckduckgo_search import DDGS

def search_web_for_claim(claim: str, max_results: int = 5) -> list[str]:
    """
    Search DuckDuckGo for the given claim and return a list of URLs.
    Includes basic retry logic for rate limiting.
    """
    urls = []
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            with DDGS() as ddgs:
                # We consume the generator into a list to trigger any potential rate-limit exceptions immediately
                results = list(ddgs.text(claim, max_results=max_results))
                if results:
                    urls = [r.get("href") for r in results if r.get("href")]
                    break  # Success, exit retry loop
        except Exception as e:
            print(f"Search attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt) # Exponential backoff: 1s, 2s...
                
    return urls
