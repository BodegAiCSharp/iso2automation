"""
Test cases for User Type CRUD operations
"""
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.user_type_page import UserTypePage


class TestUserTypeCRUD:
    """Test suite for User Type CRUD operations"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Setup before each test"""
        self.page = page
        self.login_page = LoginPage(page)
        self.user_type_page = UserTypePage(page)
        
        # Navigate and login (adjust URL as needed)
        self.login_page.navigate_to("https://your-app-url.com/login")
        self.login_page.login("admin", "admin123")
        
        # Navigate to user type page
        self.user_type_page.navigate_to("https://your-app-url.com/user-types")
    
    def test_create_user_type(self):
        """Test creating a new user type"""
        user_type_name = "Test User Type"
        user_type_description = "This is a test user type"
        
        self.user_type_page.create_user_type(user_type_name, user_type_description)
        
        # Verify user type was created
        assert self.user_type_page.is_user_type_visible(user_type_name)
    
    def test_read_user_type(self):
        """Test reading/viewing user types"""
        # Create a user type first
        user_type_name = "Read Test Type"
        self.user_type_page.create_user_type(user_type_name, "Description")
        
        # Verify it's visible in the list
        assert self.user_type_page.is_user_type_visible(user_type_name)
    
    def test_update_user_type(self):
        """Test updating an existing user type"""
        # Create a user type first
        original_name = "Original Type"
        self.user_type_page.create_user_type(original_name, "Original description")
        
        # Update the user type
        new_name = "Updated Type"
        new_description = "Updated description"
        self.user_type_page.edit_user_type(original_name, new_name, new_description)
        
        # Verify the update
        assert self.user_type_page.is_user_type_visible(new_name)
    
    def test_delete_user_type(self):
        """Test deleting a user type"""
        # Create a user type first
        user_type_name = "Type to Delete"
        self.user_type_page.create_user_type(user_type_name, "Will be deleted")
        
        # Delete the user type
        self.user_type_page.delete_user_type(user_type_name)
        
        # Verify it's no longer visible
        assert not self.user_type_page.is_user_type_visible(user_type_name)
