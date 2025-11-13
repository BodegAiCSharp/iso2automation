"""
Test cases for Permissions configuration
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.permissions_page import PermissionsPage


class TestPermissions:
    """Test suite for Permissions configuration"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.permissions_page = PermissionsPage(page)
        
        # Navigate and login (adjust URL as needed)
        self.login_page.navigate_to("https://your-app-url.com/login")
        self.login_page.login("admin", "admin123")
        
        # Navigate to permissions page
        self.permissions_page.navigate_to("https://your-app-url.com/permissions")
    
    def test_set_single_permission(self):
        """Test setting a single permission for a user type"""
        user_type = "Manager"
        permission_name = "create_user"
        
        self.permissions_page.select_user_type(user_type)
        self.permissions_page.set_permission(permission_name, True)
        self.permissions_page.save_permissions()
        
        # Verify permission was set
        assert self.permissions_page.is_permission_enabled(permission_name)
    
    def test_configure_multiple_permissions(self):
        """Test configuring multiple permissions at once"""
        user_type = "Editor"
        permissions = {
            "create_content": True,
            "edit_content": True,
            "delete_content": False,
            "publish_content": False
        }
        
        self.permissions_page.configure_permissions(user_type, permissions)
        
        # Verify all permissions were set correctly
        for permission_name, expected_state in permissions.items():
            assert self.permissions_page.is_permission_enabled(permission_name) == expected_state
    
    def test_disable_permission(self):
        """Test disabling a permission"""
        user_type = "Viewer"
        permission_name = "edit_content"
        
        self.permissions_page.select_user_type(user_type)
        self.permissions_page.set_permission(permission_name, False)
        self.permissions_page.save_permissions()
        
        # Verify permission was disabled
        assert not self.permissions_page.is_permission_enabled(permission_name)
    
    def test_reset_permissions(self):
        """Test resetting permissions to default"""
        user_type = "Admin"
        
        self.permissions_page.select_user_type(user_type)
        self.permissions_page.reset_permissions()
        
        # Verify success message or default state
        # This will depend on your application's behavior
