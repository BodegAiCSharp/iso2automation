# ISO2 Page Locators Documentation

This document provides comprehensive locator information for all pages in the ISO2 application (https://iso2.bodegaai.com/) for use in Playwright test automation.

## Table of Contents
1. [Login Page](#login-page)
2. [Verification Code Page](#verification-code-page)
3. [Organizations List Page](#organizations-list-page)
4. [Organization Detail Page](#organization-detail-page)
5. [Add ISO User Modal](#add-iso-user-modal)
6. [Edit ISO User Modal](#edit-iso-user-modal)
7. [Common Elements](#common-elements)

---

## Login Page

**URL:** `/Login` or `/` (redirects to login)

### Page Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Logo Image | CSS | `img[src*="Bodega_AI_logo"]` | Bodega AI logo |
| Page Title | CSS | `h1.login-title` | "Welcome to Bodega Ai ISO POS Portal" |
| Subtitle | CSS | `p.login-subtitle` | "Enter your email to get started" |
| Email Input | CSS | `input[name="Email"]` | Email input field |
| Email Input | ID | `#Email` | Email input field (alternative) |
| Email Input | Type | `input[type="email"]` | Email input field (alternative) |
| Continue Button | CSS | `button[type="submit"]` | Submit button |
| Continue Button | Text | `button:has-text("Continue")` | Submit button (alternative) |
| Validation Error | CSS | `.text-danger.field-validation-error` | Validation error message |
| Validation Error (Email) | CSS | `span[data-valmsg-for="Email"]` | Email-specific validation error |

### Assertions for Login Page

```python
# Verify login page is displayed
expect(page.locator('h1.login-title')).to_be_visible()
expect(page.locator('h1.login-title')).to_contain_text('Welcome to Bodega Ai')

# Verify email input is visible and enabled
expect(page.locator('input[name="Email"]')).to_be_visible()
expect(page.locator('input[name="Email"]')).to_be_enabled()

# Verify continue button is visible
expect(page.locator('button:has-text("Continue")')).to_be_visible()

# Verify error message for disabled account
expect(page.locator('.text-danger.field-validation-error')).to_contain_text('Account disabled')
```

### Validation Scenarios

1. **Empty Email:** Required field validation
2. **Invalid Email Format:** Email format validation
3. **Disabled Account:** "Account disabled." error message
4. **Valid Email:** Redirects to verification code page

---

## Verification Code Page

**URL:** `/VerifyCode`

### Page Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Logo Image | CSS | `img[src*="Bodega_AI_logo"]` | Bodega AI logo |
| Page Title | CSS | `h1.login-title` | "Check your email" |
| Subtitle | CSS | `p.login-subtitle` | Email confirmation message |
| Email Display | CSS | `p.login-subtitle strong` | User's email address |
| PIN Input | CSS | `input[name="Pin"]` | Verification code input |
| PIN Input | CSS | `.pin-input` | Verification code input (alternative) |
| PIN Input | Type | `input[type="text"]` | Verification code input (alternative) |
| Sign In Button | CSS | `button[type="submit"]` | Submit button |
| Sign In Button | Text | `button:has-text("Sign In")` | Submit button (alternative) |
| Resend Link | CSS | `a.resend-link` | "I didn't get the email" link |
| Resend Link | Href | `a[href="/Login"]` | Link back to login |
| Validation Error | CSS | `.text-danger.field-validation-error` | Validation error message |
| Validation Error (PIN) | CSS | `span[data-valmsg-for="Pin"]` | PIN-specific validation error |

### Assertions for Verification Code Page

```python
# Verify verification page is displayed
expect(page.locator('h1.login-title')).to_be_visible()
expect(page.locator('h1.login-title')).to_contain_text('Check your email')

# Verify email is displayed
expect(page.locator('p.login-subtitle strong')).to_contain_text(email)

# Verify PIN input is visible and enabled
expect(page.locator('input[name="Pin"]')).to_be_visible()
expect(page.locator('input[name="Pin"]')).to_be_enabled()
expect(page.locator('input[name="Pin"]')).to_have_attribute('maxlength', '6')

# Verify sign in button is visible
expect(page.locator('button:has-text("Sign In")')).to_be_visible()

# Verify resend link is visible
expect(page.locator('a.resend-link')).to_be_visible()
```

### Validation Scenarios

1. **Empty PIN:** Required field validation
2. **Invalid PIN:** Incorrect verification code error
3. **Valid PIN:** Redirects to stores page (`/stores`)
4. **PIN Format:** Only accepts 6 digits (maxlength="6")

---

## Organizations List Page

**URL:** `/organizations`

### Page Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Page Title | CSS | `h1.stores-title` | "Organization" |
| Add Button | CSS | `button[data-bs-target="#addOrganizationModal"]` | Add organization button |
| Add Button | Text | `button:has-text("Add")` | Add organization button (alternative) |
| Refresh Button | CSS | `.refresh-btn` | Refresh button |
| Organizations Grid | ID | `#organizations-grid` | Main grid container |
| Search Input | CSS | `#organizations-grid input[placeholder*="Search"]` | Search input field |
| Grid Table | CSS | `#organizations-grid table` | Organizations table |
| Grid Rows | CSS | `#organizations-grid table tbody tr` | Organization rows |
| Edit Button (in row) | CSS | `button[data-bs-target="#editOrganizationModal"]` | Edit organization button |
| View Stores Button | CSS | `button:has-text("View Stores")` | View stores button |

### Grid Columns

| Column Header | Field | Type |
|---------------|-------|------|
| NAME | name | text |
| SUPPORT PHONE | support_phone | phone |
| USERS | user_count | number |
| STORES | store_count | number |

### Assertions for Organizations Page

```python
# Verify organizations page is displayed
expect(page.locator('h1.stores-title')).to_be_visible()
expect(page.locator('h1.stores-title')).to_contain_text('Organization')

# Verify add button is visible
expect(page.locator('button:has-text("Add")')).to_be_visible()

# Verify grid is displayed
expect(page.locator('#organizations-grid')).to_be_visible()
expect(page.locator('#organizations-grid table')).to_be_visible()

# Verify search functionality
expect(page.locator('#organizations-grid input[placeholder*="Search"]')).to_be_visible()

# Click on organization row to navigate to detail
first_row = page.locator('#organizations-grid table tbody tr').first
first_row.click()
expect(page).to_have_url('**/organizations/*')
```

---

## Organization Detail Page

**URL:** `/organizations/{id}`

### Page Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Breadcrumb Link | CSS | `a.breadcrumb-link` | Back to organizations |
| Organization Title | CSS | `h1.organization-title` | Organization name |
| Support Phone | CSS | `p.organization-support` | Support phone display |
| View Stores Button | CSS | `button:has-text("View Stores")` | View stores button |
| Edit Button | CSS | `button[data-bs-target="#editOrganizationModal"]` | Edit organization button |
| Add User Button | CSS | `button[data-bs-target="#addIsoUserModal"]` | Add user button |
| Add User Button | Text | `button:has-text("Add")` | Add user button (alternative) |
| Users Grid | ID | `#organization-users-grid` | Users grid container |
| Users Table | CSS | `#organization-users-grid table` | Users table |
| User Rows | CSS | `#organization-users-grid table tbody tr` | User rows |
| No Users Message | CSS | `.text-center.text-muted` | "No BodegaAi POS login users configured" |

### Users Grid Columns

| Column Header | Field | Type |
|---------------|-------|------|
| NAME | FullName | text |
| EMAIL | email | text |
| PHONE | phone | phone |
| IS OWNER | is_owner | boolean |
| IS ACTIVE | is_active | boolean |
| NOTIFICATIONS ENABLED | notifications_enabled | boolean |

### Assertions for Organization Detail Page

```python
# Verify organization detail page is displayed
expect(page.locator('h1.organization-title')).to_be_visible()
expect(page.locator('p.organization-support')).to_be_visible()

# Verify add user button is visible
expect(page.locator('button[data-bs-target="#addIsoUserModal"]')).to_be_visible()

# Verify users grid is displayed
expect(page.locator('#organization-users-grid')).to_be_visible()

# Verify user appears in grid after creation
user_row = page.locator(f'#organization-users-grid table tbody tr:has-text("{email}")')
expect(user_row).to_be_visible()
```

---

## Add ISO User Modal

**Modal ID:** `#addIsoUserModal`

### Modal Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Modal Container | ID | `#addIsoUserModal` | Modal container |
| Modal Title | CSS | `#addIsoUserModal .modal-title` | "Add User" |
| Close Button | CSS | `#addIsoUserModal .btn-close` | Close button (X) |
| Form | ID | `#addIsoUserForm` | Form element |
| ISO ID Input (hidden) | ID | `#isoIdInput` | Hidden organization ID |
| First Name Input | CSS | `input[name="FirstName"]` | First name field |
| Last Name Input | CSS | `input[name="LastName"]` | Last name field |
| Email Input | CSS | `input[name="Email"]` | Email field |
| Phone Input | CSS | `input[name="Phone"]` | Phone field |
| Notifications Checkbox | CSS | `input[name="NotificationsEnabled"]` | Notifications enabled checkbox |
| Is Owner Checkbox | CSS | `input[name="IsOwner"]` | Is owner checkbox |
| Cancel Button | CSS | `#addIsoUserModal button:has-text("Cancel")` | Cancel button |
| Submit Button | CSS | `#addIsoUserModal button[type="submit"]` | Submit button |
| Submit Button | Text | `#addIsoUserModal button:has-text("Submit")` | Submit button (alternative) |
| Validation Error | CSS | `.validation-error[data-field="{FieldName}"]` | Field-specific validation error |

### Field Validation Errors

| Field | Locator | Required |
|-------|---------|----------|
| FirstName | `.validation-error[data-field="FirstName"]` | Yes |
| LastName | `.validation-error[data-field="LastName"]` | Yes |
| Email | `.validation-error[data-field="Email"]` | Yes |
| Phone | `.validation-error[data-field="Phone"]` | No |
| NotificationsEnabled | `.validation-error[data-field="NotificationsEnabled"]` | No |
| IsOwner | `.validation-error[data-field="IsOwner"]` | No |

### Assertions for Add User Modal

```python
# Verify modal is displayed
expect(page.locator('#addIsoUserModal')).to_be_visible()
expect(page.locator('#addIsoUserModal .modal-title')).to_contain_text('Add User')

# Verify all required fields are present
expect(page.locator('input[name="FirstName"]')).to_be_visible()
expect(page.locator('input[name="LastName"]')).to_be_visible()
expect(page.locator('input[name="Email"]')).to_be_visible()
expect(page.locator('input[name="Phone"]')).to_be_visible()
expect(page.locator('input[name="NotificationsEnabled"]')).to_be_visible()
expect(page.locator('input[name="IsOwner"]')).to_be_visible()

# Verify buttons are present
expect(page.locator('#addIsoUserModal button:has-text("Cancel")')).to_be_visible()
expect(page.locator('#addIsoUserModal button:has-text("Submit")')).to_be_visible()

# Verify modal closes after successful submission
expect(page.locator('#addIsoUserModal')).to_be_hidden()

# Verify validation errors are displayed
expect(page.locator('.validation-error[data-field="FirstName"]')).to_contain_text('error message')
```

### Form Submission

**Endpoint:** `POST /organizations/{isoId}`
**Method:** AJAX (fetch)
**Response:** JSON with `success` and `errors` fields

```javascript
// Success response
{
  "success": true
}

// Error response
{
  "success": false,
  "errors": {
    "FirstName": ["First name is required"],
    "Email": ["Email already exists"]
  },
  "message": "Validation failed"
}
```

---

## Edit ISO User Modal

**Modal ID:** `#editIsoUserModal`

### Modal Elements

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Modal Container | ID | `#editIsoUserModal` | Modal container |
| Modal Title | CSS | `#editIsoUserModal .modal-title` | "Edit User" |
| Close Button | CSS | `#editIsoUserModal .btn-close` | Close button (X) |
| Form | ID | `#editIsoUserForm` | Form element |
| User ID Input (hidden) | ID | `#editUserId` | Hidden user ID |
| First Name Input | CSS | `#editIsoUserModal input[name="FirstName"]` | First name field |
| Last Name Input | CSS | `#editIsoUserModal input[name="LastName"]` | Last name field |
| Email Input | CSS | `#editIsoUserModal input[name="Email"]` | Email field |
| Phone Input | CSS | `#editIsoUserModal input[name="Phone"]` | Phone field |
| Is Active Checkbox | ID | `#editIsActive` | Is active checkbox |
| Notifications Checkbox | ID | `#editNotificationsEnabled` | Notifications enabled checkbox |
| Is Owner Checkbox | ID | `#editIsOwner` | Is owner checkbox |
| Cancel Button | CSS | `#editIsoUserModal button:has-text("Cancel")` | Cancel button |
| Update Button | CSS | `#editIsoUserModal button[type="submit"]` | Update button |
| Update Button | Text | `#editIsoUserModal button:has-text("Update User")` | Update button (alternative) |

---

## Common Elements

### Toast Notifications

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Toast Container | CSS | `.toast` | Toast notification container |
| Toast Container | Attribute | `[data-testid="toast"]` | Toast notification (alternative) |
| Success Toast | CSS | `.toast.success` | Success notification |
| Error Toast | CSS | `.toast.error` | Error notification |

### Toast Assertions

```python
# Verify success toast is displayed
toast = page.locator('.toast, [data-testid="toast"]')
expect(toast).to_be_visible(timeout=10000)
expect(toast).to_contain_text('success')

# Verify error toast is displayed
expect(toast).to_be_visible(timeout=10000)
expect(toast).to_contain_text('error')
```

### Loading Overlay

| Element | Locator Type | Locator | Description |
|---------|--------------|---------|-------------|
| Loading Overlay | CSS | `.loading-overlay` | Loading overlay |

```python
# Wait for loading to complete
loading_overlay = page.locator('.loading-overlay')
if loading_overlay.is_visible():
    loading_overlay.wait_for(state='hidden', timeout=10000)
```

---

## Navigation Flow

### Complete Login Flow

```python
# 1. Navigate to login page
page.goto('https://iso2.bodegaai.com/')
expect(page.locator('h1.login-title')).to_contain_text('Welcome to Bodega Ai')

# 2. Enter email
page.locator('input[name="Email"]').fill('user@example.com')
page.locator('button:has-text("Continue")').click()

# 3. Verify verification page
expect(page.locator('h1.login-title')).to_contain_text('Check your email')
expect(page.locator('p.login-subtitle strong')).to_contain_text('user@example.com')

# 4. Enter verification code
page.locator('input[name="Pin"]').fill('123456')
page.locator('button:has-text("Sign In")').click()

# 5. Verify successful login
expect(page).to_have_url('**/stores', timeout=30000)
```

### Complete User Creation Flow

```python
# 1. Navigate to organizations
page.goto('/organizations')
expect(page.locator('h1.stores-title')).to_contain_text('Organization')

# 2. Click on organization
first_org = page.locator('#organizations-grid table tbody tr').first
first_org.click()
expect(page).to_have_url('**/organizations/*')

# 3. Open add user modal
page.locator('button[data-bs-target="#addIsoUserModal"]').click()
expect(page.locator('#addIsoUserModal')).to_be_visible()

# 4. Fill user form
page.locator('input[name="FirstName"]').fill('John')
page.locator('input[name="LastName"]').fill('Doe')
page.locator('input[name="Email"]').fill('john.doe@example.com')
page.locator('input[name="Phone"]').fill('(555) 123-4567')

# 5. Set checkboxes
notifications_checkbox = page.locator('input[name="NotificationsEnabled"]')
if not notifications_checkbox.is_checked():
    notifications_checkbox.click()

# 6. Submit form
page.locator('#addIsoUserModal button:has-text("Submit")').click()

# 7. Verify success
toast = page.locator('.toast, [data-testid="toast"]')
expect(toast).to_be_visible(timeout=10000)
expect(toast).to_contain_text('success')

# 8. Verify modal closes
expect(page.locator('#addIsoUserModal')).to_be_hidden(timeout=10000)

# 9. Verify user in grid
user_row = page.locator(f'#organization-users-grid table tbody tr:has-text("john.doe@example.com")')
expect(user_row).to_be_visible()
```

---

## Best Practices

### Waiting for Elements

```python
# Wait for page load
page.wait_for_load_state('networkidle')

# Wait for specific element
page.locator('selector').wait_for(state='visible', timeout=10000)

# Wait for URL change
page.wait_for_url('**/expected-path', timeout=30000)
```

### Handling Modals

```python
# Open modal
page.locator('button[data-bs-target="#modalId"]').click()
expect(page.locator('#modalId')).to_be_visible()

# Close modal
page.locator('#modalId .btn-close').click()
expect(page.locator('#modalId')).to_be_hidden()

# Or press Escape
page.keyboard.press('Escape')
```

### Form Validation

```python
# Check required field validation
page.locator('button[type="submit"]').click()
input_field = page.locator('input[name="FieldName"]')
is_invalid = input_field.evaluate('el => !el.validity.valid')
assert is_invalid

# Check validation error message
error = page.locator('.validation-error[data-field="FieldName"]')
expect(error).to_be_visible()
expect(error).to_contain_text('error message')
```

---

## Notes

1. **Authentication:** The application uses email/verification code authentication, not username/password
2. **Session Management:** Sessions are maintained after login and persist across page refreshes
3. **AJAX Forms:** Most modals use AJAX submission with JSON responses
4. **Toast Notifications:** Success/error messages are displayed via toast notifications
5. **Grid Interactions:** Clicking on grid rows navigates to detail pages
6. **Checkbox Handling:** Checkboxes need special handling to set true/false values
7. **Phone Formatting:** Phone numbers are automatically formatted with mask (123) 456-7890
8. **Validation:** Client-side and server-side validation both present
9. **Loading States:** Loading overlays may appear during async operations
10. **URL Patterns:** Organization detail pages use GUID in URL: `/organizations/{guid}`
