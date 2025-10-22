"""
Client-facing routes for web portal
Handles questionnaires, cases, and task viewing
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from kioskhelp import KioskHelpSystem
import datetime

bp = Blueprint('client', __name__, url_prefix='/client')

# Initialize KioskHelp system
system = KioskHelpSystem()


@bp.route('/dashboard')
def dashboard():
    """Client dashboard"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    client_id = session['client_id']
    dashboard_data = system.get_client_dashboard(client_id)
    
    return render_template('client/dashboard.html', 
                         dashboard=dashboard_data,
                         client_id=client_id)


@bp.route('/start')
def start():
    """Start new client session"""
    return render_template('client/start.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Client registration"""
    if request.method == 'POST':
        data = request.json
        
        # Start session
        session_result = system.start_session(client_type='new')
        
        # Register client
        client_data = {
            'anonymous': data.get('anonymous', False),
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'phone': data.get('phone', ''),
            'contact_preference': data.get('contact_preference', 'email'),
            'consent_data_processing': data.get('consent_data_processing', True),
            'consent_data_sharing': data.get('consent_data_sharing', True),
            'consent_service_referral': data.get('consent_service_referral', True),
            'consent_communication': data.get('consent_communication', True)
        }
        
        result = system.complete_registration_workflow(
            session_result['session_id'],
            client_data
        )
        
        if result['success']:
            session['client_id'] = result['client_id']
            session['intake_id'] = result['intake_id']
            session['session_id'] = session_result['session_id']
            
            return jsonify({
                'success': True,
                'client_id': result['client_id'],
                'intake_id': result['intake_id'],
                'redirect': url_for('client.questionnaire')
            })
        else:
            return jsonify(result), 400
    
    return render_template('client/register.html')


@bp.route('/questionnaire')
def questionnaire():
    """Extended questionnaire for comprehensive assessment"""
    if 'intake_id' not in session:
        return redirect(url_for('client.register'))
    
    return render_template('client/questionnaire.html')


@bp.route('/submit-questionnaire', methods=['POST'])
def submit_questionnaire():
    """Submit comprehensive questionnaire and create case with tasks"""
    if 'client_id' not in session or 'intake_id' not in session:
        return jsonify({'success': False, 'message': 'Session expired'}), 401
    
    data = request.json
    client_id = session['client_id']
    intake_id = session['intake_id']
    
    # Submit intake responses
    intake_responses = {
        'housing_status': data.get('housing_status'),
        'food_security': data.get('food_security') == 'yes',
        'healthcare_access': data.get('healthcare_access') == 'yes',
        'mental_health_support': data.get('mental_health_support') == 'yes',
        'employment_status': data.get('employment_status'),
        'legal_issues': data.get('legal_issues') == 'yes',
        'transportation': data.get('transportation') == 'yes',
        'immediate_needs': data.get('immediate_needs', [])
    }
    
    intake_result = system.complete_intake_workflow(intake_id, intake_responses)
    
    if not intake_result['success']:
        return jsonify(intake_result), 400
    
    # If there are priority needs, complete detailed assessment
    if intake_result.get('assessment_id'):
        assessment_id = intake_result['assessment_id']
        
        # Submit detailed responses
        for category in intake_result['priority_needs']:
            if category == 'housing':
                system.assessment.submit_response(
                    assessment_id, 'current_situation', 'housing',
                    data.get('housing_details', 'Not specified')
                )
                system.assessment.submit_response(
                    assessment_id, 'safety_concerns', 'housing',
                    data.get('housing_safety') == 'yes'
                )
            elif category == 'mental_health':
                system.assessment.submit_response(
                    assessment_id, 'current_support', 'mental_health',
                    data.get('mental_health_current') == 'yes'
                )
                system.assessment.submit_response(
                    assessment_id, 'crisis_support', 'mental_health',
                    data.get('mental_health_crisis') == 'yes'
                )
            elif category == 'employment':
                system.assessment.submit_response(
                    assessment_id, 'job_search', 'employment',
                    data.get('employment_search') == 'yes'
                )
                system.assessment.submit_response(
                    assessment_id, 'training_interest', 'employment',
                    data.get('employment_training') == 'yes'
                )
        
        # Generate comprehensive plan with tasks
        plan = system.generate_comprehensive_plan(client_id, assessment_id)
        
        # Create tasks for client and staff
        if plan['success']:
            case_id = plan['case_id']
            
            # Create client tasks
            client_tasks = _create_client_tasks(plan['priority_needs'])
            for task in client_tasks:
                system.case_manager.add_case_activity(
                    case_id,
                    'task_created',
                    f"Task for client: {task['title']}",
                    {'task': task, 'assignee': 'client'}
                )
            
            # Create staff tasks
            staff_tasks = _create_staff_tasks(plan['priority_needs'])
            for task in staff_tasks:
                system.case_manager.add_case_activity(
                    case_id,
                    'task_created',
                    f"Task for staff: {task['title']}",
                    {'task': task, 'assignee': 'staff'}
                )
            
            return jsonify({
                'success': True,
                'case_id': case_id,
                'client_tasks': client_tasks,
                'staff_tasks': staff_tasks,
                'referrals': plan.get('total_referrals', 0),
                'redirect': url_for('client.dashboard')
            })
    
    return jsonify({'success': True, 'redirect': url_for('client.dashboard')})


@bp.route('/cases')
def view_cases():
    """View client cases"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    client_id = session['client_id']
    cases = system.case_manager.get_client_cases(client_id)
    
    return render_template('client/cases.html', cases=cases)


@bp.route('/tasks')
def view_tasks():
    """View assigned tasks"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    client_id = session['client_id']
    cases = system.case_manager.get_client_cases(client_id)
    
    # Extract tasks from case activities
    all_tasks = []
    for case in cases:
        case_summary = system.case_manager.get_case_summary(case['case_id'])
        for activity in case_summary.get('activities', []):
            if activity['activity_type'] == 'task_created':
                task_data = activity.get('details', {}).get('task', {})
                if activity.get('details', {}).get('assignee') == 'client':
                    all_tasks.append({
                        'case_id': case['case_id'],
                        'task': task_data,
                        'created_at': activity['timestamp']
                    })
    
    return render_template('client/tasks.html', tasks=all_tasks)


@bp.route('/resources')
def resources():
    """View available resources"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    category = request.args.get('category', None)
    
    if category:
        resources_list = system.resources.search_resources(category=category)
    else:
        resources_list = system.resources.get_all_resources()
    
    return render_template('client/resources.html', resources=resources_list)


@bp.route('/appointments')
def appointments():
    """View appointments"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    client_id = session['client_id']
    appointments = system.scheduler.get_client_appointments(client_id)
    
    return render_template('client/appointments.html', appointments=appointments)


@bp.route('/messages')
def messages():
    """View messages"""
    if 'client_id' not in session:
        return redirect(url_for('client.start'))
    
    client_id = session['client_id']
    messages = system.communication.get_client_messages(client_id)
    
    return render_template('client/messages.html', messages=messages)


def _create_client_tasks(needs):
    """Create tasks for client based on needs"""
    tasks = []
    
    if 'housing' in needs:
        tasks.extend([
            {
                'title': 'Complete housing application',
                'description': 'Fill out and submit housing assistance application',
                'priority': 'high',
                'due_date': (datetime.datetime.now() + datetime.timedelta(days=7)).isoformat()
            },
            {
                'title': 'Gather required documents',
                'description': 'Collect ID, income verification, and other required documents',
                'priority': 'high',
                'due_date': (datetime.datetime.now() + datetime.timedelta(days=3)).isoformat()
            }
        ])
    
    if 'employment' in needs:
        tasks.extend([
            {
                'title': 'Update resume',
                'description': 'Update resume with recent experience and skills',
                'priority': 'medium',
                'due_date': (datetime.datetime.now() + datetime.timedelta(days=5)).isoformat()
            },
            {
                'title': 'Apply to jobs',
                'description': 'Submit applications to at least 5 job openings',
                'priority': 'medium',
                'due_date': (datetime.datetime.now() + datetime.timedelta(days=14)).isoformat()
            }
        ])
    
    if 'mental_health' in needs:
        tasks.append({
            'title': 'Schedule counseling appointment',
            'description': 'Contact mental health services to schedule first appointment',
            'priority': 'high',
            'due_date': (datetime.datetime.now() + datetime.timedelta(days=2)).isoformat()
        })
    
    if 'food_security' in needs:
        tasks.append({
            'title': 'Visit food bank',
            'description': 'Visit local food bank to access food assistance',
            'priority': 'high',
            'due_date': (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
        })
    
    return tasks


def _create_staff_tasks(needs):
    """Create tasks for staff/service providers based on needs"""
    tasks = []
    
    if 'housing' in needs:
        tasks.extend([
            {
                'title': 'Review housing options',
                'description': 'Identify available housing resources and eligibility',
                'priority': 'high',
                'assignee': 'housing_specialist'
            },
            {
                'title': 'Coordinate with housing providers',
                'description': 'Contact housing providers to check availability',
                'priority': 'high',
                'assignee': 'case_manager'
            }
        ])
    
    if 'employment' in needs:
        tasks.append({
            'title': 'Connect with job placement services',
            'description': 'Refer client to employment services and job training programs',
            'priority': 'medium',
            'assignee': 'employment_counselor'
        })
    
    if 'mental_health' in needs:
        tasks.append({
            'title': 'Arrange mental health assessment',
            'description': 'Schedule client for mental health assessment with licensed provider',
            'priority': 'high',
            'assignee': 'mental_health_coordinator'
        })
    
    if 'legal_support' in needs:
        tasks.append({
            'title': 'Legal aid consultation',
            'description': 'Connect client with legal aid services',
            'priority': 'medium',
            'assignee': 'legal_advocate'
        })
    
    return tasks
