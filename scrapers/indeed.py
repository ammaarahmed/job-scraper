import json
from typing import Generator, Dict, Any
from bs4 import BeautifulSoup

from .base import BaseScraper


class IndeedScraper(BaseScraper):
    """Scraper with two approaches: GraphQL API and standard HTML scraping."""

    GRAPHQL_ENDPOINT = "https://www.indeed.com/graphql"

    def search_graphql(self, query: str, location: str, start: int = 0, limit: int = 10) -> Generator[Dict[str, Any], None, None]:
        """Yield jobs from Indeed GraphQL API."""
        payload = {
            "operationName": "JobSearch",
            "variables": {
                "query": query,
                "location": location,
                "start": start,
                "limit": limit,
            },
            "query": """
            query JobSearch($query: String!, $location: String!, $start: Int!, $limit: Int!) {
              jobsearch(query: $query, location: $location, start: $start, limit: $limit) {
                jobs {
                  jobkey
                  companyName
                  formattedLocation
                  jobTitle
                }
              }
            }
            """
        }
        response = self.post(self.GRAPHQL_ENDPOINT, json=payload, headers={"Content-Type": "application/json"})
        data = response.json()
        jobs = data.get("data", {}).get("jobsearch", {}).get("jobs", [])
        for job in jobs:
            yield {
                "id": job.get("jobkey"),
                "title": job.get("jobTitle"),
                "company": job.get("companyName"),
                "location": job.get("formattedLocation"),
            }

    def search_scrape(self, query: str, location: str, start: int = 0) -> Generator[Dict[str, Any], None, None]:
        """Scrape Indeed search result HTML."""
        url = f"https://www.indeed.com/jobs?q={query}&l={location}&start={start}"
        response = self.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "lxml")
        for card in soup.select("div.job_seen_beacon"):
            jobkey = card.find("a", {"data-jk": True})
            title_el = card.select_one("h2.jobTitle span")
            company_el = card.select_one("span[data-testid='company-name']")
            location_el = card.select_one("div[data-testid='text-location'] span")
            yield {
                "id": jobkey.get("data-jk") if jobkey else None,
                "title": title_el.text.strip() if title_el else None,
                "company": company_el.text.strip() if company_el else None,
                "location": location_el.text.strip() if location_el else None,
            }
