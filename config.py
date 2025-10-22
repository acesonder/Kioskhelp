"""
Kiosk Self-Help System Configuration
"""

# Application Settings
APP_NAME = "KioskHelp"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Kiosk-based self-help system for vulnerable clients"

# Database Settings
DATABASE = {
    'type': 'sqlite',
    'name': 'kioskhelp.db',
    'path': 'data/'
}

# Session Settings
SESSION_TIMEOUT = 300  # 5 minutes of inactivity

# Security Settings
ENCRYPTION_ENABLED = True
CONSENT_REQUIRED = True

# Module Settings
MODULES = {
    'registration': True,
    'consent': True,
    'intake': True,
    'assessment': True,
    'referral': True,
    'communication': True,
    'resources': True,
    'case_management': True,
    'self_help_tools': True
}

# Assessment Settings
ASSESSMENT_CATEGORIES = [
    'housing',
    'food_security',
    'healthcare',
    'mental_health',
    'employment',
    'legal_support',
    'education',
    'transportation',
    'family_services'
]

# Service Provider Integration
SERVICE_PROVIDERS = {
    'enabled': True,
    'auto_referral': True,
    'notification_enabled': True
}

# User Interface Settings
UI = {
    'language': 'en',
    'accessibility': True,
    'large_text_mode': True,
    'high_contrast_mode': True,
    'audio_support': True
}

# Privacy Settings
PRIVACY = {
    'data_retention_days': 365,
    'anonymous_mode': True,
    'gdpr_compliant': True
}
