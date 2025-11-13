"""
Login Page Object
Handles all interactions with the login page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str):
        """Perform login action"""
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_login_button_visible(self) -> bool:
        """Check if login button is visible"""
        return self.is_visible(self.LOGIN_BUTTON)
