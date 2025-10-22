"""
Widget Manager - Manages dashboard widgets and layouts
"""


class WidgetManager:
    """Manages widgets and dashboard layouts"""
    
    def __init__(self):
        self.widgets = self._initialize_widgets()
        self.layouts = self._initialize_layouts()
        self.widget_states = {}  # Track enabled/disabled widgets
        self.layout_customizations = {}
        self.default_layout = 'default'
    
    def _initialize_widgets(self):
        """Initialize all available widgets"""
        return {
            'welcome_widget': {
                'id': 'welcome_widget',
                'name': 'Welcome Widget',
                'description': 'Display welcome message and quick stats',
                'category': 'overview',
                'enabled': True,
                'configurable': True,
                'config': {
                    'show_stats': True,
                    'show_greeting': True,
                    'animation': 'fade'
                }
            },
            'quick_actions': {
                'id': 'quick_actions',
                'name': 'Quick Actions',
                'description': 'Quick action buttons for common tasks',
                'category': 'navigation',
                'enabled': True,
                'configurable': True,
                'config': {
                    'actions': ['new_case', 'new_client', 'search'],
                    'layout': 'grid'
                }
            },
            'recent_cases': {
                'id': 'recent_cases',
                'name': 'Recent Cases',
                'description': 'Display recently updated cases',
                'category': 'data',
                'enabled': True,
                'configurable': True,
                'config': {
                    'limit': 5,
                    'show_status': True,
                    'show_priority': True
                }
            },
            'pending_tasks': {
                'id': 'pending_tasks',
                'name': 'Pending Tasks',
                'description': 'Show pending tasks and assignments',
                'category': 'tasks',
                'enabled': True,
                'configurable': True,
                'config': {
                    'limit': 10,
                    'group_by': 'priority',
                    'show_assignee': True
                }
            },
            'notifications': {
                'id': 'notifications',
                'name': 'Notifications',
                'description': 'Display system notifications and alerts',
                'category': 'communication',
                'enabled': True,
                'configurable': True,
                'config': {
                    'limit': 5,
                    'auto_dismiss': False,
                    'sound': True
                }
            },
            'calendar': {
                'id': 'calendar',
                'name': 'Calendar',
                'description': 'Show upcoming appointments and events',
                'category': 'scheduling',
                'enabled': True,
                'configurable': True,
                'config': {
                    'view': 'month',
                    'show_events': True,
                    'color_coding': True
                }
            },
            'statistics': {
                'id': 'statistics',
                'name': 'Statistics',
                'description': 'Display key performance statistics',
                'category': 'analytics',
                'enabled': True,
                'configurable': True,
                'config': {
                    'charts': ['pie', 'bar', 'line'],
                    'period': 'month',
                    'metrics': ['clients', 'cases', 'referrals']
                }
            },
            'resource_links': {
                'id': 'resource_links',
                'name': 'Resource Links',
                'description': 'Quick links to important resources',
                'category': 'navigation',
                'enabled': True,
                'configurable': True,
                'config': {
                    'links': ['housing', 'employment', 'healthcare'],
                    'show_icons': True
                }
            },
            'announcements': {
                'id': 'announcements',
                'name': 'Announcements',
                'description': 'System announcements and updates',
                'category': 'communication',
                'enabled': True,
                'configurable': True,
                'config': {
                    'limit': 3,
                    'show_date': True,
                    'dismissable': True
                }
            },
            'help_tips': {
                'id': 'help_tips',
                'name': 'Help Tips',
                'description': 'Helpful tips and guidance',
                'category': 'support',
                'enabled': True,
                'configurable': True,
                'config': {
                    'rotate': True,
                    'frequency': 'daily'
                }
            }
        }
    
    def _initialize_layouts(self):
        """Initialize available dashboard layouts"""
        return {
            'default': {
                'id': 'default',
                'name': 'Default Layout',
                'description': 'Standard two-column layout',
                'columns': 2,
                'widgets': [
                    {'widget_id': 'welcome_widget', 'position': 'top', 'width': 'full'},
                    {'widget_id': 'quick_actions', 'position': 'left', 'width': 'half'},
                    {'widget_id': 'recent_cases', 'position': 'right', 'width': 'half'},
                    {'widget_id': 'pending_tasks', 'position': 'left', 'width': 'half'},
                    {'widget_id': 'notifications', 'position': 'right', 'width': 'half'}
                ]
            },
            'compact': {
                'id': 'compact',
                'name': 'Compact Layout',
                'description': 'Minimalist single-column layout',
                'columns': 1,
                'widgets': [
                    {'widget_id': 'quick_actions', 'position': 'top', 'width': 'full'},
                    {'widget_id': 'pending_tasks', 'position': 'middle', 'width': 'full'},
                    {'widget_id': 'notifications', 'position': 'bottom', 'width': 'full'}
                ]
            },
            'expanded': {
                'id': 'expanded',
                'name': 'Expanded Layout',
                'description': 'Full-width layout with all widgets',
                'columns': 1,
                'widgets': [
                    {'widget_id': 'welcome_widget', 'position': 'top', 'width': 'full'},
                    {'widget_id': 'statistics', 'position': 'row2', 'width': 'full'},
                    {'widget_id': 'recent_cases', 'position': 'row3', 'width': 'full'},
                    {'widget_id': 'pending_tasks', 'position': 'row4', 'width': 'full'}
                ]
            },
            'grid-3col': {
                'id': 'grid-3col',
                'name': '3-Column Grid',
                'description': 'Three-column grid layout',
                'columns': 3,
                'widgets': [
                    {'widget_id': 'quick_actions', 'position': 'col1', 'width': 'third'},
                    {'widget_id': 'recent_cases', 'position': 'col2', 'width': 'third'},
                    {'widget_id': 'notifications', 'position': 'col3', 'width': 'third'},
                    {'widget_id': 'pending_tasks', 'position': 'col1', 'width': 'third'},
                    {'widget_id': 'calendar', 'position': 'col2', 'width': 'third'},
                    {'widget_id': 'statistics', 'position': 'col3', 'width': 'third'}
                ]
            },
            'grid-4col': {
                'id': 'grid-4col',
                'name': '4-Column Grid',
                'description': 'Four-column grid layout',
                'columns': 4,
                'widgets': [
                    {'widget_id': 'welcome_widget', 'position': 'header', 'width': 'full'},
                    {'widget_id': 'quick_actions', 'position': 'col1', 'width': 'quarter'},
                    {'widget_id': 'recent_cases', 'position': 'col2', 'width': 'quarter'},
                    {'widget_id': 'pending_tasks', 'position': 'col3', 'width': 'quarter'},
                    {'widget_id': 'notifications', 'position': 'col4', 'width': 'quarter'}
                ]
            },
            'sidebar-left': {
                'id': 'sidebar-left',
                'name': 'Left Sidebar',
                'description': 'Layout with left sidebar',
                'columns': 2,
                'widgets': [
                    {'widget_id': 'quick_actions', 'position': 'sidebar', 'width': 'quarter'},
                    {'widget_id': 'notifications', 'position': 'sidebar', 'width': 'quarter'},
                    {'widget_id': 'welcome_widget', 'position': 'main', 'width': 'three-quarters'},
                    {'widget_id': 'recent_cases', 'position': 'main', 'width': 'three-quarters'},
                    {'widget_id': 'pending_tasks', 'position': 'main', 'width': 'three-quarters'}
                ]
            },
            'sidebar-right': {
                'id': 'sidebar-right',
                'name': 'Right Sidebar',
                'description': 'Layout with right sidebar',
                'columns': 2,
                'widgets': [
                    {'widget_id': 'welcome_widget', 'position': 'main', 'width': 'three-quarters'},
                    {'widget_id': 'recent_cases', 'position': 'main', 'width': 'three-quarters'},
                    {'widget_id': 'quick_actions', 'position': 'sidebar', 'width': 'quarter'},
                    {'widget_id': 'calendar', 'position': 'sidebar', 'width': 'quarter'}
                ]
            },
            'split-screen': {
                'id': 'split-screen',
                'name': 'Split Screen',
                'description': 'Equal split screen layout',
                'columns': 2,
                'widgets': [
                    {'widget_id': 'recent_cases', 'position': 'left', 'width': 'half'},
                    {'widget_id': 'pending_tasks', 'position': 'right', 'width': 'half'}
                ]
            },
            'tabbed': {
                'id': 'tabbed',
                'name': 'Tabbed Layout',
                'description': 'Tabbed interface layout',
                'columns': 1,
                'widgets': [
                    {'widget_id': 'quick_actions', 'position': 'tab1', 'width': 'full', 'tab': 'Overview'},
                    {'widget_id': 'recent_cases', 'position': 'tab2', 'width': 'full', 'tab': 'Cases'},
                    {'widget_id': 'pending_tasks', 'position': 'tab3', 'width': 'full', 'tab': 'Tasks'},
                    {'widget_id': 'statistics', 'position': 'tab4', 'width': 'full', 'tab': 'Analytics'}
                ]
            },
            'accordion': {
                'id': 'accordion',
                'name': 'Accordion Layout',
                'description': 'Collapsible accordion sections',
                'columns': 1,
                'widgets': [
                    {'widget_id': 'quick_actions', 'position': 'section1', 'width': 'full', 'collapsible': True},
                    {'widget_id': 'recent_cases', 'position': 'section2', 'width': 'full', 'collapsible': True},
                    {'widget_id': 'pending_tasks', 'position': 'section3', 'width': 'full', 'collapsible': True},
                    {'widget_id': 'calendar', 'position': 'section4', 'width': 'full', 'collapsible': True}
                ]
            }
        }
    
    def get_all_widgets(self):
        """Get all widgets with their current states"""
        widgets = []
        for widget_id, widget in self.widgets.items():
            widget_data = widget.copy()
            # Override enabled state if explicitly set
            if widget_id in self.widget_states:
                widget_data['enabled'] = self.widget_states[widget_id]
            widgets.append(widget_data)
        return widgets
    
    def get_widget(self, widget_id):
        """Get specific widget"""
        return self.widgets.get(widget_id)
    
    def toggle_widget(self, widget_id, enabled):
        """Toggle widget on/off"""
        if widget_id not in self.widgets:
            return {'success': False, 'message': 'Widget not found'}
        
        self.widget_states[widget_id] = enabled
        return {'success': True, 'message': f'Widget {widget_id} {"enabled" if enabled else "disabled"}'}
    
    def configure_widget(self, widget_id, configuration):
        """Configure widget settings"""
        if widget_id not in self.widgets:
            return {'success': False, 'message': 'Widget not found'}
        
        if not self.widgets[widget_id]['configurable']:
            return {'success': False, 'message': 'Widget is not configurable'}
        
        # Update widget configuration
        self.widgets[widget_id]['config'].update(configuration)
        return {'success': True, 'message': 'Widget configured successfully'}
    
    def get_all_layouts(self):
        """Get all available layouts"""
        return list(self.layouts.values())
    
    def get_layout(self, layout_id):
        """Get specific layout"""
        return self.layouts.get(layout_id)
    
    def get_default_layout(self):
        """Get default layout"""
        return self.default_layout
    
    def set_default_layout(self, layout_id):
        """Set default layout"""
        if layout_id in self.layouts:
            self.default_layout = layout_id
            return True
        return False
    
    def customize_layout(self, layout_id, customization):
        """Customize layout"""
        if layout_id not in self.layouts:
            return {'success': False, 'message': 'Layout not found'}
        
        self.layout_customizations[layout_id] = customization
        return {'success': True, 'message': 'Layout customized successfully'}
    
    def get_enabled_widgets(self):
        """Get list of enabled widgets"""
        enabled = []
        for widget_id, widget in self.widgets.items():
            is_enabled = self.widget_states.get(widget_id, widget['enabled'])
            if is_enabled:
                enabled.append(widget_id)
        return enabled
