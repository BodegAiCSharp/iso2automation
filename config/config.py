"""
Configuration settings for the test automation framework
"""
import os
from typing import Dict, Any


class Config:
    """Base configuration class"""
    
    # Application URLs
    BASE_URL = os.getenv("BASE_URL", "https://your-app-url.com")
    LOGIN_URL = f"{BASE_URL}/login"
    USER_TYPES_URL = f"{BASE_URL}/user-types"
    PERMISSIONS_URL = f"{BASE_URL}/permissions"
    VISUALIZATION_URL = f"{BASE_URL}/visualization"
    
    # Test credentials
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
    
    # Browser settings
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    VIEWPORT_WIDTH = int(os.getenv("VIEWPORT_WIDTH", "1920"))
    VIEWPORT_HEIGHT = int(os.getenv("VIEWPORT_HEIGHT", "1080"))
    
    # Timeout settings (in milliseconds)
    DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", "30000"))
    NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "30000"))
    
    # Screenshot settings
    SCREENSHOT_ON_FAILURE = os.getenv("SCREENSHOT_ON_FAILURE", "true").lower() == "true"
    SCREENSHOT_DIR = os.getenv("SCREENSHOT_DIR", "screenshots")
    
    # Video recording
    RECORD_VIDEO = os.getenv("RECORD_VIDEO", "false").lower() == "true"
    VIDEO_DIR = os.getenv("VIDEO_DIR", "videos")
    
    # Trace settings
    TRACE_ON = os.getenv("TRACE_ON", "false").lower() == "true"
    TRACE_DIR = os.getenv("TRACE_DIR", "traces")
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """Get browser configuration"""
        return {
            "headless": cls.HEADLESS,
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT
            },
            "record_video_dir": cls.VIDEO_DIR if cls.RECORD_VIDEO else None,
        }
    
    @classmethod
    def get_context_config(cls) -> Dict[str, Any]:
        """Get context configuration"""
        return {
            "viewport": {
                "width": cls.VIEWPORT_WIDTH,
                "height": cls.VIEWPORT_HEIGHT
            },
            "record_video_dir": cls.VIDEO_DIR if cls.RECORD_VIDEO else None,
        }


class DevelopmentConfig(Config):
    """Development environment configuration"""
    DEBUG = True
    BASE_URL = "http://localhost:3000"


class StagingConfig(Config):
    """Staging environment configuration"""
    BASE_URL = "https://staging.your-app-url.com"


class ProductionConfig(Config):
    """Production environment configuration"""
    BASE_URL = "https://your-app-url.com"
    HEADLESS = True


# Environment configuration mapping
config_by_name = {
    "development": DevelopmentConfig,
    "staging": StagingConfig,
    "production": ProductionConfig,
    "default": Config
}


def get_config(env_name: str = None) -> Config:
    """Get configuration based on environment name"""
    if env_name is None:
        env_name = os.getenv("ENV", "default")
    return config_by_name.get(env_name, Config)
