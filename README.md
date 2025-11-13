# iso2automation

This repository automates the flows related to user type management in the ISO2 system.

## Overview

The project provides automated testing for CRUD (Create, Read, Update, Delete) operations of user types and their associated workflows. It ensures the reliability and consistency of key functionalities including permissions management and visualization settings.

The project follows the **Page Object Model (POM)** design pattern for better maintainability and scalability.

## Main Flows

The automation covers the following main flows:

- **User Type CRUD Operations**: Automated testing of creating, reading, updating, and deleting user types
- **Permission Configuration**: Automated workflows for setting and validating user permissions
- **Visualization Settings**: Automated testing of UI visibility and display configurations for different user types

## Technology Stack

- **Language**: Python 3.x
- **Framework**: Playwright for Python
- **Testing Framework**: Pytest
- **Design Pattern**: Page Object Model (POM)

## Project Structure

```
iso2automation/
├── config/                      # Configuration files
│   ├── __init__.py
│   └── config.py               # Environment and browser configurations
├── pages/                       # Page Object Models
│   ├── __init__.py
│   ├── base_page.py            # Base page with common methods
│   ├── login_page.py           # Login page object
│   ├── user_type_page.py       # User type management page object
│   ├── permissions_page.py     # Permissions configuration page object
│   └── visualization_page.py   # Visualization settings page object
├── tests/                       # Test files
│   ├── __init__.py
│   ├── test_user_type_crud.py  # User type CRUD tests
│   ├── test_permissions.py     # Permission configuration tests
│   └── test_visualization.py   # Visualization settings tests
├── utils/                       # Utility functions
│   ├── __init__.py
│   ├── helpers.py              # Helper functions
│   └── logger.py               # Logging utilities
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── conftest.py                  # Pytest fixtures and hooks
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/BodegAiCSharp/iso2automation.git
cd iso2automation
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Configure environment variables:
```bash
# Copy the example file
copy .env.example .env

# Edit .env with your configuration
```

### Configuration

Update the `.env` file with your specific settings:

- `BASE_URL`: The URL of your application
- `ADMIN_USERNAME` and `ADMIN_PASSWORD`: Test credentials
- `HEADLESS`: Set to `true` for headless browser mode
- `BROWSER`: Choose between `chromium`, `firefox`, or `webkit`

### Running Tests

Run all tests:
```bash
pytest
```

Run specific test file:
```bash
pytest tests/test_user_type_crud.py
```

Run tests with specific marker:
```bash
pytest -m crud
pytest -m permissions
pytest -m visualization
```

Run tests in headed mode (visible browser):
```bash
pytest --headed
```

Generate HTML report:
```bash
pytest --html=report.html
```

### Test Markers

The project uses pytest markers to categorize tests:

- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression tests
- `@pytest.mark.crud` - CRUD operation tests
- `@pytest.mark.permissions` - Permission configuration tests
- `@pytest.mark.visualization` - Visualization settings tests

## Page Object Model Structure

Each page object inherits from `BasePage` and encapsulates:

- **Locators**: Element selectors for the page
- **Actions**: Methods to interact with page elements
- **Validations**: Methods to verify page state

Example:
```python
from pages.user_type_page import UserTypePage

def test_create_user_type(page):
    user_type_page = UserTypePage(page)
    user_type_page.navigate_to(BASE_URL + "/user-types")
    user_type_page.create_user_type("Manager", "Manager role")
    assert user_type_page.is_user_type_visible("Manager")
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
