"""
Pytest configuration and fixtures
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from config.config import get_config
from utils.logger import get_default_logger
import os

# Get configuration
config = get_config()
logger = get_default_logger()


@pytest.fixture(scope="session")
def playwright_instance():
    """Create a Playwright instance for the test session"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright) -> Browser:
    """Create a browser instance for the test session"""
    logger.info(f"Launching {config.BROWSER} browser")
    
    browser_type = getattr(playwright_instance, config.BROWSER)
    browser = browser_type.launch(
        headless=config.HEADLESS,
        slow_mo=100 if not config.HEADLESS else 0
    )
    yield browser
    browser.close()
    logger.info("Browser closed")


@pytest.fixture(scope="function")
def context(browser: Browser) -> BrowserContext:
    """Create a new browser context for each test"""
    context = browser.new_context(
        viewport={
            "width": config.VIEWPORT_WIDTH,
            "height": config.VIEWPORT_HEIGHT
        },
        record_video_dir=config.VIDEO_DIR if config.RECORD_VIDEO else None
    )
    
    if config.TRACE_ON:
        context.tracing.start(screenshots=True, snapshots=True)
    
    yield context
    
    if config.TRACE_ON:
        os.makedirs(config.TRACE_DIR, exist_ok=True)
        trace_file = os.path.join(config.TRACE_DIR, f"trace_{pytest.timestamp()}.zip")
        context.tracing.stop(path=trace_file)
    
    context.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    """Create a new page for each test"""
    page = context.new_page()
    page.set_default_timeout(config.DEFAULT_TIMEOUT)
    
    yield page
    
    # Take screenshot on failure
    if config.SCREENSHOT_ON_FAILURE:
        test_failed = hasattr(pytest, "test_failed") and pytest.test_failed
        if test_failed:
            os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)
            screenshot_path = os.path.join(
                config.SCREENSHOT_DIR,
                f"failure_{pytest.current_test_name()}_{pytest.timestamp()}.png"
            )
            page.screenshot(path=screenshot_path)
            logger.error(f"Screenshot saved: {screenshot_path}")
    
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results"""
    outcome = yield
    rep = outcome.get_result()
    
    # Store test result for screenshot capture
    if rep.when == "call":
        pytest.test_failed = rep.failed
        pytest.current_test_name = lambda: item.name
        pytest.timestamp = lambda: __import__("datetime").datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session")
def base_url():
    """Provide base URL from config"""
    return config.BASE_URL


@pytest.fixture(scope="session")
def admin_credentials():
    """Provide admin credentials from config"""
    return {
        "username": config.ADMIN_USERNAME,
        "password": config.ADMIN_PASSWORD
    }
