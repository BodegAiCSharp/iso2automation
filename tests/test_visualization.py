"""
Test cases for Visualization settings
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.visualization_page import VisualizationPage


class TestVisualization:
    """Test suite for Visualization settings"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.visualization_page = VisualizationPage(page)
        
        # Navigate and login (adjust URL as needed)
        self.login_page.navigate_to("https://your-app-url.com/login")
        self.login_page.login("admin", "admin123")
        
        # Navigate to visualization page
        self.visualization_page.navigate_to("https://your-app-url.com/visualization")
    
    def test_set_element_visibility(self):
        """Test setting visibility for a single UI element"""
        user_type = "Manager"
        element_name = "admin_panel"
        
        self.visualization_page.select_user_type(user_type)
        self.visualization_page.set_visibility(element_name, True)
        self.visualization_page.save_settings()
        
        # Verify visibility was set
        assert self.visualization_page.is_element_visible_for_user_type(element_name)
    
    def test_hide_element(self):
        """Test hiding a UI element for a user type"""
        user_type = "Viewer"
        element_name = "edit_button"
        
        self.visualization_page.select_user_type(user_type)
        self.visualization_page.set_visibility(element_name, False)
        self.visualization_page.save_settings()
        
        # Verify element is hidden
        assert not self.visualization_page.is_element_visible_for_user_type(element_name)
    
    def test_configure_multiple_visibility_settings(self):
        """Test configuring visibility for multiple UI elements"""
        user_type = "Editor"
        visibility_settings = {
            "dashboard": True,
            "reports": True,
            "admin_panel": False,
            "user_management": False
        }
        
        self.visualization_page.configure_visualization(user_type, visibility_settings)
        
        # Verify all visibility settings were applied
        for element_name, expected_visibility in visibility_settings.items():
            assert self.visualization_page.is_element_visible_for_user_type(element_name) == expected_visibility
    
    def test_select_display_option(self):
        """Test selecting a display option"""
        user_type = "Admin"
        display_option = "grid_view"
        
        self.visualization_page.select_user_type(user_type)
        self.visualization_page.select_display_option(display_option)
        self.visualization_page.save_settings()
        
        # Verify success message
        # This will depend on your application's behavior
