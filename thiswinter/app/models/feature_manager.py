"""
Feature Manager - Manages feature flags and toggles
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from config import settings
except ImportError:
    # Fallback settings if config not available
    class settings:
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


class FeatureManager:
    """Manages feature flags and feature toggles"""
    
    def __init__(self):
        self.features = self._initialize_features()
        self.feature_states = {}  # Track custom feature states
    
    def _initialize_features(self):
        """Initialize all features with their default states"""
        return {
            'questionnaire': {
                'id': 'questionnaire',
                'name': 'Advanced Questionnaire',
                'description': 'Extended questionnaire system for comprehensive assessment',
                'enabled': settings.DEFAULT_FEATURES.get('questionnaire', True),
                'category': 'core',
                'dependencies': []
            },
            'case_management': {
                'id': 'case_management',
                'name': 'Case Management',
                'description': 'Comprehensive case tracking and management',
                'enabled': settings.DEFAULT_FEATURES.get('case_management', True),
                'category': 'core',
                'dependencies': []
            },
            'task_assignment': {
                'id': 'task_assignment',
                'name': 'Task Assignment',
                'description': 'Automatic task creation and assignment to clients and staff',
                'enabled': settings.DEFAULT_FEATURES.get('task_assignment', True),
                'category': 'core',
                'dependencies': ['case_management']
            },
            'admin_portal': {
                'id': 'admin_portal',
                'name': 'Admin Portal',
                'description': 'Advanced administrative portal with full system control',
                'enabled': settings.DEFAULT_FEATURES.get('admin_portal', True),
                'category': 'administration',
                'dependencies': []
            },
            'client_portal': {
                'id': 'client_portal',
                'name': 'Client Portal',
                'description': 'Client-facing portal for self-service',
                'enabled': settings.DEFAULT_FEATURES.get('client_portal', True),
                'category': 'core',
                'dependencies': []
            },
            'reporting': {
                'id': 'reporting',
                'name': 'Reporting',
                'description': 'Generate comprehensive reports and analytics',
                'enabled': settings.DEFAULT_FEATURES.get('reporting', True),
                'category': 'analytics',
                'dependencies': []
            },
            'notifications': {
                'id': 'notifications',
                'name': 'Notifications',
                'description': 'Real-time notifications and alerts',
                'enabled': settings.DEFAULT_FEATURES.get('notifications', True),
                'category': 'communication',
                'dependencies': []
            },
            'resource_library': {
                'id': 'resource_library',
                'name': 'Resource Library',
                'description': 'Access to educational resources and materials',
                'enabled': settings.DEFAULT_FEATURES.get('resource_library', True),
                'category': 'resources',
                'dependencies': []
            },
            'self_help_tools': {
                'id': 'self_help_tools',
                'name': 'Self-Help Tools',
                'description': 'Interactive self-help and wellness tools',
                'enabled': settings.DEFAULT_FEATURES.get('self_help_tools', True),
                'category': 'resources',
                'dependencies': []
            },
            'appointments': {
                'id': 'appointments',
                'name': 'Appointments',
                'description': 'Appointment scheduling and management',
                'enabled': settings.DEFAULT_FEATURES.get('appointments', True),
                'category': 'scheduling',
                'dependencies': []
            },
            'messaging': {
                'id': 'messaging',
                'name': 'Messaging',
                'description': 'Internal messaging system',
                'enabled': settings.DEFAULT_FEATURES.get('messaging', True),
                'category': 'communication',
                'dependencies': []
            },
            'analytics': {
                'id': 'analytics',
                'name': 'Analytics Dashboard',
                'description': 'Advanced analytics and data visualization',
                'enabled': settings.DEFAULT_FEATURES.get('analytics', True),
                'category': 'analytics',
                'dependencies': []
            },
            'export': {
                'id': 'export',
                'name': 'Data Export',
                'description': 'Export data to various formats (CSV, PDF, Excel)',
                'enabled': settings.DEFAULT_FEATURES.get('export', True),
                'category': 'data',
                'dependencies': []
            },
            'backup': {
                'id': 'backup',
                'name': 'Automated Backup',
                'description': 'Automatic system backups',
                'enabled': settings.DEFAULT_FEATURES.get('backup', True),
                'category': 'administration',
                'dependencies': []
            },
            'audit_log': {
                'id': 'audit_log',
                'name': 'Audit Log',
                'description': 'Comprehensive audit trail of all system actions',
                'enabled': settings.DEFAULT_FEATURES.get('audit_log', True),
                'category': 'security',
                'dependencies': []
            },
            'theme_customization': {
                'id': 'theme_customization',
                'name': 'Theme Customization',
                'description': 'Ability to customize and switch themes',
                'enabled': True,
                'category': 'customization',
                'dependencies': []
            },
            'widget_customization': {
                'id': 'widget_customization',
                'name': 'Widget Customization',
                'description': 'Toggle and configure dashboard widgets',
                'enabled': True,
                'category': 'customization',
                'dependencies': []
            },
            'layout_customization': {
                'id': 'layout_customization',
                'name': 'Layout Customization',
                'description': 'Customize dashboard layouts',
                'enabled': True,
                'category': 'customization',
                'dependencies': []
            },
            'multi_language': {
                'id': 'multi_language',
                'name': 'Multi-Language Support',
                'description': 'Support for multiple languages',
                'enabled': False,
                'category': 'localization',
                'dependencies': []
            },
            'api_access': {
                'id': 'api_access',
                'name': 'API Access',
                'description': 'RESTful API for external integrations',
                'enabled': True,
                'category': 'integration',
                'dependencies': []
            }
        }
    
    def get_all_features(self):
        """Get all features with their current states"""
        features = []
        for feature_id, feature in self.features.items():
            feature_data = feature.copy()
            # Override enabled state if explicitly set
            if feature_id in self.feature_states:
                feature_data['enabled'] = self.feature_states[feature_id]
            features.append(feature_data)
        return features
    
    def get_feature(self, feature_id):
        """Get specific feature"""
        feature = self.features.get(feature_id)
        if feature and feature_id in self.feature_states:
            feature = feature.copy()
            feature['enabled'] = self.feature_states[feature_id]
        return feature
    
    def is_enabled(self, feature_id):
        """Check if a feature is enabled"""
        if feature_id in self.feature_states:
            return self.feature_states[feature_id]
        
        feature = self.features.get(feature_id)
        return feature['enabled'] if feature else False
    
    def toggle_feature(self, feature_id, enabled):
        """Toggle feature on/off"""
        if feature_id not in self.features:
            return {'success': False, 'message': 'Feature not found'}
        
        # Check dependencies if disabling
        if not enabled:
            dependent_features = self._get_dependent_features(feature_id)
            if dependent_features:
                return {
                    'success': False,
                    'message': f'Cannot disable. Other features depend on this: {", ".join(dependent_features)}'
                }
        
        # Check if dependencies are enabled when enabling
        if enabled:
            dependencies = self.features[feature_id].get('dependencies', [])
            for dep in dependencies:
                if not self.is_enabled(dep):
                    return {
                        'success': False,
                        'message': f'Cannot enable. Dependency "{dep}" is disabled.'
                    }
        
        self.feature_states[feature_id] = enabled
        return {
            'success': True,
            'message': f'Feature {feature_id} {"enabled" if enabled else "disabled"}'
        }
    
    def _get_dependent_features(self, feature_id):
        """Get features that depend on this feature"""
        dependent = []
        for fid, feature in self.features.items():
            if feature_id in feature.get('dependencies', []):
                if self.is_enabled(fid):
                    dependent.append(feature['name'])
        return dependent
    
    def get_enabled_features(self):
        """Get list of enabled feature IDs"""
        enabled = []
        for feature_id, feature in self.features.items():
            is_enabled = self.feature_states.get(feature_id, feature['enabled'])
            if is_enabled:
                enabled.append(feature_id)
        return enabled
    
    def get_features_by_category(self, category):
        """Get features filtered by category"""
        return [f for f in self.get_all_features() if f['category'] == category]
    
    def reset_to_defaults(self):
        """Reset all features to their default states"""
        self.feature_states = {}
        return {'success': True, 'message': 'All features reset to defaults'}
