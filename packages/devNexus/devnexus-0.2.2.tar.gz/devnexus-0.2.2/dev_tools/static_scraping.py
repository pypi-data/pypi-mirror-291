import requests
from bs4 import BeautifulSoup
from typing import List, Optional

class StaticScraper:
    def __init__(self, url: str):
        self.url = url
        self.soup = self._get_soup()

    def _get_soup(self) -> BeautifulSoup:
        """Fetch the page content and return a BeautifulSoup object."""
        response = requests.get(self.url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return BeautifulSoup(response.text, 'html.parser')

    def find_by_id(self, element_id: str) -> Optional[BeautifulSoup]:
        """Find an HTML element by its ID."""
        return self.soup.find(id=element_id)

    def find_by_class(self, class_name: str) -> List[BeautifulSoup]:
        """Find HTML elements by their class name."""
        return self.soup.find_all(class_=class_name)

    def find_by_tag(self, tag_name: str) -> List[BeautifulSoup]:
        """Find HTML elements by their tag name."""
        return self.soup.find_all(tag_name)

    def find_by_css(self, css_selector: str) -> List[BeautifulSoup]:
        """Find HTML elements using a CSS selector."""
        return self.soup.select(css_selector)

    def find_by_attribute(self, tag_name: str, attribute_name: str, attribute_value: str) -> List[BeautifulSoup]:
        """Find HTML elements by tag name and attribute."""
        return self.soup.find_all(tag_name, {attribute_name: attribute_value})

    def find_text(self, text: str) -> List[BeautifulSoup]:
        """Find HTML elements containing the given text."""
        return self.soup.find_all(string=lambda t: text in t)

    def get_links(self) -> List[str]:
        """Get all hyperlinks (anchor tags) on the page."""
        return [a['href'] for a in self.soup.find_all('a', href=True)]

    def get_images(self) -> List[str]:
        """Get all image sources (img tags) on the page."""
        return [img['src'] for img in self.soup.find_all('img', src=True)]

    def get_text(self) -> str:
        """Get all the text content of the page."""
        return self.soup.get_text()

    def find_next_sibling(self, element: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the next sibling of a given HTML element."""
        return element.find_next_sibling()

    def find_previous_sibling(self, element: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the previous sibling of a given HTML element."""
        return element.find_previous_sibling()

    def find_parent(self, element: BeautifulSoup) -> Optional[BeautifulSoup]:
        """Find the parent of a given HTML element."""
        return element.find_parent()

    def find_children(self, element: BeautifulSoup) -> List[BeautifulSoup]:
        """Find all children of a given HTML element."""
        return element.find_all(recursive=False)

    def find_descendants(self, element: BeautifulSoup) -> List[BeautifulSoup]:
        """Find all descendants of a given HTML element."""
        return element.find_all()
