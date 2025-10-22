"""
KioskHelp System - Example Usage
Demonstrates the complete workflow of the kiosk self-help system
"""

from kioskhelp import KioskHelpSystem


def demonstrate_new_client_workflow():
    """Demonstrate complete workflow for a new client"""
    print("\n" + "="*60)
    print("DEMONSTRATION: New Client Workflow")
    print("="*60)
    
    # Initialize system
    system = KioskHelpSystem()
    
    # Step 1: Start session
    print("\n1. Starting new client session...")
    session = system.start_session(client_type='new')
    print(f"   ✓ Session started: {session['session_id']}")
    
    # Step 2: Register client with consent
    print("\n2. Registering new client...")
    client_data = {
        'anonymous': False,
        'name': 'John Doe',
        'contact_preference': 'email',
        'consent_data_processing': True,
        'consent_data_sharing': True,
        'consent_service_referral': True,
        'consent_communication': True
    }
    
    reg_result = system.complete_registration_workflow(
        session['session_id'], client_data
    )
    print(f"   ✓ Client registered: {reg_result['client_id']}")
    print(f"   ✓ Intake started: {reg_result['intake_id']}")
    
    client_id = reg_result['client_id']
    intake_id = reg_result['intake_id']
    
    # Step 3: Complete intake assessment
    print("\n3. Completing intake assessment...")
    intake_responses = {
        'housing_status': 'Homeless',
        'food_security': False,
        'healthcare_access': False,
        'mental_health_support': False,
        'employment_status': 'Unemployed',
        'legal_issues': True,
        'transportation': False,
        'immediate_needs': ['Shelter', 'Food', 'Mental health services', 'Employment']
    }
    
    intake_result = system.complete_intake_workflow(intake_id, intake_responses)
    print(f"   ✓ Intake completed")
    print(f"   ✓ Priority needs identified: {', '.join(intake_result['priority_needs'])}")
    
    # Step 4: Complete detailed assessment
    print("\n4. Completing detailed assessment...")
    assessment_id = intake_result['assessment_id']
    
    # Submit assessment responses for critical needs
    system.assessment.submit_response(
        assessment_id, 'current_situation', 'housing',
        'Currently staying in emergency shelter'
    )
    system.assessment.submit_response(
        assessment_id, 'safety_concerns', 'housing', True
    )
    system.assessment.submit_response(
        assessment_id, 'crisis_support', 'mental_health', True
    )
    system.assessment.submit_response(
        assessment_id, 'current_support', 'mental_health', False
    )
    system.assessment.submit_response(
        assessment_id, 'job_search', 'employment', True
    )
    system.assessment.submit_response(
        assessment_id, 'training_interest', 'employment', True
    )
    
    print(f"   ✓ Assessment responses submitted")
    
    # Step 5: Generate comprehensive plan
    print("\n5. Generating comprehensive support plan...")
    plan = system.generate_comprehensive_plan(client_id, assessment_id)
    print(f"   ✓ Case created: {plan['case_id']}")
    print(f"   ✓ Referrals created: {plan.get('total_referrals', 0)}")
    print(f"   ✓ Resources available: {len(plan['resources'])}")
    
    # Display referrals
    if plan.get('referrals'):
        print("\n   Referrals:")
        for referral in plan['referrals']:
            if 'providers' in referral:
                for provider in referral['providers']:
                    print(f"     • {provider['name']}")
                    print(f"       Contact: {provider['contact']['phone']}")
    
    # Display resources
    if plan.get('resources'):
        print("\n   Recommended Resources:")
        for resource in plan['resources'][:5]:  # Show first 5
            print(f"     • {resource['title']} ({resource['category']})")
    
    # Display next steps
    print("\n   Next Steps:")
    for i, step in enumerate(plan['next_steps'], 1):
        print(f"     {i}. {step}")
    
    # Step 6: Use self-help tools
    print("\n6. Using self-help tools...")
    
    # Create crisis plan
    crisis_plan = system.self_help.create_crisis_plan(
        client_id=client_id,
        warning_signs=['Feeling hopeless', 'Isolating from others'],
        coping_strategies=['Call crisis line', 'Practice breathing exercises'],
        support_contacts=[
            {'name': 'Friend', 'phone': '555-0001'},
            {'name': 'Counselor', 'phone': '555-0002'}
        ]
    )
    print(f"   ✓ Crisis plan created")
    
    # Track wellness
    wellness = system.self_help.use_wellness_tracker(
        client_id=client_id,
        mood=5,
        sleep_hours=6.5,
        notes='Feeling hopeful about getting help'
    )
    print(f"   ✓ Wellness tracked")
    
    # Step 7: View dashboard
    print("\n7. Viewing client dashboard...")
    dashboard = system.get_client_dashboard(client_id)
    print(f"   Active Cases: {dashboard['active_cases']}")
    print(f"   Pending Referrals: {dashboard['pending_referrals']}")
    print(f"   Unread Messages: {dashboard['unread_messages']}")
    print(f"   Available Tools: {dashboard['available_tools']}")
    
    # Step 8: End session
    print("\n8. Ending session...")
    end_result = system.end_session(session['session_id'])
    print(f"   ✓ Session duration: {end_result['duration_minutes']:.2f} minutes")
    print(f"   ✓ Steps completed: {len(end_result['steps_completed'])}")
    
    print("\n" + "="*60)
    print("CLIENT WORKFLOW COMPLETED SUCCESSFULLY")
    print("="*60)
    
    return system, client_id


def demonstrate_case_management(system, client_id):
    """Demonstrate case management features"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Smart Case Management")
    print("="*60)
    
    # Get client cases
    cases = system.case_manager.get_client_cases(client_id)
    case_id = cases[0]['case_id']
    
    print(f"\n1. Working with case: {case_id}")
    
    # Set goals
    print("\n2. Setting case goals...")
    goals = [
        {
            'description': 'Secure stable housing within 30 days',
            'target_date': '2024-01-31'
        },
        {
            'description': 'Establish regular access to food resources',
            'target_date': '2024-01-15'
        },
        {
            'description': 'Begin mental health counseling',
            'target_date': '2024-01-10'
        }
    ]
    
    system.case_manager.set_case_goals(case_id, goals)
    print(f"   ✓ Set {len(goals)} goals")
    
    # Add case notes
    print("\n3. Adding case notes...")
    system.case_manager.add_case_note(
        case_id,
        "Client is motivated and engaged with services",
        author="case_worker"
    )
    print("   ✓ Note added")
    
    # Update goal status
    print("\n4. Updating goal progress...")
    case_summary = system.case_manager.get_case_summary(case_id)
    first_goal_id = case_summary['goals'][0]['goal_id']
    
    system.case_manager.update_goal_status(
        case_id, first_goal_id, 'in_progress'
    )
    print("   ✓ Goal status updated")
    
    # Track progress
    print("\n5. Tracking progress metrics...")
    system.case_manager.track_progress(
        case_id, 'housing_applications', 3
    )
    print("   ✓ Progress tracked")
    
    # Generate insights
    print("\n6. Generating case insights...")
    insights = system.case_manager.generate_case_insights(case_id)
    
    if insights.get('recommendations'):
        print("   Recommendations:")
        for rec in insights['recommendations']:
            print(f"     • {rec}")
    
    if insights.get('success_indicators'):
        print("   Success Indicators:")
        for indicator in insights['success_indicators']:
            print(f"     • {indicator}")
    
    # Get final summary
    print("\n7. Case Summary:")
    summary = system.case_manager.get_case_summary(case_id)
    print(f"   Status: {summary['status']}")
    print(f"   Priority: {summary['priority']}")
    print(f"   Goals: {len(summary['goals'])}")
    print(f"   Notes: {len(summary['notes'])}")
    print(f"   Progress: {summary['progress_percentage']:.0f}%")


def demonstrate_resources_and_tools(system, client_id):
    """Demonstrate resource library and self-help tools"""
    print("\n" + "="*60)
    print("DEMONSTRATION: Resources and Self-Help Tools")
    print("="*60)
    
    # Search resources
    print("\n1. Searching resources...")
    housing_resources = system.resources.search_resources(category='housing')
    print(f"   ✓ Found {len(housing_resources)} housing resources")
    
    employment_resources = system.resources.search_resources(keyword='job')
    print(f"   ✓ Found {len(employment_resources)} employment-related resources")
    
    # Access a resource
    print("\n2. Accessing a resource...")
    if housing_resources:
        resource = system.resources.get_resource(housing_resources[0]['resource_id'])
        system.resources.log_resource_access(client_id, resource['resource_id'])
        print(f"   ✓ Accessed: {resource['title']}")
    
    # Use budgeting tool
    print("\n3. Using budgeting tool...")
    budget = system.self_help.use_budgeting_tool(
        client_id=client_id,
        income=2000,
        expenses={
            'housing': 800,
            'food': 400,
            'transportation': 200,
            'utilities': 150,
            'other': 200
        }
    )
    
    print(f"   ✓ Budget analysis complete")
    print(f"   Total expenses: ${budget['analysis']['total_expenses']}")
    print(f"   Remaining: ${budget['analysis']['remaining']}")
    
    # Create goal plan
    print("\n4. Creating goal plan...")
    goal_plan = system.self_help.use_goal_planner(
        client_id=client_id,
        goal='Find full-time employment',
        steps=[
            'Update resume',
            'Apply to 5 jobs per week',
            'Practice interview skills',
            'Follow up on applications'
        ],
        target_date='2024-02-15'
    )
    print(f"   ✓ Goal plan created with {len(goal_plan['plan']['steps'])} steps")
    
    # Get all available tools
    print("\n5. Available Self-Help Tools:")
    tools = system.self_help.get_available_tools()
    for tool in tools:
        print(f"   • {tool['name']} ({tool['category']})")


def main():
    """Run all demonstrations"""
    print("\n" + "="*70)
    print(" "*15 + "KIOSKHELP SYSTEM DEMONSTRATION")
    print("="*70)
    
    # Demonstrate new client workflow
    system, client_id = demonstrate_new_client_workflow()
    
    # Demonstrate case management
    demonstrate_case_management(system, client_id)
    
    # Demonstrate resources and tools
    demonstrate_resources_and_tools(system, client_id)
    
    print("\n" + "="*70)
    print(" "*20 + "DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nThe KioskHelp system successfully demonstrated:")
    print("  ✓ Client registration and consent management")
    print("  ✓ Comprehensive intake and assessment")
    print("  ✓ Intelligent referral generation")
    print("  ✓ Smart case management with goals and tracking")
    print("  ✓ Resource library access")
    print("  ✓ Self-help tools for client empowerment")
    print("  ✓ Communication and notification system")
    print("\nThe system is ready to provide professional and compassionate")
    print("support to vulnerable clients in their journey toward positive change.")
    print("="*70 + "\n")


if __name__ == '__main__':
    main()
