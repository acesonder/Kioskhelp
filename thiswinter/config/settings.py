"""
Web Portal Settings Configuration
"""

import os
import secrets

# Application Settings
APP_NAME = "KioskHelp Web Portal"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Comprehensive web-based platform for vulnerable client support"

# Security
SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Database Settings
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///kioskhelp_web.db')

# Session Settings
SESSION_TIMEOUT = 1800  # 30 minutes
PERMANENT_SESSION_LIFETIME = 3600  # 1 hour

# Admin Settings
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@kioskhelp.org')
ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'changeme123')  # Should be changed in production

# Feature Flags (can be toggled from admin panel)
DEFAULT_FEATURES = {
    'questionnaire': True,
    'case_management': True,
    'task_assignment': True,
    'admin_portal': True,
    'client_portal': True,
    'reporting': True,
    'notifications': True,
    'resource_library': True,
    'self_help_tools': True,
    'appointments': True,
    'messaging': True,
    'analytics': True,
    'export': True,
    'backup': True,
    'audit_log': True,
}

# Default Theme
DEFAULT_THEME = 'professional-blue'

# Available Themes (20 different themes)
THEMES = [
    'professional-blue',
    'modern-dark',
    'light-minimal',
    'warm-orange',
    'cool-green',
    'corporate-grey',
    'vibrant-purple',
    'ocean-blue',
    'sunset-red',
    'forest-green',
    'midnight-black',
    'pastel-pink',
    'earth-tone',
    'high-contrast',
    'accessibility-friendly',
    'classic-white',
    'gradient-blue',
    'material-design',
    'bootstrap-inspired',
    'custom-branded'
]

# Widget Configuration
AVAILABLE_WIDGETS = [
    'welcome_widget',
    'quick_actions',
    'recent_cases',
    'pending_tasks',
    'notifications',
    'calendar',
    'statistics',
    'resource_links',
    'announcements',
    'help_tips'
]

# Dashboard Layouts
DASHBOARD_LAYOUTS = [
    'default',
    'compact',
    'expanded',
    'grid-3col',
    'grid-4col',
    'sidebar-left',
    'sidebar-right',
    'split-screen',
    'tabbed',
    'accordion'
]

# Upload Settings
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif'}

# Pagination
ITEMS_PER_PAGE = 25

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'logs/kioskhelp_web.log'
