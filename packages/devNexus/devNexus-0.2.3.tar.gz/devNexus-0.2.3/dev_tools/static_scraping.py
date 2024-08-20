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

    def find_by_id(self, element_id: str) -> Optional[str]:
        """Find an HTML element by its ID and return its text content."""
        element = self.soup.find(id=element_id)
        return element.get_text(strip=True) if element else None

    def find_by_class(self, class_name: str) -> List[str]:
        """Find HTML elements by their class name and return their text content."""
        elements = self.soup.find_all(class_=class_name)
        return [element.get_text(strip=True) for element in elements]

    def find_by_tag(self, tag_name: str) -> List[str]:
        """Find HTML elements by their tag name and return their text content."""
        elements = self.soup.find_all(tag_name)
        return [element.get_text(strip=True) for element in elements]

    def find_by_css(self, css_selector: str) -> List[str]:
        """Find HTML elements using a CSS selector and return their text content."""
        elements = self.soup.select(css_selector)
        return [element.get_text(strip=True) for element in elements]

    def find_by_attribute(self, tag_name: str, attribute_name: str, attribute_value: str) -> List[str]:
        """Find HTML elements by tag name and attribute, and return their text content."""
        elements = self.soup.find_all(tag_name, {attribute_name: attribute_value})
        return [element.get_text(strip=True) for element in elements]

    def find_text(self, text: str) -> List[str]:
        """Find HTML elements containing the given text and return their text content."""
        elements = self.soup.find_all(string=lambda t: text in t)
        return [element.strip() for element in elements]

    def get_links(self) -> List[str]:
        """Get all hyperlinks (anchor tags) on the page and return their href attributes."""
        return [a['href'] for a in self.soup.find_all('a', href=True)]

    def get_images(self) -> List[str]:
        """Get all image sources (img tags) on the page and return their src attributes."""
        return [img['src'] for img in self.soup.find_all('img', src=True)]

    def get_text(self) -> str:
        """Get all the text content of the page."""
        return self.soup.get_text()

    def find_next_sibling(self, element: BeautifulSoup) -> Optional[str]:
        """Find the next sibling of a given HTML element and return its text content."""
        sibling = element.find_next_sibling()
        return sibling.get_text(strip=True) if sibling else None

    def find_previous_sibling(self, element: BeautifulSoup) -> Optional[str]:
        """Find the previous sibling of a given HTML element and return its text content."""
        sibling = element.find_previous_sibling()
        return sibling.get_text(strip=True) if sibling else None

    def find_parent(self, element: BeautifulSoup) -> Optional[str]:
        """Find the parent of a given HTML element and return its text content."""
        parent = element.find_parent()
        return parent.get_text(strip=True) if parent else None

    def find_children(self, element: BeautifulSoup) -> List[str]:
        """Find all children of a given HTML element and return their text content."""
        children = element.find_all(recursive=False)
        return [child.get_text(strip=True) for child in children]

    def find_descendants(self, element: BeautifulSoup) -> List[str]:
        """Find all descendants of a given HTML element and return their text content."""
        descendants = element.find_all()
        return [descendant.get_text(strip=True) for descendant in descendants]
