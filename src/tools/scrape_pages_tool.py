import os
from typing import Optional, Type, Any

import requests
from bs4 import BeautifulSoup
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field


class FixedScrapePagesToolSchema(BaseModel):
    """Input for ScrapePagesTool."""
    pass


class ScrapePagesToolSchema(FixedScrapePagesToolSchema):
    """Defines the input for ScrapePagesTool to handle multiple URLs."""
    pages_urls: str = Field(..., description="""Mandatory list of website URLs separated by the '|' symbol.'""")


class ScrapePagesTool(BaseTool):
    name: str = "Scrape list of pages content"
    description: str = ("""A tool designed to scrape and extract text from multiple web pages, specified by a delimited 
                        list of URLs using '|'. This tool processes each URL and returns the text content.""")
    args_schema: Type[BaseModel] = ScrapePagesToolSchema
    pages_urls: Optional[str] = None
    cookies: Optional[dict] = None
    headers: Optional[dict] = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Encoding': 'gzip, deflate, br'
    }

    def __init__(self, pages_urls: Optional[str] = None, cookies: Optional[dict] = None, **kwargs):
        super().__init__(**kwargs)
        if pages_urls is not None:
            self.pages_urls = pages_urls
            self.description = f"""A tool designed to scrape and extract text from multiple web pages, specified by a 
                                delimited list of URLs using '|'. This tool processes each URL and returns the text 
                                content. URL list is:{pages_urls}"""
            self.args_schema = FixedScrapePagesToolSchema
            self._generate_description()
            if cookies is not None:
                self.cookies = {cookies["name"]: os.getenv(cookies["value"])}


    def _run(
            self,
            **kwargs: Any
    ) -> Any:
        pages_urls = kwargs.get('pages_urls', self.pages_urls)

        print("\n\nSCRAPE PAGE INPUT ******************************************************************")
        print(pages_urls)
        print("SCRAPE PAGE INPUT END **************************************************************")


        urls = pages_urls.split('|')  # Split the string into a list of URLs
        results = []
        for url in urls:
            try:
                page = requests.get(
                    url.strip(),
                    timeout=15,
                    headers=self.headers if self.headers else {},
                    cookies=self.cookies if self.cookies else {}
                )
                parsed = BeautifulSoup(page.content, "html.parser")
                text = parsed.get_text()
                text = '\n'.join([i for i in text.split('\n') if i.strip() != ''])
                text = ' '.join([i for i in text.split(' ') if i.strip() != ''])
                results.append(text)
            except Exception as e:
                results.append(f"Error retrieving {url}: {str(e)}")
        return '\n\n'.join(results)
