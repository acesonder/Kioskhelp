"""
Comprehensive test script for KioskHelp Web Portal
Tests all major features and links
"""

import sys
import os

# Add parent directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
grandparent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, grandparent_dir)

# Import KioskHelp system
from kioskhelp import KioskHelpSystem

# Import managers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.models.theme_manager import ThemeManager
from app.models.widget_manager import WidgetManager
from app.models.feature_manager import FeatureManager


def test_kioskhelp_system():
    """Test core KioskHelp system integration"""
    print("\n=== Testing KioskHelp System Integration ===")
    
    system = KioskHelpSystem()
    print("✓ KioskHelp system initialized")
    
    # Test session creation
    session = system.start_session(client_type='new')
    assert session['success'], "Failed to create session"
    print("✓ Session creation works")
    
    # Test registration
    client_data = {
        'anonymous': False,
        'name': 'Test Client',
        'email': 'test@example.com',
        'contact_preference': 'email',
        'consent_data_processing': True,
        'consent_service_referral': True
    }
    
    reg_result = system.complete_registration_workflow(session['session_id'], client_data)
    assert reg_result['success'], "Registration failed"
    print("✓ Client registration works")
    
    return True


def test_theme_manager():
    """Test theme management"""
    print("\n=== Testing Theme Manager ===")
    
    theme_manager = ThemeManager()
    
    # Test getting all themes
    themes = theme_manager.get_all_themes()
    assert len(themes) == 20, f"Expected 20 themes, got {len(themes)}"
    print(f"✓ All 20 themes available: {len(themes)}")
    
    # Test theme names
    theme_names = [t['name'] for t in themes]
    print(f"✓ Themes: {', '.join(theme_names[:5])}...")
    
    # Test setting default theme
    result = theme_manager.set_default_theme('modern-dark')
    assert result, "Failed to set default theme"
    print("✓ Theme switching works")
    
    # Test theme customization
    custom_result = theme_manager.customize_theme('modern-dark', {
        'primary_color': '#FF0000'
    })
    assert custom_result['success'], "Failed to customize theme"
    print("✓ Theme customization works")
    
    # Test CSS generation
    css = theme_manager.apply_theme('professional-blue')
    assert css is not None, "Failed to generate CSS"
    print("✓ Theme CSS generation works")
    
    return True


def test_widget_manager():
    """Test widget management"""
    print("\n=== Testing Widget Manager ===")
    
    widget_manager = WidgetManager()
    
    # Test getting all widgets
    widgets = widget_manager.get_all_widgets()
    assert len(widgets) == 10, f"Expected 10 widgets, got {len(widgets)}"
    print(f"✓ All 10 widgets available: {len(widgets)}")
    
    # Test widget names
    widget_names = [w['name'] for w in widgets]
    print(f"✓ Widgets: {', '.join(widget_names[:5])}...")
    
    # Test widget toggle
    result = widget_manager.toggle_widget('welcome_widget', False)
    assert result['success'], "Failed to toggle widget"
    print("✓ Widget toggle works")
    
    # Test widget configuration
    config_result = widget_manager.configure_widget('notifications', {
        'limit': 10,
        'sound': False
    })
    assert config_result['success'], "Failed to configure widget"
    print("✓ Widget configuration works")
    
    # Test getting all layouts
    layouts = widget_manager.get_all_layouts()
    assert len(layouts) == 10, f"Expected 10 layouts, got {len(layouts)}"
    print(f"✓ All 10 layouts available: {len(layouts)}")
    
    # Test layout names
    layout_names = [l['name'] for l in layouts]
    print(f"✓ Layouts: {', '.join(layout_names[:5])}...")
    
    return True


def test_feature_manager():
    """Test feature management"""
    print("\n=== Testing Feature Manager ===")
    
    feature_manager = FeatureManager()
    
    # Test getting all features
    features = feature_manager.get_all_features()
    assert len(features) >= 15, f"Expected at least 15 features, got {len(features)}"
    print(f"✓ All {len(features)} features available")
    
    # Test feature names
    feature_names = [f['name'] for f in features]
    print(f"✓ Features: {', '.join(feature_names[:5])}...")
    
    # Test feature toggle
    result = feature_manager.toggle_feature('notifications', False)
    assert result['success'], "Failed to toggle feature"
    print("✓ Feature toggle works")
    
    # Test checking feature status
    is_enabled = feature_manager.is_enabled('case_management')
    print(f"✓ Feature status check works (case_management: {is_enabled})")
    
    # Test getting enabled features
    enabled = feature_manager.get_enabled_features()
    print(f"✓ {len(enabled)} features currently enabled")
    
    return True


def test_questionnaire_workflow():
    """Test complete questionnaire workflow"""
    print("\n=== Testing Questionnaire Workflow ===")
    
    system = KioskHelpSystem()
    
    # Create session and register client
    session = system.start_session(client_type='new')
    client_data = {
        'anonymous': False,
        'name': 'Workflow Test Client',
        'email': 'workflow@test.com',
        'contact_preference': 'email',
        'consent_data_processing': True,
        'consent_service_referral': True
    }
    
    reg_result = system.complete_registration_workflow(session['session_id'], client_data)
    client_id = reg_result['client_id']
    intake_id = reg_result['intake_id']
    
    print("✓ Client registered for workflow test")
    
    # Submit intake responses
    intake_responses = {
        'housing_status': 'Homeless',
        'food_security': False,
        'healthcare_access': False,
        'mental_health_support': False,
        'employment_status': 'Unemployed',
        'legal_issues': True,
        'transportation': False,
        'immediate_needs': ['Shelter', 'Food', 'Employment']
    }
    
    intake_result = system.complete_intake_workflow(intake_id, intake_responses)
    assert intake_result['success'], "Intake workflow failed"
    print(f"✓ Intake completed, identified {len(intake_result['priority_needs'])} priority needs")
    
    # If assessment created, complete it
    if intake_result.get('assessment_id'):
        assessment_id = intake_result['assessment_id']
        
        # Submit assessment responses
        for need in intake_result['priority_needs']:
            if need == 'housing':
                system.assessment.submit_response(
                    assessment_id, 'current_situation', 'housing',
                    'Currently homeless, seeking emergency shelter'
                )
        
        # Generate comprehensive plan
        plan = system.generate_comprehensive_plan(client_id, assessment_id)
        assert plan['success'], "Plan generation failed"
        print(f"✓ Comprehensive plan generated with {plan.get('total_referrals', 0)} referrals")
        print(f"✓ Case created: {plan['case_id']}")
    
    return True


def test_file_structure():
    """Test that all required files exist"""
    print("\n=== Testing File Structure ===")
    
    # Get the thiswinter base directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(current_dir)  # Go up from tests/ to thiswinter/
    
    required_files = [
        'app.py',
        'config/settings.py',
        'app/routes/client_routes.py',
        'app/routes/admin_routes.py',
        'app/models/theme_manager.py',
        'app/models/widget_manager.py',
        'app/models/feature_manager.py',
        'templates/base.html',
        'templates/index.html',
        'templates/admin/dashboard.html',
        'templates/admin/login.html',
        'templates/client/questionnaire.html',
        'static/css/main.css',
        'static/js/main.js',
        'README.md',
        'requirements.txt'
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if not os.path.exists(full_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"✗ Missing files: {', '.join(missing_files)}")
        return False
    
    print(f"✓ All {len(required_files)} required files exist")
    
    # Test theme files
    themes_dir = os.path.join(base_dir, 'static/themes')
    theme_files = [f for f in os.listdir(themes_dir) if f.endswith('.css')]
    print(f"✓ {len(theme_files)} theme files found")
    
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("KIOSKHELP WEB PORTAL - COMPREHENSIVE TEST SUITE")
    print("="*60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("KioskHelp System", test_kioskhelp_system),
        ("Theme Manager", test_theme_manager),
        ("Widget Manager", test_widget_manager),
        ("Feature Manager", test_feature_manager),
        ("Questionnaire Workflow", test_questionnaire_workflow),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"\n{'✓' if result else '✗'} {test_name} - {'PASSED' if result else 'FAILED'}")
        except Exception as e:
            results.append((test_name, False))
            print(f"\n✗ {test_name} - FAILED: {str(e)}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status:12} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 All tests passed! The web portal is ready to use.")
        return True
    else:
        print("\n⚠ Some tests failed. Please review the errors above.")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
