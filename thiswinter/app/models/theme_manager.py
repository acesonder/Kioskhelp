"""
Theme Manager - Handles 20+ different themes with customization
"""

import json
import os


class ThemeManager:
    """Manages themes and their customizations"""
    
    def __init__(self):
        self.themes = self._initialize_themes()
        self.default_theme = 'professional-blue'
        self.customizations = {}
    
    def _initialize_themes(self):
        """Initialize all 20 themes"""
        return {
            'professional-blue': {
                'id': 'professional-blue',
                'name': 'Professional Blue',
                'primary_color': '#2563eb',
                'secondary_color': '#1e40af',
                'background': '#f8fafc',
                'text': '#1e293b',
                'accent': '#3b82f6',
                'font_family': 'Inter, sans-serif',
                'border_radius': '8px',
                'category': 'professional'
            },
            'modern-dark': {
                'id': 'modern-dark',
                'name': 'Modern Dark',
                'primary_color': '#1f2937',
                'secondary_color': '#111827',
                'background': '#0f172a',
                'text': '#f1f5f9',
                'accent': '#6366f1',
                'font_family': 'Roboto, sans-serif',
                'border_radius': '12px',
                'category': 'dark'
            },
            'light-minimal': {
                'id': 'light-minimal',
                'name': 'Light Minimal',
                'primary_color': '#ffffff',
                'secondary_color': '#f9fafb',
                'background': '#ffffff',
                'text': '#374151',
                'accent': '#059669',
                'font_family': 'system-ui, sans-serif',
                'border_radius': '4px',
                'category': 'minimal'
            },
            'warm-orange': {
                'id': 'warm-orange',
                'name': 'Warm Orange',
                'primary_color': '#ea580c',
                'secondary_color': '#c2410c',
                'background': '#fff7ed',
                'text': '#431407',
                'accent': '#f97316',
                'font_family': 'Poppins, sans-serif',
                'border_radius': '10px',
                'category': 'warm'
            },
            'cool-green': {
                'id': 'cool-green',
                'name': 'Cool Green',
                'primary_color': '#059669',
                'secondary_color': '#047857',
                'background': '#f0fdfa',
                'text': '#064e3b',
                'accent': '#10b981',
                'font_family': 'Open Sans, sans-serif',
                'border_radius': '8px',
                'category': 'cool'
            },
            'corporate-grey': {
                'id': 'corporate-grey',
                'name': 'Corporate Grey',
                'primary_color': '#4b5563',
                'secondary_color': '#374151',
                'background': '#f9fafb',
                'text': '#1f2937',
                'accent': '#6b7280',
                'font_family': 'Arial, sans-serif',
                'border_radius': '6px',
                'category': 'corporate'
            },
            'vibrant-purple': {
                'id': 'vibrant-purple',
                'name': 'Vibrant Purple',
                'primary_color': '#7c3aed',
                'secondary_color': '#6d28d9',
                'background': '#faf5ff',
                'text': '#4c1d95',
                'accent': '#a78bfa',
                'font_family': 'Montserrat, sans-serif',
                'border_radius': '12px',
                'category': 'vibrant'
            },
            'ocean-blue': {
                'id': 'ocean-blue',
                'name': 'Ocean Blue',
                'primary_color': '#0891b2',
                'secondary_color': '#0e7490',
                'background': '#ecfeff',
                'text': '#164e63',
                'accent': '#06b6d4',
                'font_family': 'Lato, sans-serif',
                'border_radius': '8px',
                'category': 'cool'
            },
            'sunset-red': {
                'id': 'sunset-red',
                'name': 'Sunset Red',
                'primary_color': '#dc2626',
                'secondary_color': '#b91c1c',
                'background': '#fef2f2',
                'text': '#7f1d1d',
                'accent': '#ef4444',
                'font_family': 'Nunito, sans-serif',
                'border_radius': '10px',
                'category': 'warm'
            },
            'forest-green': {
                'id': 'forest-green',
                'name': 'Forest Green',
                'primary_color': '#15803d',
                'secondary_color': '#166534',
                'background': '#f7fee7',
                'text': '#14532d',
                'accent': '#22c55e',
                'font_family': 'Merriweather, serif',
                'border_radius': '8px',
                'category': 'natural'
            },
            'midnight-black': {
                'id': 'midnight-black',
                'name': 'Midnight Black',
                'primary_color': '#000000',
                'secondary_color': '#171717',
                'background': '#0a0a0a',
                'text': '#fafafa',
                'accent': '#525252',
                'font_family': 'SF Pro, sans-serif',
                'border_radius': '6px',
                'category': 'dark'
            },
            'pastel-pink': {
                'id': 'pastel-pink',
                'name': 'Pastel Pink',
                'primary_color': '#ec4899',
                'secondary_color': '#db2777',
                'background': '#fdf2f8',
                'text': '#831843',
                'accent': '#f472b6',
                'font_family': 'Quicksand, sans-serif',
                'border_radius': '16px',
                'category': 'pastel'
            },
            'earth-tone': {
                'id': 'earth-tone',
                'name': 'Earth Tone',
                'primary_color': '#92400e',
                'secondary_color': '#78350f',
                'background': '#fef3c7',
                'text': '#451a03',
                'accent': '#d97706',
                'font_family': 'Georgia, serif',
                'border_radius': '8px',
                'category': 'natural'
            },
            'high-contrast': {
                'id': 'high-contrast',
                'name': 'High Contrast',
                'primary_color': '#000000',
                'secondary_color': '#1a1a1a',
                'background': '#ffffff',
                'text': '#000000',
                'accent': '#0000ff',
                'font_family': 'Arial, sans-serif',
                'border_radius': '0px',
                'category': 'accessibility'
            },
            'accessibility-friendly': {
                'id': 'accessibility-friendly',
                'name': 'Accessibility Friendly',
                'primary_color': '#1e40af',
                'secondary_color': '#1e3a8a',
                'background': '#ffffff',
                'text': '#000000',
                'accent': '#2563eb',
                'font_family': 'Verdana, sans-serif',
                'border_radius': '4px',
                'category': 'accessibility'
            },
            'classic-white': {
                'id': 'classic-white',
                'name': 'Classic White',
                'primary_color': '#f8f9fa',
                'secondary_color': '#e9ecef',
                'background': '#ffffff',
                'text': '#212529',
                'accent': '#0d6efd',
                'font_family': 'Times New Roman, serif',
                'border_radius': '4px',
                'category': 'classic'
            },
            'gradient-blue': {
                'id': 'gradient-blue',
                'name': 'Gradient Blue',
                'primary_color': '#4f46e5',
                'secondary_color': '#7c3aed',
                'background': '#f5f3ff',
                'text': '#312e81',
                'accent': '#818cf8',
                'font_family': 'Inter, sans-serif',
                'border_radius': '16px',
                'category': 'gradient'
            },
            'material-design': {
                'id': 'material-design',
                'name': 'Material Design',
                'primary_color': '#1976d2',
                'secondary_color': '#1565c0',
                'background': '#fafafa',
                'text': '#212121',
                'accent': '#2196f3',
                'font_family': 'Roboto, sans-serif',
                'border_radius': '4px',
                'category': 'modern'
            },
            'bootstrap-inspired': {
                'id': 'bootstrap-inspired',
                'name': 'Bootstrap Inspired',
                'primary_color': '#0d6efd',
                'secondary_color': '#0b5ed7',
                'background': '#f8f9fa',
                'text': '#212529',
                'accent': '#0dcaf0',
                'font_family': 'system-ui, sans-serif',
                'border_radius': '6px',
                'category': 'modern'
            },
            'custom-branded': {
                'id': 'custom-branded',
                'name': 'Custom Branded',
                'primary_color': '#8b5cf6',
                'secondary_color': '#7c3aed',
                'background': '#faf5ff',
                'text': '#2e1065',
                'accent': '#a78bfa',
                'font_family': 'Custom, sans-serif',
                'border_radius': '12px',
                'category': 'custom'
            }
        }
    
    def get_all_themes(self):
        """Get all available themes"""
        return list(self.themes.values())
    
    def get_theme(self, theme_id):
        """Get specific theme"""
        return self.themes.get(theme_id)
    
    def get_default_theme(self):
        """Get default theme"""
        return self.default_theme
    
    def set_default_theme(self, theme_id):
        """Set default theme"""
        if theme_id in self.themes:
            self.default_theme = theme_id
            return True
        return False
    
    def customize_theme(self, theme_id, customization):
        """Customize a theme"""
        if theme_id not in self.themes:
            return {'success': False, 'message': 'Theme not found'}
        
        self.customizations[theme_id] = customization
        return {'success': True, 'message': 'Theme customized successfully'}
    
    def get_theme_customization(self, theme_id):
        """Get theme customization"""
        return self.customizations.get(theme_id, {})
    
    def apply_theme(self, theme_id):
        """Generate CSS for applying a theme"""
        theme = self.themes.get(theme_id)
        if not theme:
            return None
        
        customization = self.customizations.get(theme_id, {})
        
        # Merge theme with customization
        final_theme = {**theme, **customization}
        
        css = f"""
        :root {{
            --primary-color: {final_theme['primary_color']};
            --secondary-color: {final_theme['secondary_color']};
            --background-color: {final_theme['background']};
            --text-color: {final_theme['text']};
            --accent-color: {final_theme['accent']};
            --font-family: {final_theme['font_family']};
            --border-radius: {final_theme['border_radius']};
        }}
        
        body {{
            background-color: var(--background-color);
            color: var(--text-color);
            font-family: var(--font-family);
        }}
        
        .btn-primary {{
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }}
        
        .btn-secondary {{
            background-color: var(--secondary-color);
            border-color: var(--secondary-color);
        }}
        
        .card {{
            border-radius: var(--border-radius);
        }}
        
        a {{
            color: var(--accent-color);
        }}
        """
        
        return css
