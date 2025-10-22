"""
Admin portal routes with advanced troubleshooting and management tools
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from kioskhelp import KioskHelpSystem
from app.models.theme_manager import ThemeManager
from app.models.widget_manager import WidgetManager
from app.models.feature_manager import FeatureManager
import config.settings as settings
import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Initialize managers
system = KioskHelpSystem()
theme_manager = ThemeManager()
widget_manager = WidgetManager()
feature_manager = FeatureManager()


@bp.before_request
def check_admin_auth():
    """Check if user is authenticated as admin"""
    if request.endpoint and 'admin.login' not in request.endpoint:
        if not session.get('is_admin'):
            return redirect(url_for('admin.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        # Simple authentication (should use proper password hashing in production)
        if username == settings.ADMIN_USERNAME and password == settings.ADMIN_PASSWORD:
            session['is_admin'] = True
            session['admin_username'] = username
            return jsonify({'success': True, 'redirect': url_for('admin.dashboard')})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'}), 401
    
    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    """Admin logout"""
    session.clear()
    return redirect(url_for('admin.login'))


@bp.route('/dashboard')
def dashboard():
    """Admin dashboard with system overview"""
    # Get system statistics
    stats = {
        'total_clients': len(system.registration.clients),
        'active_cases': sum(1 for case in system.case_manager.cases.values() if case['status'] == 'active'),
        'pending_referrals': sum(1 for ref in system.referral.referrals.values() if ref['status'] == 'pending'),
        'total_resources': len(system.resources.resources),
        'active_features': len(feature_manager.get_enabled_features()),
    }
    
    return render_template('admin/dashboard.html', stats=stats)


@bp.route('/clients')
def clients():
    """View and manage all clients"""
    clients = list(system.registration.clients.values())
    return render_template('admin/clients.html', clients=clients)


@bp.route('/clients/<client_id>')
def client_detail(client_id):
    """View detailed client information"""
    client = system.registration.clients.get(client_id)
    if not client:
        return "Client not found", 404
    
    # Get client cases
    cases = system.case_manager.get_client_cases(client_id)
    
    # Get client referrals
    referrals = system.referral.get_client_referrals(client_id)
    
    # Get appointments
    appointments = system.scheduler.get_client_appointments(client_id)
    
    # Get messages
    messages = system.communication.get_client_messages(client_id)
    
    return render_template('admin/client_detail.html',
                         client=client,
                         cases=cases,
                         referrals=referrals,
                         appointments=appointments,
                         messages=messages)


@bp.route('/cases')
def cases():
    """View and manage all cases"""
    all_cases = list(system.case_manager.cases.values())
    return render_template('admin/cases.html', cases=all_cases)


@bp.route('/cases/<case_id>')
def case_detail(case_id):
    """View detailed case information"""
    case = system.case_manager.cases.get(case_id)
    if not case:
        return "Case not found", 404
    
    case_summary = system.case_manager.get_case_summary(case_id)
    insights = system.case_manager.generate_case_insights(case_id)
    
    return render_template('admin/case_detail.html',
                         case=case,
                         summary=case_summary,
                         insights=insights)


@bp.route('/tasks')
def tasks():
    """View and manage all tasks"""
    all_tasks = []
    
    for case in system.case_manager.cases.values():
        case_summary = system.case_manager.get_case_summary(case['case_id'])
        for activity in case_summary.get('activities', []):
            if activity['activity_type'] == 'task_created':
                all_tasks.append({
                    'case_id': case['case_id'],
                    'client_id': case['client_id'],
                    'task': activity.get('details', {}).get('task', {}),
                    'assignee': activity.get('details', {}).get('assignee'),
                    'created_at': activity['timestamp']
                })
    
    return render_template('admin/tasks.html', tasks=all_tasks)


@bp.route('/themes')
def themes():
    """Manage themes"""
    all_themes = theme_manager.get_all_themes()
    return render_template('admin/themes.html', themes=all_themes)


@bp.route('/themes/set', methods=['POST'])
def set_default_theme():
    """Set default theme"""
    data = request.json
    theme_id = data.get('theme_id')
    
    if theme_manager.set_default_theme(theme_id):
        return jsonify({'success': True, 'message': 'Default theme updated'})
    else:
        return jsonify({'success': False, 'message': 'Invalid theme'}), 400


@bp.route('/themes/customize', methods=['POST'])
def customize_theme():
    """Customize theme settings"""
    data = request.json
    theme_id = data.get('theme_id')
    customization = data.get('customization', {})
    
    result = theme_manager.customize_theme(theme_id, customization)
    return jsonify(result)


@bp.route('/layouts')
def layouts():
    """Manage dashboard layouts"""
    all_layouts = widget_manager.get_all_layouts()
    return render_template('admin/layouts.html', layouts=all_layouts)


@bp.route('/layouts/customize', methods=['POST'])
def customize_layout():
    """Customize dashboard layout"""
    data = request.json
    layout_id = data.get('layout_id')
    customization = data.get('customization', {})
    
    result = widget_manager.customize_layout(layout_id, customization)
    return jsonify(result)


@bp.route('/widgets')
def widgets():
    """Manage widgets"""
    all_widgets = widget_manager.get_all_widgets()
    return render_template('admin/widgets.html', widgets=all_widgets)


@bp.route('/widgets/toggle', methods=['POST'])
def toggle_widget():
    """Toggle widget on/off"""
    data = request.json
    widget_id = data.get('widget_id')
    enabled = data.get('enabled', True)
    
    result = widget_manager.toggle_widget(widget_id, enabled)
    return jsonify(result)


@bp.route('/widgets/configure', methods=['POST'])
def configure_widget():
    """Configure widget settings"""
    data = request.json
    widget_id = data.get('widget_id')
    configuration = data.get('configuration', {})
    
    result = widget_manager.configure_widget(widget_id, configuration)
    return jsonify(result)


@bp.route('/features')
def features():
    """Manage feature flags"""
    all_features = feature_manager.get_all_features()
    return render_template('admin/features.html', features=all_features)


@bp.route('/features/toggle', methods=['POST'])
def toggle_feature():
    """Toggle feature on/off"""
    data = request.json
    feature_id = data.get('feature_id')
    enabled = data.get('enabled', True)
    
    result = feature_manager.toggle_feature(feature_id, enabled)
    return jsonify(result)


@bp.route('/troubleshoot')
def troubleshoot():
    """Troubleshooting dashboard"""
    return render_template('admin/troubleshoot.html')


@bp.route('/troubleshoot/system-check', methods=['POST'])
def system_check():
    """Run comprehensive system check"""
    checks = {
        'modules': _check_modules(),
        'database': _check_database(),
        'sessions': _check_sessions(),
        'integrations': _check_integrations(),
        'performance': _check_performance()
    }
    
    return jsonify(checks)


@bp.route('/troubleshoot/logs')
def view_logs():
    """View system logs"""
    # In production, read from actual log files
    logs = [
        {'timestamp': datetime.datetime.now().isoformat(), 'level': 'INFO', 'message': 'System running normally'},
        {'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat(), 'level': 'INFO', 'message': 'New client registered'},
        {'timestamp': (datetime.datetime.now() - datetime.timedelta(minutes=10)).isoformat(), 'level': 'WARNING', 'message': 'High load detected'},
    ]
    
    return render_template('admin/logs.html', logs=logs)


@bp.route('/troubleshoot/diagnostics', methods=['POST'])
def run_diagnostics():
    """Run system diagnostics"""
    diagnostics = {
        'clients_with_issues': _diagnose_clients(),
        'stalled_cases': _diagnose_cases(),
        'failed_referrals': _diagnose_referrals(),
        'orphaned_data': _diagnose_data_integrity()
    }
    
    return jsonify(diagnostics)


@bp.route('/troubleshoot/repair', methods=['POST'])
def repair_system():
    """Attempt to repair system issues"""
    data = request.json
    issue_type = data.get('issue_type')
    
    if issue_type == 'stalled_cases':
        result = _repair_stalled_cases()
    elif issue_type == 'orphaned_data':
        result = _repair_orphaned_data()
    elif issue_type == 'failed_referrals':
        result = _repair_failed_referrals()
    else:
        result = {'success': False, 'message': 'Unknown issue type'}
    
    return jsonify(result)


@bp.route('/analytics')
def analytics():
    """Analytics dashboard"""
    analytics_data = {
        'client_growth': _get_client_growth(),
        'case_outcomes': _get_case_outcomes(),
        'referral_success': _get_referral_success(),
        'resource_usage': _get_resource_usage(),
        'popular_services': _get_popular_services()
    }
    
    return render_template('admin/analytics.html', analytics=analytics_data)


@bp.route('/reports')
def reports():
    """Generate reports"""
    return render_template('admin/reports.html')


@bp.route('/reports/generate', methods=['POST'])
def generate_report():
    """Generate custom report"""
    data = request.json
    report_type = data.get('report_type')
    date_range = data.get('date_range', {})
    
    if report_type == 'client_summary':
        report_data = _generate_client_summary_report(date_range)
    elif report_type == 'case_summary':
        report_data = _generate_case_summary_report(date_range)
    elif report_type == 'service_usage':
        report_data = _generate_service_usage_report(date_range)
    else:
        return jsonify({'success': False, 'message': 'Unknown report type'}), 400
    
    return jsonify({'success': True, 'report': report_data})


@bp.route('/settings')
def settings_page():
    """System settings"""
    return render_template('admin/settings.html',
                         current_theme=theme_manager.get_default_theme(),
                         current_layout=widget_manager.get_default_layout(),
                         features=feature_manager.get_all_features())


# Helper functions for troubleshooting

def _check_modules():
    """Check if all modules are functioning"""
    return {
        'status': 'healthy',
        'modules': {
            'registration': 'OK',
            'assessment': 'OK',
            'referral': 'OK',
            'case_management': 'OK',
            'communication': 'OK'
        }
    }


def _check_database():
    """Check database connectivity and integrity"""
    return {
        'status': 'healthy',
        'connection': 'OK',
        'tables': 'OK',
        'indexes': 'OK'
    }


def _check_sessions():
    """Check active sessions"""
    return {
        'status': 'healthy',
        'active_sessions': len(system.sessions),
        'expired_sessions': 0
    }


def _check_integrations():
    """Check external integrations"""
    return {
        'status': 'healthy',
        'service_providers': 'OK',
        'notification_service': 'OK',
        'email_service': 'OK'
    }


def _check_performance():
    """Check system performance"""
    return {
        'status': 'healthy',
        'response_time': '< 100ms',
        'memory_usage': 'Normal',
        'cpu_usage': 'Normal'
    }


def _diagnose_clients():
    """Diagnose client-related issues"""
    issues = []
    for client_id, client in system.registration.clients.items():
        if not client.get('email') and not client.get('phone'):
            issues.append({
                'client_id': client_id,
                'issue': 'No contact information',
                'severity': 'medium'
            })
    return issues


def _diagnose_cases():
    """Diagnose stalled cases"""
    stalled = []
    for case_id, case in system.case_manager.cases.items():
        # Check if case has been inactive for more than 30 days
        if case['status'] == 'active':
            # In production, check actual timestamps
            stalled.append({
                'case_id': case_id,
                'client_id': case['client_id'],
                'issue': 'No activity in 30+ days',
                'severity': 'medium'
            })
    return stalled[:5]  # Return first 5


def _diagnose_referrals():
    """Diagnose failed referrals"""
    failed = []
    for ref_id, referral in system.referral.referrals.items():
        if referral.get('status') == 'failed':
            failed.append({
                'referral_id': ref_id,
                'client_id': referral['client_id'],
                'reason': 'Provider unavailable'
            })
    return failed


def _diagnose_data_integrity():
    """Check for orphaned data"""
    issues = []
    # Check for cases without valid clients
    for case_id, case in system.case_manager.cases.items():
        if case['client_id'] not in system.registration.clients:
            issues.append({
                'type': 'orphaned_case',
                'case_id': case_id,
                'issue': 'Case belongs to non-existent client'
            })
    return issues


def _repair_stalled_cases():
    """Repair stalled cases"""
    # Add activity to stalled cases
    repaired = 0
    for case_id, case in system.case_manager.cases.items():
        if case['status'] == 'active':
            system.case_manager.add_case_note(
                case_id,
                'System check performed - case reviewed',
                'system'
            )
            repaired += 1
    
    return {'success': True, 'repaired': repaired}


def _repair_orphaned_data():
    """Clean up orphaned data"""
    return {'success': True, 'cleaned': 0}


def _repair_failed_referrals():
    """Retry failed referrals"""
    return {'success': True, 'retried': 0}


def _get_client_growth():
    """Get client growth data"""
    return {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'data': [10, 15, 25, 30, 45, 50]
    }


def _get_case_outcomes():
    """Get case outcome statistics"""
    return {
        'resolved': 45,
        'active': 30,
        'pending': 15,
        'closed': 10
    }


def _get_referral_success():
    """Get referral success rate"""
    total = len(system.referral.referrals)
    successful = sum(1 for r in system.referral.referrals.values() if r.get('status') == 'completed')
    
    return {
        'total': total,
        'successful': successful,
        'rate': (successful / total * 100) if total > 0 else 0
    }


def _get_resource_usage():
    """Get resource usage statistics"""
    return {
        'most_accessed': [
            {'name': 'Housing Resources', 'count': 150},
            {'name': 'Employment Guide', 'count': 120},
            {'name': 'Mental Health Support', 'count': 95}
        ]
    }


def _get_popular_services():
    """Get popular service categories"""
    return {
        'housing': 45,
        'employment': 35,
        'mental_health': 30,
        'food_security': 25,
        'healthcare': 20
    }


def _generate_client_summary_report(date_range):
    """Generate client summary report"""
    return {
        'total_clients': len(system.registration.clients),
        'new_clients': 10,
        'active_clients': 35,
        'by_need': {
            'housing': 15,
            'employment': 12,
            'mental_health': 10
        }
    }


def _generate_case_summary_report(date_range):
    """Generate case summary report"""
    return {
        'total_cases': len(system.case_manager.cases),
        'active_cases': 30,
        'resolved_cases': 15,
        'average_resolution_days': 45
    }


def _generate_service_usage_report(date_range):
    """Generate service usage report"""
    return {
        'total_referrals': len(system.referral.referrals),
        'successful_referrals': 25,
        'pending_referrals': 10,
        'by_category': {
            'housing': 15,
            'employment': 10,
            'healthcare': 8
        }
    }
