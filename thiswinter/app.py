"""
KioskHelp Web Portal - Main Application
A comprehensive web-based portal for KioskHelp system with advanced admin features
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import sys
import os

# Add parent directory to path to import KioskHelp modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kioskhelp import KioskHelpSystem
from app.routes import client_routes, admin_routes
from app.models.theme_manager import ThemeManager
from app.models.widget_manager import WidgetManager
from app.models.feature_manager import FeatureManager
import config.settings as settings

app = Flask(__name__)
app.secret_key = settings.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Initialize KioskHelp system
kioskhelp_system = KioskHelpSystem()

# Initialize managers
theme_manager = ThemeManager()
widget_manager = WidgetManager()
feature_manager = FeatureManager()

# Register blueprints
app.register_blueprint(client_routes.bp)
app.register_blueprint(admin_routes.bp)


@app.route('/')
def index():
    """Home page"""
    theme = session.get('theme', 'default')
    return render_template('index.html', 
                         theme=theme,
                         features=feature_manager.get_enabled_features())


@app.route('/api/themes')
def get_themes():
    """API endpoint to get available themes"""
    return jsonify(theme_manager.get_all_themes())


@app.route('/api/widgets')
def get_widgets():
    """API endpoint to get available widgets"""
    return jsonify(widget_manager.get_all_widgets())


@app.route('/api/features')
def get_features():
    """API endpoint to get feature flags"""
    return jsonify(feature_manager.get_all_features())


@app.context_processor
def inject_globals():
    """Inject global variables into all templates"""
    return {
        'app_name': settings.APP_NAME,
        'app_version': settings.APP_VERSION,
        'current_theme': session.get('theme', 'default'),
        'enabled_features': feature_manager.get_enabled_features()
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
