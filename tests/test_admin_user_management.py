"""
Admin User Management Tests
Tests for ISO2 admin user creation, login, and logout functionality
"""
import pytest
import time
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.organizations_page import OrganizationsPage
from config.config import get_config

config = get_config()


@pytest.mark.admin
@pytest.mark.smoke
class TestISO2Authentication:
    """Test cases for authentication with qa_automation@bodegaai.com"""

    def test_successful_login_with_qa_automation(self, page: Page, base_url: str):
        """Test successful login with qa_automation@bodegaai.com"""
        login_page = LoginPage(page)
        
        login_page.navigate_to(base_url)
        login_page.verify_login_page()
        
        login_page.enter_email('qa_automation@bodegaai.com')
        login_page.verify_verification_page('qa_automation@bodegaai.com')
        
        login_page.enter_verification_code('123456')
        
        expect(page).to_have_url('**/stores', timeout=30000)

    def test_maintain_session_after_refresh(self, page: Page, base_url: str):
        """Test that session is maintained after page refresh"""
        login_page = LoginPage(page)
        
        login_page.navigate_to(base_url)
        login_page.login_with_email_verification('qa_automation@bodegaai.com')
        
        page.reload()
        
        expect(page).not_to_have_url('**/login')
        expect(page).to_have_url('**/stores')

    def test_invalid_verification_code(self, page: Page, base_url: str):
        """Test handling of invalid verification code"""
        login_page = LoginPage(page)
        
        login_page.navigate_to(base_url)
        login_page.enter_email('qa_automation@bodegaai.com')
        
        login_page.fill_input(login_page.VERIFICATION_CODE_INPUT, '000000')
        login_page.click_element(login_page.SIGN_IN_BUTTON)
        
        expect(page.locator(login_page.CHECK_EMAIL_HEADING)).to_be_visible()


@pytest.mark.admin
@pytest.mark.regression
class TestLogoutFunctionality:
    """Test cases for logout functionality"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login before each test"""
        login_page = LoginPage(page)
        login_page.navigate_to(base_url)
        login_page.login_with_email_verification('qa_automation@bodegaai.com')
        yield

    def test_successful_logout(self, page: Page):
        """Test successful logout from the application"""
        page.goto('/logout')
        
        expect(page).to_have_url('**/login', timeout=10000)
        expect(page.locator('h1:has-text("Welcome to Bodega Ai")')).to_be_visible()

    def test_session_cleared_after_logout(self, page: Page):
        """Test that session is cleared after logout"""
        page.goto('/logout')
        expect(page).to_have_url('**/login')
        
        page.goto('/stores')
        
        expect(page).to_have_url('**/login')

    def test_re_authentication_after_logout(self, page: Page):
        """Test that re-authentication is required after logout"""
        login_page = LoginPage(page)
        
        page.goto('/logout')
        expect(page).to_have_url('**/login')
        
        page.goto('/organizations')
        expect(page).to_have_url('**/login')
        
        login_page.enter_email('qa_automation@bodegaai.com')
        login_page.enter_verification_code('123456')
        expect(page).to_have_url('**/stores', timeout=30000)


@pytest.mark.admin
@pytest.mark.crud
class TestAdminUserCreation:
    """Test cases for admin user creation"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login before each test"""
        login_page = LoginPage(page)
        login_page.navigate_to(base_url)
        login_page.login_with_email_verification('qa_automation@bodegaai.com')
        yield

    def test_display_add_user_modal_fields(self, page: Page):
        """Test that Add User modal displays all required fields"""
        organizations_page = OrganizationsPage(page)
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.open_add_user_modal()
        organizations_page.verify_add_user_modal_fields()

    @pytest.mark.smoke
    def test_create_new_admin_user_successfully(self, page: Page):
        """Test successful creation of a new admin user"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'Test',
            'last_name': 'Admin',
            'email': f'testadmin{timestamp}@bodegaai.com',
            'phone': '(555) 123-4567',
            'notifications_enabled': True,
            'is_owner': False
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        organizations_page.verify_success_toast()
        
        page.wait_for_load_state('networkidle')
        organizations_page.verify_user_in_grid(test_user['email'])

    def test_validate_required_fields(self, page: Page):
        """Test validation of required fields when creating admin user"""
        organizations_page = OrganizationsPage(page)
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.open_add_user_modal()
        organizations_page.submit_user_form()
        
        assert organizations_page.is_modal_visible()
        
        first_name_input = page.locator(organizations_page.FIRST_NAME_INPUT)
        is_invalid = first_name_input.evaluate('el => !el.validity.valid')
        assert is_invalid

    def test_validate_email_format(self, page: Page):
        """Test email format validation when creating admin user"""
        organizations_page = OrganizationsPage(page)
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.open_add_user_modal()
        organizations_page.fill_input(organizations_page.FIRST_NAME_INPUT, 'Test')
        organizations_page.fill_input(organizations_page.LAST_NAME_INPUT, 'User')
        organizations_page.fill_input(organizations_page.EMAIL_INPUT, 'invalid-email')
        organizations_page.submit_user_form()
        
        assert organizations_page.is_modal_visible()
        
        email_input = page.locator(organizations_page.EMAIL_INPUT)
        is_invalid = email_input.evaluate('el => !el.validity.valid')
        assert is_invalid

    def test_prevent_duplicate_email(self, page: Page):
        """Test that duplicate email addresses are prevented"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'Duplicate',
            'last_name': 'Test',
            'email': f'duplicate{timestamp}@bodegaai.com',
            'phone': '(555) 999-8888',
            'notifications_enabled': True,
            'is_owner': False
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        page.wait_for_load_state('networkidle')
        
        organizations_page.open_add_user_modal()
        organizations_page.fill_user_form(test_user)
        organizations_page.submit_user_form()
        
        organizations_page.verify_error_toast('already exists')

    def test_create_user_with_minimal_fields(self, page: Page):
        """Test creating admin user with only required fields"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'Minimal',
            'last_name': 'User',
            'email': f'minimal{timestamp}@bodegaai.com'
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        
        page.wait_for_load_state('networkidle')
        organizations_page.verify_user_in_grid(test_user['email'])

    def test_create_user_with_all_fields(self, page: Page):
        """Test creating admin user with all optional fields"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'Complete',
            'last_name': 'User',
            'email': f'complete{timestamp}@bodegaai.com',
            'phone': '(555) 777-6666',
            'notifications_enabled': False,
            'is_owner': True
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        
        page.wait_for_load_state('networkidle')
        organizations_page.verify_user_in_grid(test_user['email'])
        
        user_row = page.locator(f'{organizations_page.USERS_GRID} tr:has-text("{test_user["email"]}")')
        expect(user_row).to_contain_text('Complete User')

    def test_cancel_user_creation(self, page: Page):
        """Test canceling admin user creation"""
        organizations_page = OrganizationsPage(page)
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.open_add_user_modal()
        organizations_page.fill_input(organizations_page.FIRST_NAME_INPUT, 'Cancel')
        organizations_page.fill_input(organizations_page.LAST_NAME_INPUT, 'Test')
        organizations_page.fill_input(organizations_page.EMAIL_INPUT, 'cancel@test.com')
        
        organizations_page.cancel_user_form()
        
        modal = page.locator(organizations_page.ADD_ISO_USER_MODAL)
        expect(modal).to_be_hidden()
        
        user_row = page.locator(f'{organizations_page.USERS_GRID} tr:has-text("cancel@test.com")')
        expect(user_row).not_to_be_visible()


@pytest.mark.admin
@pytest.mark.regression
class TestAdminUserEdgeCases:
    """Test cases for admin user creation edge cases"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, base_url: str):
        """Setup: Login before each test"""
        login_page = LoginPage(page)
        login_page.navigate_to(base_url)
        login_page.login_with_email_verification('qa_automation@bodegaai.com')
        yield

    def test_special_characters_in_names(self, page: Page):
        """Test handling of special characters in user names"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': "O'Brien",
            'last_name': 'Smith-Jones',
            'email': f'special{timestamp}@bodegaai.com'
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        
        page.wait_for_load_state('networkidle')
        organizations_page.verify_user_in_grid(test_user['email'])

    def test_long_names(self, page: Page):
        """Test handling of long names within limits"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'VeryLongFirstNameThatIsStillValid',
            'last_name': 'VeryLongLastNameThatIsStillValid',
            'email': f'longname{timestamp}@bodegaai.com'
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        
        page.wait_for_load_state('networkidle')
        organizations_page.verify_user_in_grid(test_user['email'])

    def test_phone_number_formatting(self, page: Page):
        """Test that phone numbers are formatted correctly"""
        organizations_page = OrganizationsPage(page)
        timestamp = int(time.time())
        
        test_user = {
            'first_name': 'Phone',
            'last_name': 'Test',
            'email': f'phone{timestamp}@bodegaai.com',
            'phone': '5551234567'
        }
        
        organizations_page.navigate_to_organizations()
        
        first_org_row = page.locator('table tbody tr').first
        first_org_row.click()
        page.wait_for_url('**/organizations/*')
        
        organizations_page.create_admin_user(test_user)
        
        page.wait_for_load_state('networkidle')
        
        user_row = page.locator(f'{organizations_page.USERS_GRID} tr:has-text("{test_user["email"]}")')
        expect(user_row).to_be_visible()
