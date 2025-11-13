"""
Permissions Page Object
Handles all interactions with the permissions configuration page
"""
from playwright.sync_api import Page
from pages.base_page import BasePage


class PermissionsPage(BasePage):
    """Permissions configuration page object"""
    
    # Locators
    USER_TYPE_SELECTOR = "select#userType"
    PERMISSION_CHECKBOX = "input[type='checkbox'][data-permission]"
    SAVE_PERMISSIONS_BUTTON = "button[data-action='save-permissions']"
    RESET_BUTTON = "button[data-action='reset']"
    SUCCESS_MESSAGE = ".success-message"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def select_user_type(self, user_type: str):
        """Select a user type from dropdown"""
        self.page.select_option(self.USER_TYPE_SELECTOR, user_type)
    
    def set_permission(self, permission_name: str, enabled: bool):
        """Set a specific permission on or off"""
        checkbox_selector = f"input[data-permission='{permission_name}']"
        if enabled:
            self.page.check(checkbox_selector)
        else:
            self.page.uncheck(checkbox_selector)
    
    def save_permissions(self):
        """Save the permission configuration"""
        self.click_element(self.SAVE_PERMISSIONS_BUTTON)
    
    def reset_permissions(self):
        """Reset permissions to default"""
        self.click_element(self.RESET_BUTTON)
    
    def is_permission_enabled(self, permission_name: str) -> bool:
        """Check if a permission is enabled"""
        checkbox_selector = f"input[data-permission='{permission_name}']"
        return self.page.is_checked(checkbox_selector)
    
    def configure_permissions(self, user_type: str, permissions: dict):
        """
        Configure multiple permissions for a user type
        
        Args:
            user_type: The user type to configure
            permissions: Dictionary with permission names as keys and boolean values
        """
        self.select_user_type(user_type)
        for permission_name, enabled in permissions.items():
            self.set_permission(permission_name, enabled)
        self.save_permissions()
    
    def get_success_message(self) -> str:
        """Get success message text"""
        return self.get_text(self.SUCCESS_MESSAGE)
