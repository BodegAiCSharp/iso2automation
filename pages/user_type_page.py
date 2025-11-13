"""
User Type Page Object
Handles all interactions with the user type management page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class UserTypePage(BasePage):
    """User Type management page object"""
    
    # Locators
    CREATE_USER_TYPE_BUTTON = "button[data-action='create']"
    USER_TYPE_NAME_INPUT = "#userTypeName"
    USER_TYPE_DESCRIPTION_INPUT = "#userTypeDescription"
    SAVE_BUTTON = "button[data-action='save']"
    CANCEL_BUTTON = "button[data-action='cancel']"
    DELETE_BUTTON = "button[data-action='delete']"
    EDIT_BUTTON = "button[data-action='edit']"
    USER_TYPE_TABLE = "table.user-types"
    SUCCESS_MESSAGE = ".success-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def click_create_user_type(self):
        """Click the create user type button"""
        self.click_element(self.CREATE_USER_TYPE_BUTTON)
    
    def fill_user_type_form(self, name: str, description: str):
        """Fill the user type form"""
        self.fill_input(self.USER_TYPE_NAME_INPUT, name)
        self.fill_input(self.USER_TYPE_DESCRIPTION_INPUT, description)
    
    def click_save(self):
        """Click the save button"""
        self.click_element(self.SAVE_BUTTON)
    
    def click_cancel(self):
        """Click the cancel button"""
        self.click_element(self.CANCEL_BUTTON)
    
    def create_user_type(self, name: str, description: str):
        """Complete flow to create a user type"""
        self.click_create_user_type()
        self.fill_user_type_form(name, description)
        self.click_save()
    
    def edit_user_type(self, user_type_name: str, new_name: str, new_description: str):
        """Edit an existing user type"""
        self.click_edit_button_for_user_type(user_type_name)
        self.fill_user_type_form(new_name, new_description)
        self.click_save()
    
    def delete_user_type(self, user_type_name: str):
        """Delete a user type"""
        self.click_delete_button_for_user_type(user_type_name)
    
    def click_edit_button_for_user_type(self, user_type_name: str):
        """Click edit button for a specific user type"""
        selector = f"tr:has-text('{user_type_name}') {self.EDIT_BUTTON}"
        self.click_element(selector)
    
    def click_delete_button_for_user_type(self, user_type_name: str):
        """Click delete button for a specific user type"""
        selector = f"tr:has-text('{user_type_name}') {self.DELETE_BUTTON}"
        self.click_element(selector)
    
    def is_user_type_visible(self, user_type_name: str) -> bool:
        """Check if a user type exists in the table"""
        selector = f"{self.USER_TYPE_TABLE} tr:has-text('{user_type_name}')"
        return self.is_visible(selector)
    
    def get_success_message(self) -> str:
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
