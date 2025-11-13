"""
Login Page Object
Handles all interactions with the login page
Supports both traditional username/password and ISO2 email/verification code flows
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Login page object"""
    
    # Locators for traditional login
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    ERROR_MESSAGE = ".error-message"
    
    # Locators for ISO2 email/verification code flow
    WELCOME_HEADING = 'h1:has-text("Welcome to Bodega Ai")'
    EMAIL_INPUT = 'input[name="Email"]'
    CONTINUE_BUTTON = 'button:has-text("Continue")'
    CHECK_EMAIL_HEADING = 'h1:has-text("Check your email")'
    VERIFICATION_CODE_INPUT = 'input[type="text"]'
    SIGN_IN_BUTTON = 'button:has-text("Sign in")'
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def login(self, username: str, password: str):
        """Perform traditional login action"""
        self.fill_input(self.USERNAME_INPUT, username)
        self.fill_input(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
    
    def login_with_email_verification(self, email: str, verification_code: str = "123456"):
        """Perform ISO2 login with email and verification code"""
        self.enter_email(email)
        self.enter_verification_code(verification_code)
        self.wait_for_url("**/stores", timeout=30000)
    
    def enter_email(self, email: str):
        """Enter email and proceed to verification page"""
        self.fill_input(self.EMAIL_INPUT, email)
        self.click_element(self.CONTINUE_BUTTON)
        self.wait_for_element(self.CHECK_EMAIL_HEADING)
    
    def enter_verification_code(self, code: str):
        """Enter verification code and submit"""
        self.fill_input(self.VERIFICATION_CODE_INPUT, code)
        self.click_element(self.SIGN_IN_BUTTON)
    
    def verify_login_page(self):
        """Verify login page elements are visible"""
        expect(self.page.locator(self.WELCOME_HEADING)).to_be_visible()
        expect(self.page.locator(self.EMAIL_INPUT)).to_be_visible()
        expect(self.page.locator(self.CONTINUE_BUTTON)).to_be_visible()
    
    def verify_verification_page(self, email: str):
        """Verify verification code page is displayed"""
        expect(self.page.locator(self.CHECK_EMAIL_HEADING)).to_be_visible()
        expect(self.page.locator(f'text={email}')).to_be_visible()
        expect(self.page.locator(self.VERIFICATION_CODE_INPUT)).to_be_visible()
    
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_login_button_visible(self) -> bool:
        """Check if login button is visible"""
        return self.is_visible(self.LOGIN_BUTTON)
