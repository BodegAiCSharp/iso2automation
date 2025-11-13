"""
Visualization Page Object
Handles all interactions with the visualization settings page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class VisualizationPage(BasePage):
    """Visualization settings page object"""
    
    # Locators
    USER_TYPE_SELECTOR = "select#userType"
    VISIBILITY_TOGGLE = "input[type='checkbox'][data-visibility]"
    DISPLAY_OPTION = "input[type='radio'][data-display]"
    SAVE_SETTINGS_BUTTON = "button[data-action='save-settings']"
    SUCCESS_MESSAGE = ".success-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def select_user_type(self, user_type: str):
        """Select a user type from dropdown"""
        self.page.select_option(self.USER_TYPE_SELECTOR, user_type)
    
    def set_visibility(self, element_name: str, visible: bool):
        """Set visibility for a UI element"""
        toggle_selector = f"input[data-visibility='{element_name}']"
        if visible:
            self.page.check(toggle_selector)
        else:
            self.page.uncheck(toggle_selector)
    
    def select_display_option(self, option_name: str):
        """Select a display option"""
        option_selector = f"input[data-display='{option_name}']"
        self.page.check(option_selector)
    
    def save_settings(self):
        """Save the visualization settings"""
        self.click_element(self.SAVE_SETTINGS_BUTTON)
    
    def is_element_visible_for_user_type(self, element_name: str) -> bool:
        """Check if an element is set to visible"""
        toggle_selector = f"input[data-visibility='{element_name}']"
        return self.page.is_checked(toggle_selector)
    
    def configure_visualization(self, user_type: str, visibility_settings: dict):
        """
        Configure visualization settings for a user type
        
        Args:
            user_type: The user type to configure
            visibility_settings: Dictionary with element names as keys and boolean values
        """
        self.select_user_type(user_type)
        for element_name, visible in visibility_settings.items():
            self.set_visibility(element_name, visible)
        self.save_settings()
    
    def get_success_message(self) -> str:
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
