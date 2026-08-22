import os
import re
import requests
import trafilatura

from bs4 import BeautifulSoup
from readability import Document
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError(
        "TAVILY_API_KEY is not set. "
        "Add it to your .env file or Render Environment Variables."
    )


# ============================================================
# Tavily Client
# ============================================================

tavily = TavilyClient(
    api_key=TAVILY_API_KEY
)


# ============================================================
# Web Search Tool
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web using Tavily.

    Returns relevant titles, URLs and snippets.
    """

    try:
        results = tavily.search(
            query=query,
            max_results=5
        )

        if not results or "results" not in results:
            return "No search results were found."

        output = []

        for result in results["results"]:

            title = result.get("title", "No title")
            url = result.get("url", "No URL")
            content = result.get("content", "")

            output.append(
                f"Title: {title}\n"
                f"URL: {url}\n"
                f"Snippet: {content[:500]}\n"
            )

        if not output:
            return "No useful search results were found."

        return "\n--------------------\n".join(output)

    except Exception as e:
        return f"Web search failed: {str(e)}"


# ============================================================
# URL Scraping Tool
# ============================================================

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and extract readable content from a URL.

    Uses:
    1. Trafilatura
    2. Readability
    3. BeautifulSoup fallback
    """

    if not url:
        return "No URL was provided."

    # --------------------------------------------------------
    # HTTP headers
    # --------------------------------------------------------

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,"
                  "application/xml;q=0.9,*/*;q=0.8",
    }

    try:

        # ----------------------------------------------------
        # Fetch webpage
        # ----------------------------------------------------

        response = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        html = response.text

        if not html:
            return "The webpage returned empty content."

        # ----------------------------------------------------
        # Strategy 1: Trafilatura
        # ----------------------------------------------------

        extracted = trafilatura.extract(
            html,
            include_comments=False,
            include_tables=True,
            favor_precision=True
        )

        if extracted and len(extracted.strip()) > 200:

            cleaned = re.sub(
                r"\s+",
                " ",
                extracted
            ).strip()

            return cleaned[:8000]

        # ----------------------------------------------------
        # Strategy 2: Readability
        # ----------------------------------------------------

        try:

            document = Document(html)

            clean_html = document.summary()

            soup = BeautifulSoup(
                clean_html,
                "html.parser"
            )

            # Remove unwanted elements

            for tag in soup([
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
                "noscript"
            ]):
                tag.decompose()

            text = soup.get_text(
                separator=" ",
                strip=True
            )

            if text and len(text.strip()) > 200:

                cleaned = re.sub(
                    r"\s+",
                    " ",
                    text
                ).strip()

                return cleaned[:8000]

        except Exception:
            pass

        # ----------------------------------------------------
        # Strategy 3: BeautifulSoup fallback
        # ----------------------------------------------------

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside",
            "form",
            "noscript"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        cleaned = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        if cleaned:

            return cleaned[:8000]

        return "Could not extract meaningful content from the webpage."

    # --------------------------------------------------------
    # Error handling
    # --------------------------------------------------------

    except requests.exceptions.Timeout:

        return (
            "The request timed out while trying "
            "to scrape the URL."
        )

    except requests.exceptions.ConnectionError:

        return (
            "Could not connect to the webpage."
        )

    except requests.exceptions.HTTPError as e:

        return (
            f"HTTP error while scraping the URL: {str(e)}"
        )

    except requests.exceptions.RequestException as e:

        return (
            f"Request error while scraping the URL: {str(e)}"
        )

    except Exception as e:

        return (
            f"Could not scrape the URL: {str(e)}"
        )