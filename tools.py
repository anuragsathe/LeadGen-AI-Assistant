
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import Tool

from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse


search = DuckDuckGoSearchRun()


def extract_emails(text: str) -> list[str]:
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    return list(set(emails))  # remove duplicates


def scrape_website(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Remove scripts/styles
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text)

        return text[:5000]  # limit size

    except Exception as e:
        return f"Error scraping {url}: {str(e)}"


def generate_search_queries(company_name: str) -> list[str]:
    return [
        f"{company_name} Vancouver business",
        f"{company_name} contact email website",
        f"{company_name} services company"
    ]


def extract_urls(text: str) -> list[str]:
    urls = re.findall(
        r'https?://[^\s]+',
        text
    )

    # Filter junk links
    clean_urls = []
    for url in urls:
        parsed = urlparse(url)
        if parsed.netloc and "duckduckgo" not in url:
            clean_urls.append(url)

    return list(set(clean_urls))



def search_and_scrape_company(company_name: str) -> str:
    queries = generate_search_queries(company_name)
    collected_text = []
    collected_emails = set()

    for query in queries:
        try:
            search_results = search.run(query)
            urls = extract_urls(search_results)

            # Try top 2 URLs for better reliability
            for url in urls[:2]:
                content = scrape_website(url)

                if "Error scraping" not in content:
                    collected_text.append(content)

                    # Extract emails
                    emails = extract_emails(content)
                    collected_emails.update(emails)

                    break  # stop after first good page

        except Exception as e:
            continue

    final_text = " ".join(collected_text)

    # Attach emails at the end for easy parsing by LLM
    if collected_emails:
        final_text += "\n\nEmails Found: " + ", ".join(collected_emails)

    return final_text[:6000]  # final cap



def save_to_txt(data: str, filename: str = "leads_output.txt") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    formatted_text = (
        f"\n--- Leads Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(formatted_text)

        return f" Data successfully saved to {filename}"

    except Exception as e:
        return f" Error saving file: {str(e)}"




search_tool = Tool(
    name="search",
    func=search.run,
    description="Use this to find company names, websites, and general business info."
)

scrape_tool = Tool(
    name="search_and_scrape_company",
    func=search_and_scrape_company,
    description="Use this to gather detailed company information, including services, contact details, and emails."
)

save_tool = Tool(
    name="save_to_text",
    func=save_to_txt,
    description="Use this to save the final structured JSON output into a text file."
)