import unittest
from unittest.mock import patch, Mock

from scrapers.indeed import IndeedScraper


SAMPLE_GRAPHQL_RESPONSE = {
    "data": {
        "jobsearch": {
            "jobs": [
                {
                    "jobkey": "123",
                    "jobTitle": "Software Engineer",
                    "companyName": "Acme",
                    "formattedLocation": "Remote"
                },
                {
                    "jobkey": "456",
                    "jobTitle": "Data Scientist",
                    "companyName": "Beta",
                    "formattedLocation": "NY"
                }
            ]
        }
    }
}

SAMPLE_HTML = """
<div class='job_seen_beacon'>
    <a data-jk='789'></a>
    <h2 class='jobTitle'><span>Developer</span></h2>
    <span data-testid='company-name'>Gamma</span>
    <div data-testid='text-location'><span>CA</span></div>
</div>
"""


class TestIndeedScraper(unittest.TestCase):
    def test_search_graphql_parsing(self):
        scraper = IndeedScraper()
        with patch.object(scraper, 'post', return_value=Mock(json=lambda: SAMPLE_GRAPHQL_RESPONSE)):
            results = list(scraper.search_graphql('dev', 'remote'))
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['id'], '123')
        self.assertEqual(results[1]['company'], 'Beta')

    def test_search_scrape_parsing(self):
        scraper = IndeedScraper()
        mock_response = Mock(text=SAMPLE_HTML)
        with patch.object(scraper, 'get', return_value=mock_response):
            results = list(scraper.search_scrape('dev', 'remote'))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['company'], 'Gamma')


if __name__ == '__main__':
    unittest.main()
