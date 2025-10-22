# Quick Start Guide - KioskHelp System

## Getting Started in 5 Minutes

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/acesonder/Kioskhelp.git
cd Kioskhelp

# No dependencies required - uses Python standard library!
# Optional: Install dependencies for production features
# pip install -r requirements.txt
```

### 2. Run the Demonstration

See the complete system in action:

```bash
python example_usage.py
```

This will demonstrate:
- New client registration
- Intake and assessment process
- Automatic referral generation
- Case management
- Resource access
- Self-help tools

### 3. Basic Usage

#### Initialize the System

```python
from kioskhelp import KioskHelpSystem

# Create system instance
system = KioskHelpSystem()
```

#### Register a New Client

```python
# Start a session
session = system.start_session(client_type='new')

# Register client
client_data = {
    'name': 'Jane Doe',
    'anonymous': False,
    'contact_preference': 'email',
    'consent_data_processing': True,
    'consent_service_referral': True
}

result = system.complete_registration_workflow(
    session['session_id'], 
    client_data
)

client_id = result['client_id']
```

#### Complete Intake Assessment

```python
intake_id = result['intake_id']

# Provide intake responses
responses = {
    'housing_status': 'At risk of homelessness',
    'food_security': True,
    'healthcare_access': False,
    'employment_status': 'Unemployed',
    'immediate_needs': ['Healthcare', 'Employment']
}

intake_result = system.complete_intake_workflow(intake_id, responses)
```

#### Generate Support Plan

```python
assessment_id = intake_result['assessment_id']

# Submit detailed assessment responses
system.assessment.submit_response(
    assessment_id, 'insurance', 'healthcare', False
)
system.assessment.submit_response(
    assessment_id, 'job_search', 'employment', True
)

# Generate comprehensive plan
plan = system.generate_comprehensive_plan(client_id, assessment_id)

print(f"Case ID: {plan['case_id']}")
print(f"Referrals created: {plan['total_referrals']}")
print(f"Resources available: {len(plan['resources'])}")
```

#### Access Self-Help Tools

```python
# Budget planning
budget = system.self_help.use_budgeting_tool(
    client_id=client_id,
    income=2500,
    expenses={
        'housing': 900,
        'food': 500,
        'transportation': 200
    }
)

# Wellness tracking
wellness = system.self_help.use_wellness_tracker(
    client_id=client_id,
    mood=7,
    sleep_hours=7.5,
    notes='Feeling hopeful'
)

# Goal planning
goal = system.self_help.use_goal_planner(
    client_id=client_id,
    goal='Find stable employment',
    steps=[
        'Update resume',
        'Apply to 5 jobs weekly',
        'Network with professionals'
    ],
    target_date='2024-03-01'
)
```

#### View Client Dashboard

```python
dashboard = system.get_client_dashboard(client_id)

print(f"Active Cases: {dashboard['active_cases']}")
print(f"Pending Referrals: {dashboard['pending_referrals']}")
print(f"Upcoming Appointments: {dashboard['upcoming_appointments']}")
print(f"Unread Messages: {dashboard['unread_messages']}")
```

## Common Use Cases

### Use Case 1: Anonymous Client Seeking Help

```python
# Anonymous registration
client_data = {
    'anonymous': True,  # No personal information required
    'consent_data_processing': True
}

result = system.complete_registration_workflow(session_id, client_data)
```

### Use Case 2: Client with Immediate Crisis

```python
# Create crisis plan immediately
crisis_plan = system.self_help.create_crisis_plan(
    client_id=client_id,
    warning_signs=['Feeling hopeless', 'Thoughts of self-harm'],
    coping_strategies=['Call crisis line', 'Reach out to friend'],
    support_contacts=[
        {'name': 'Crisis Hotline', 'phone': '988'},
        {'name': 'Trusted Friend', 'phone': '555-0001'}
    ]
)

# Access saved crisis plan anytime
saved_plan = system.self_help.get_saved_tool_data(client_id, 'crisis_plan')
```

### Use Case 3: Track Client Progress

```python
# Get active cases
cases = system.case_manager.get_client_cases(client_id, active_only=True)
case_id = cases[0]['case_id']

# Set goals
system.case_manager.set_case_goals(case_id, [
    {'description': 'Secure housing', 'target_date': '2024-02-01'},
    {'description': 'Start job training', 'target_date': '2024-02-15'}
])

# Track progress
system.case_manager.track_progress(case_id, 'housing_viewings', 3)
system.case_manager.update_goal_status(case_id, 'goal_1', 'in_progress')

# Get insights
insights = system.case_manager.generate_case_insights(case_id)
```

### Use Case 4: Search and Access Resources

```python
# Search by category
housing_resources = system.resources.search_resources(category='housing')

# Search by keyword
job_resources = system.resources.search_resources(keyword='employment')

# Get specific resource
resource = system.resources.get_resource(housing_resources[0]['resource_id'])

# Log access
system.resources.log_resource_access(client_id, resource['resource_id'])

# Get client's resource history
history = system.resources.get_client_history(client_id)
```

## Configuration

Edit `config.py` to customize:

```python
# Session timeout (seconds)
SESSION_TIMEOUT = 300

# Enable/disable modules
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

# UI settings
UI = {
    'language': 'en',
    'accessibility': True,
    'large_text_mode': True,
    'high_contrast_mode': True
}
```

## Support for Service Providers

### Add New Service Provider

```python
from referral import ServiceProvider

# Create new provider
new_provider = ServiceProvider(
    provider_id='custom_001',
    name='Community Legal Services',
    services=['legal_consultation', 'document_assistance'],
    contact={'phone': '555-9999', 'email': 'help@legal.org'}
)

# Add to system
system.referral.providers[new_provider.provider_id] = new_provider
```

### Process Referrals

```python
# Get all client referrals
referrals = system.referral.get_client_referrals(client_id)

# Update referral status
for ref in referrals:
    if ref['status'] == 'pending':
        system.referral.update_referral_status(
            ref['referral_id'],
            'contacted',
            'Client contacted and appointment scheduled'
        )
```

## Tips for Success

1. **Privacy First**: Always offer anonymous registration option
2. **Clear Communication**: Use simple language in all interactions
3. **Regular Updates**: Keep clients informed of their progress
4. **Resource Access**: Make resources easily searchable and accessible
5. **Progress Tracking**: Use case management to monitor outcomes
6. **Empowerment**: Encourage use of self-help tools for independence

## Troubleshooting

### Issue: No referrals generated
**Solution**: Ensure needs are properly identified in intake/assessment

### Issue: Resources not appearing
**Solution**: Check that resource categories match client needs

### Issue: Session timeout
**Solution**: Adjust `SESSION_TIMEOUT` in config.py

## Next Steps

1. Review the full documentation in README.md
2. Run `python example_usage.py` to see all features
3. Customize service providers for your community
4. Add community-specific resources
5. Configure UI for your target population

## Getting Help

- Check README.md for detailed documentation
- Review example_usage.py for code examples
- Each module has inline documentation

## Contributing

We welcome contributions! Focus areas:
- Additional self-help tools
- More resource types
- Integration with external systems
- Accessibility improvements
- Translation support

---

**Remember**: This system is designed to serve vulnerable populations with compassion and respect. Every feature should empower clients and support their journey toward positive change.
