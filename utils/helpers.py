"""
Helper utilities for test automation
"""
import random
import string
from datetime import datetime
from typing import Optional


def generate_random_string(length: int = 10) -> str:
    """Generate a random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_unique_name(prefix: str = "test") -> str:
    """Generate a unique name with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}"


def generate_email(username: Optional[str] = None) -> str:
    """Generate a random email address"""
    if username is None:
        username = generate_random_string(8)
    return f"{username}@test.com"


def wait_for_condition(condition_func, timeout: int = 10, interval: float = 0.5) -> bool:
    """
    Wait for a condition to be true
    
    Args:
        condition_func: Function that returns boolean
        timeout: Maximum time to wait in seconds
        interval: Time between checks in seconds
    
    Returns:
        True if condition met, False if timeout
    """
    import time
    start_time = time.time()
    while time.time() - start_time < timeout:
        if condition_func():
            return True
        time.sleep(interval)
    return False


def take_screenshot(page, name: str, directory: str = "screenshots"):
    """Take a screenshot and save it"""
    import os
    os.makedirs(directory, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(directory, f"{name}_{timestamp}.png")
    page.screenshot(path=filepath)
    return filepath


def format_date(date_format: str = "%Y-%m-%d") -> str:
    """Get current date in specified format"""
    return datetime.now().strftime(date_format)


def format_datetime(datetime_format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Get current datetime in specified format"""
    return datetime.now().strftime(datetime_format)
