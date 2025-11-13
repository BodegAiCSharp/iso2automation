"""
Base Page class that all page objects will inherit from.
Contains common methods and properties shared across all pages.
"""
from playwright.sync_api import Page, expect


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str):
        """Navigate to a specific URL"""
        self.page.goto(url)
    
    def get_title(self) -> str:
        """Get the page title"""
        return self.page.title()
    
    def wait_for_element(self, selector: str, timeout: int = 30000):
        """Wait for an element to be visible"""
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click_element(self, selector: str):
        """Click on an element"""
        self.page.click(selector)
    
    def fill_input(self, selector: str, text: str):
        """Fill an input field"""
        self.page.fill(selector, text)
    
    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        return self.page.text_content(selector)
    
    def is_visible(self, selector: str) -> bool:
        """Check if an element is visible"""
        return self.page.is_visible(selector)
    
    def wait_for_url(self, url: str, timeout: int = 30000):
        """Wait for URL to match"""
        self.page.wait_for_url(url, timeout=timeout)
