"""
Organizations Page Object
Handles all interactions with the organizations and admin user management pages
"""
from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class OrganizationsPage(BasePage):
    """Organizations page object for admin user management"""
    
    ORGANIZATIONS_GRID = "#organizations-grid, table"
    ORGANIZATION_TITLE = ".organization-title, h1"
    ADD_USER_BUTTON = 'button:has-text("Add")'
    USERS_GRID = "#organization-users-grid"
    
    ADD_ISO_USER_MODAL = "#addIsoUserModal"
    FIRST_NAME_INPUT = 'input[name="FirstName"]'
    LAST_NAME_INPUT = 'input[name="LastName"]'
    EMAIL_INPUT = 'input[name="Email"]'
    PHONE_INPUT = 'input[name="Phone"]'
    NOTIFICATIONS_ENABLED_CHECKBOX = 'input[name="NotificationsEnabled"]'
    IS_OWNER_CHECKBOX = 'input[name="IsOwner"]'
    SUBMIT_BUTTON = 'button:has-text("Submit")'
    CANCEL_BUTTON = 'button:has-text("Cancel")'
    MODAL_TITLE = ".modal-title"
    
    TOAST_MESSAGE = ".toast, [data-testid='toast']"
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def navigate_to_organizations(self):
        """Navigate to organizations page"""
        self.navigate_to("/organizations")
    
    def navigate_to_organization_detail(self, organization_id: str):
        """Navigate to specific organization detail page"""
        self.navigate_to(f"/organizations/{organization_id}")
    
    def verify_organizations_page(self):
        """Verify organizations page is displayed"""
        expect(self.page.locator(self.ORGANIZATIONS_GRID)).to_be_visible()
    
    def verify_organization_detail_page(self, organization_name: str):
        """Verify organization detail page is displayed"""
        expect(self.page.locator(self.ORGANIZATION_TITLE)).to_be_visible()
        expect(self.page.locator(self.ORGANIZATION_TITLE)).to_contain_text(organization_name)
    
    def open_add_user_modal(self):
        """Open the Add User modal"""
        self.click_element(self.ADD_USER_BUTTON)
        self.wait_for_element(self.ADD_ISO_USER_MODAL)
        expect(self.page.locator(self.MODAL_TITLE)).to_contain_text("Add User")
    
    def fill_user_form(self, user_data: dict):
        """Fill the user form with provided data"""
        self.fill_input(self.FIRST_NAME_INPUT, user_data['first_name'])
        self.fill_input(self.LAST_NAME_INPUT, user_data['last_name'])
        self.fill_input(self.EMAIL_INPUT, user_data['email'])
        
        if 'phone' in user_data:
            self.fill_input(self.PHONE_INPUT, user_data['phone'])
        
        if 'notifications_enabled' in user_data:
            checkbox = self.page.locator(self.NOTIFICATIONS_ENABLED_CHECKBOX)
            is_checked = checkbox.is_checked()
            if is_checked != user_data['notifications_enabled']:
                checkbox.click()
        
        if 'is_owner' in user_data:
            checkbox = self.page.locator(self.IS_OWNER_CHECKBOX)
            is_checked = checkbox.is_checked()
            if is_checked != user_data['is_owner']:
                checkbox.click()
    
    def submit_user_form(self):
        """Submit the user form"""
        self.click_element(self.SUBMIT_BUTTON)
    
    def cancel_user_form(self):
        """Cancel the user form"""
        self.click_element(self.CANCEL_BUTTON)
    
    def create_admin_user(self, user_data: dict):
        """Complete flow to create an admin user"""
        self.open_add_user_modal()
        self.fill_user_form(user_data)
        self.submit_user_form()
        
        toast = self.page.locator(self.TOAST_MESSAGE)
        toast.wait_for(state="visible", timeout=10000)
        
        modal = self.page.locator(self.ADD_ISO_USER_MODAL)
        modal.wait_for(state="hidden", timeout=10000)
    
    def verify_user_in_grid(self, email: str):
        """Verify user appears in the users grid"""
        user_row = self.page.locator(f'{self.USERS_GRID} tr:has-text("{email}")')
        expect(user_row).to_be_visible()
    
    def verify_add_user_modal_fields(self):
        """Verify all required fields are present in Add User modal"""
        expect(self.page.locator(self.FIRST_NAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.LAST_NAME_INPUT)).to_be_visible()
        expect(self.page.locator(self.EMAIL_INPUT)).to_be_visible()
        expect(self.page.locator(self.PHONE_INPUT)).to_be_visible()
        expect(self.page.locator(self.NOTIFICATIONS_ENABLED_CHECKBOX)).to_be_visible()
        expect(self.page.locator(self.IS_OWNER_CHECKBOX)).to_be_visible()
        expect(self.page.locator(self.SUBMIT_BUTTON)).to_be_visible()
        expect(self.page.locator(self.CANCEL_BUTTON)).to_be_visible()
    
    def verify_success_toast(self):
        """Verify success toast message is displayed"""
        toast = self.page.locator(self.TOAST_MESSAGE)
        expect(toast).to_be_visible(timeout=10000)
        expect(toast).to_contain_text("success")
    
    def verify_error_toast(self, error_text: str):
        """Verify error toast message is displayed with specific text"""
        toast = self.page.locator(self.TOAST_MESSAGE)
        expect(toast).to_be_visible(timeout=10000)
        expect(toast).to_contain_text(error_text)
    
    def is_modal_visible(self) -> bool:
        """Check if Add User modal is visible"""
        return self.is_visible(self.ADD_ISO_USER_MODAL)
