# iso2automation

This repository automates the flows related to user type management in the ISO2 system

## Overview

The project provides automated testing for CRUD (Create, Read, Update, Delete) operations of user types and their associated workflows. It ensures the reliability and consistency of key functionalities including permissions management and visualization settings.

## Main Flows

The automation covers the following main flows:

- **User Type CRUD Operations**: Automated testing of creating, reading, updating, and deleting user types
- **Permission Configuration**: Automated workflows for setting and validating user permissions
- **Visualization Settings**: Automated testing of UI visibility and display configurations for different user types

## Technology Stack

- **Language**: Python
- **Framework**: Playwright
- **Version**: Python 3.x with Playwright for Python

## Getting Started

### Prerequisites

- Python 3.x installed
- Playwright for Python

### Installation

```bash
pip install playwright
playwright install
```

### Running Tests

```bash
pytest test_example.py
```

## Project Structure

```
iso2automation/
├── README.md
├── test_example.py
└── __pycache__/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.
