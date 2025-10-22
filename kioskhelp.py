"""
KioskHelp - Main Application
Kiosk-based self-help system for vulnerable clients

This system provides:
- Client registration and consent management
- Comprehensive intake and assessment
- Intelligent referral system
- Communication and appointment scheduling
- Resource library access
- Smart case management
- Self-help tools for empowerment
"""

import datetime
from typing import Dict, List, Optional

from registration import ClientRegistration, ClientVerification
from consent import ConsentManager
from intake import IntakeAssessment
from assessment import ClientAssessment
from referral import ReferralSystem
from communication import CommunicationSystem, AppointmentScheduler
from resources import ResourceLibrary
from case_management import CaseManager
from self_help_tools import SelfHelpTools
import config


class KioskHelpSystem:
    """Main KioskHelp application"""
    
    def __init__(self):
        """Initialize all system modules"""
        self.registration = ClientRegistration()
        self.verification = ClientVerification()
        self.consent = ConsentManager()
        self.intake = IntakeAssessment()
        self.assessment = ClientAssessment()
        self.referral = ReferralSystem()
        self.communication = CommunicationSystem()
        self.scheduler = AppointmentScheduler()
        self.resources = ResourceLibrary()
        self.case_manager = CaseManager()
        self.self_help = SelfHelpTools()
        
        self.sessions = {}
        
    def start_session(self, client_type: str = 'new') -> Dict:
        """
        Start a new kiosk session
        
        Args:
            client_type: 'new' for new client, 'existing' for returning client
            
        Returns:
            Session information
        """
        session_id = f"session_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        session = {
            'session_id': session_id,
            'client_type': client_type,
            'start_time': datetime.datetime.now().isoformat(),
            'status': 'active',
            'steps_completed': []
        }
        
        self.sessions[session_id] = session
        
        return {
            'success': True,
            'session_id': session_id,
            'next_step': 'registration' if client_type == 'new' else 'verification',
            'message': f'Session started for {client_type} client'
        }
    
    def complete_registration_workflow(self, session_id: str, 
                                      client_data: Dict) -> Dict:
        """
        Complete full registration workflow for new client
        
        Args:
            session_id: Session identifier
            client_data: Client information
            
        Returns:
            Workflow completion result
        """
        # Step 1: Register client
        reg_result = self.registration.register_new_client(client_data)
        if not reg_result['success']:
            return reg_result
        
        client_id = reg_result['client_id']
        
        # Step 2: Record consents
        required_consents = [
            'data_processing',
            'data_sharing',
            'service_referral',
            'communication'
        ]
        
        for consent_type in required_consents:
            self.consent.record_consent(client_id, {
                'consent_type': consent_type,
                'granted': client_data.get(f'consent_{consent_type}', True)
            })
        
        # Step 3: Start intake assessment
        intake_result = self.intake.start_intake(client_id)
        
        # Update session
        if session_id in self.sessions:
            self.sessions[session_id]['client_id'] = client_id
            self.sessions[session_id]['steps_completed'].append('registration')
            self.sessions[session_id]['steps_completed'].append('consent')
        
        return {
            'success': True,
            'client_id': client_id,
            'intake_id': intake_result['intake_id'],
            'next_step': 'intake_assessment',
            'message': 'Registration completed successfully'
        }
    
    def complete_intake_workflow(self, intake_id: str, 
                                responses: Dict) -> Dict:
        """
        Complete intake assessment workflow
        
        Args:
            intake_id: Intake session identifier
            responses: Dictionary of question responses
            
        Returns:
            Intake workflow result
        """
        # Record all responses
        for question_id, response in responses.items():
            self.intake.record_response(intake_id, question_id, response)
        
        # Complete intake and get priority needs
        intake_result = self.intake.complete_intake(intake_id)
        
        if not intake_result['success']:
            return intake_result
        
        priority_needs = intake_result['priority_needs']
        
        # Get intake summary to extract client_id
        intake_summary = self.intake.get_intake_summary(intake_id)
        client_id = intake_summary['client_id']
        
        # Create assessment for identified needs
        if priority_needs:
            assessment_result = self.assessment.create_assessment(
                client_id, priority_needs
            )
            
            return {
                'success': True,
                'priority_needs': priority_needs,
                'assessment_id': assessment_result['assessment_id'],
                'next_step': 'detailed_assessment',
                'message': f'Intake completed. {len(priority_needs)} priority needs identified.'
            }
        
        return {
            'success': True,
            'priority_needs': [],
            'next_step': 'resources',
            'message': 'Intake completed successfully'
        }
    
    def generate_comprehensive_plan(self, client_id: str, 
                                   assessment_id: str) -> Dict:
        """
        Generate comprehensive support plan based on assessment
        
        Args:
            client_id: Unique client identifier
            assessment_id: Assessment identifier
            
        Returns:
            Comprehensive plan with referrals, resources, and case
        """
        # Complete assessment
        assessment_result = self.assessment.complete_assessment(assessment_id)
        
        if not assessment_result['success']:
            return assessment_result
        
        insights = assessment_result['insights']
        recommended_services = insights.get('services', [])
        priority_needs_raw = insights.get('needs_identified', [])
        
        # Normalize needs to match referral categories
        # Remove '_support' suffix if present
        priority_needs = [
            need.replace('_support', '') for need in priority_needs_raw
        ]
        
        # Create case
        case_result = self.case_manager.create_case(
            client_id=client_id,
            needs=priority_needs,
            priority=insights.get('priority', 'medium'),
            description='Client case created from assessment'
        )
        
        case_id = case_result['case_id']
        
        # Generate referrals
        referral_result = self.referral.create_multiple_referrals(
            client_id=client_id,
            needs=priority_needs,
            priority=insights.get('priority', 'medium')
        )
        
        # Get recommended resources
        resources = self.resources.get_recommended_resources(priority_needs)
        
        # Send welcome message
        self.communication.send_message(
            client_id=client_id,
            message_type='welcome',
            content='Welcome to KioskHelp! Your personalized support plan has been created.'
        )
        
        # Create notification about plan
        self.communication.create_notification(
            client_id=client_id,
            notification_type='plan_created',
            title='Your Support Plan is Ready',
            content=f'We have created a comprehensive plan to address your needs.',
            priority='high'
        )
        
        return {
            'success': True,
            'case_id': case_id,
            'referrals': referral_result.get('referrals', []),
            'total_referrals': referral_result.get('total_referrals', 0),
            'resources': resources,
            'priority_needs': priority_needs,
            'next_steps': self._generate_next_steps(priority_needs, recommended_services),
            'message': 'Comprehensive support plan created successfully'
        }
    
    def _generate_next_steps(self, needs: List[str], 
                           services: List[str]) -> List[str]:
        """Generate actionable next steps"""
        steps = []
        
        if 'housing' in needs:
            steps.append('Contact housing services for emergency or transitional housing')
        
        if 'food_security' in needs:
            steps.append('Visit community food bank for immediate food assistance')
        
        if 'mental_health' in needs or 'mental_health_crisis' in services:
            steps.append('Reach out to mental health support services')
        
        if 'healthcare' in needs:
            steps.append('Schedule appointment with community health clinic')
        
        if 'employment' in needs:
            steps.append('Visit workforce development center for job search support')
        
        if not steps:
            steps.append('Review recommended resources in the system')
            steps.append('Complete self-help tools to track your progress')
        
        return steps
    
    def get_client_dashboard(self, client_id: str) -> Dict:
        """
        Get comprehensive client dashboard
        
        Args:
            client_id: Unique client identifier
            
        Returns:
            Dashboard with all client information
        """
        dashboard = {
            'client_id': client_id,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Get active cases
        cases = self.case_manager.get_client_cases(client_id, active_only=True)
        dashboard['active_cases'] = len(cases)
        
        # Get referrals
        referrals = self.referral.get_client_referrals(client_id)
        dashboard['referrals'] = len(referrals)
        dashboard['pending_referrals'] = sum(
            1 for r in referrals if r['status'] == 'pending'
        )
        
        # Get appointments
        appointments = self.scheduler.get_client_appointments(
            client_id, upcoming_only=True
        )
        dashboard['upcoming_appointments'] = len(appointments)
        
        # Get notifications
        notifications = self.communication.get_notifications(client_id)
        dashboard['unread_notifications'] = sum(
            1 for n in notifications if not n['read']
        )
        
        # Get messages
        messages = self.communication.get_client_messages(
            client_id, unread_only=True
        )
        dashboard['unread_messages'] = len(messages)
        
        # Get available resources
        available_tools = self.self_help.get_available_tools()
        dashboard['available_tools'] = len(available_tools)
        
        return dashboard
    
    def end_session(self, session_id: str) -> Dict:
        """
        End kiosk session
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary
        """
        if session_id not in self.sessions:
            return {
                'success': False,
                'message': 'Session not found'
            }
        
        session = self.sessions[session_id]
        session['status'] = 'completed'
        session['end_time'] = datetime.datetime.now().isoformat()
        
        # Calculate session duration
        start = datetime.datetime.fromisoformat(session['start_time'])
        end = datetime.datetime.fromisoformat(session['end_time'])
        duration = (end - start).total_seconds() / 60  # in minutes
        
        return {
            'success': True,
            'session_id': session_id,
            'duration_minutes': duration,
            'steps_completed': session['steps_completed'],
            'message': 'Session completed successfully'
        }


def main():
    """Main application entry point"""
    print(f"=== {config.APP_NAME} v{config.APP_VERSION} ===")
    print(config.APP_DESCRIPTION)
    print("\nInitializing system modules...")
    
    # Initialize system
    system = KioskHelpSystem()
    
    print("\n✓ All modules initialized successfully")
    print("\nAvailable Modules:")
    print("  • Client Registration and Verification")
    print("  • Consent Management")
    print("  • Intake Assessment")
    print("  • Detailed Client Assessment")
    print("  • Service Referral System")
    print("  • Communication and Appointments")
    print("  • Resource Library")
    print("  • Smart Case Management")
    print("  • Self-Help Tools")
    
    print("\n=== System Ready ===")
    print("\nFor demonstration, run example_usage.py")
    
    return system


if __name__ == '__main__':
    main()
