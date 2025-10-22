# KioskHelp - Comprehensive Self-Help Kiosk System

A professional, compassionate kiosk-based self-help system designed to support vulnerable clients through registration, assessment, referral, and case management services.

## Overview

KioskHelp provides a comprehensive platform for vulnerable individuals to access services, resources, and support through an easy-to-use kiosk interface. The system is designed to be accessible, privacy-focused, and empowering for clients seeking help.

## Key Features

### 1. **Client Registration & Consent Management**
- Secure registration for new and existing clients
- Anonymous registration option for privacy
- Comprehensive consent management system
- GDPR-compliant data handling

### 2. **Intake & Assessment**
- Guided intake process to identify immediate needs
- Detailed assessments across multiple life domains:
  - Housing stability
  - Food security
  - Healthcare access
  - Mental health support
  - Employment status
  - Legal assistance needs
  - Transportation
  - Family services
- Intelligent need prioritization

### 3. **Intelligent Referral System**
- Automatic matching with appropriate service providers
- Comprehensive provider directory including:
  - Housing services
  - Food banks and meal programs
  - Healthcare clinics
  - Mental health support centers
  - Employment services
  - Legal aid
  - Family services
- Priority-based referral routing
- Referral tracking and status updates

### 4. **Communication & Appointments**
- Client messaging system
- Notification management
- Appointment scheduling with service providers
- Automated appointment reminders
- Multiple communication channels (email, SMS, app)

### 5. **Resource Library**
- Curated educational resources
- Guides, articles, videos, and forms
- Searchable by category or keyword
- Resource access tracking
- Personalized recommendations based on needs

### 6. **Smart Case Management**
- Automated case creation from assessments
- Goal setting and tracking
- Progress monitoring with metrics
- Case notes and activity logging
- Intelligent insights and recommendations
- Priority-based case routing

### 7. **Self-Help Tools**
- **Budget Planning Tool** - Create and manage personal budgets
- **Housing Search Checklist** - Track housing applications
- **Wellness Tracker** - Monitor daily mood and wellbeing
- **Goal Planner** - Set and track personal goals
- **Job Search Organizer** - Manage job applications
- **Crisis Plan Creator** - Develop personal crisis response plans
- **Resource Finder** - Locate community resources

## System Architecture

```
KioskHelp System
├── Registration Module
│   ├── New client registration
│   ├── Existing client verification
│   └── Anonymous registration support
├── Consent Management
│   ├── Consent recording
│   ├── Consent tracking
│   └── Revocation handling
├── Intake & Assessment
│   ├── Initial intake questions
│   ├── Detailed assessments
│   └── Need identification
├── Referral System
│   ├── Service provider directory
│   ├── Automatic matching
│   └── Referral tracking
├── Communication
│   ├── Messaging system
│   ├── Notifications
│   └── Appointment scheduling
├── Resource Library
│   ├── Resource catalog
│   ├── Search functionality
│   └── Access logging
├── Case Management
│   ├── Case creation
│   ├── Goal tracking
│   ├── Progress monitoring
│   └── Intelligent insights
└── Self-Help Tools
    ├── Budgeting
    ├── Wellness tracking
    ├── Goal planning
    └── Crisis planning
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/acesonder/Kioskhelp.git
cd Kioskhelp
```

2. Install Python dependencies (Python 3.7+ required):
```bash
pip install -r requirements.txt
```

3. Run the system:
```bash
python kioskhelp.py
```

## Usage

### Running the Example Demonstration

To see the complete system in action:

```bash
python example_usage.py
```

This will demonstrate:
- New client registration workflow
- Intake and assessment process
- Referral generation
- Case management
- Resource access
- Self-help tool usage

### Using the System Programmatically

```python
from kioskhelp import KioskHelpSystem

# Initialize the system
system = KioskHelpSystem()

# Start a new session
session = system.start_session(client_type='new')

# Register a client
client_data = {
    'anonymous': False,
    'name': 'Client Name',
    'contact_preference': 'email',
    'consent_data_processing': True,
    'consent_service_referral': True
}

result = system.complete_registration_workflow(
    session['session_id'], 
    client_data
)

# Continue with intake, assessment, and plan generation...
```

## Module Documentation

### Registration Module
Handles client registration and identity verification.

```python
from registration import ClientRegistration, ClientVerification

registration = ClientRegistration()
result = registration.register_new_client({
    'email': 'client@example.com',
    'name': 'John Doe',
    'anonymous': False
})
```

### Consent Management
Manages all aspects of client consent.

```python
from consent import ConsentManager

consent = ConsentManager()
consent.record_consent(client_id, {
    'consent_type': 'data_processing',
    'granted': True
})
```

### Intake & Assessment
Conducts client intake and detailed assessments.

```python
from intake import IntakeAssessment
from assessment import ClientAssessment

intake = IntakeAssessment()
intake_result = intake.start_intake(client_id)

# Record responses
intake.record_response(intake_id, 'housing_status', 'Homeless')
intake_summary = intake.complete_intake(intake_id)
```

### Referral System
Creates and manages service provider referrals.

```python
from referral import ReferralSystem

referral = ReferralSystem()
result = referral.create_referral(
    client_id=client_id,
    need_category='housing',
    priority='high'
)
```

### Communication
Handles messaging and appointments.

```python
from communication import CommunicationSystem, AppointmentScheduler

comm = CommunicationSystem()
comm.send_message(
    client_id=client_id,
    message_type='update',
    content='Your appointment is confirmed'
)

scheduler = AppointmentScheduler()
scheduler.schedule_appointment(
    client_id=client_id,
    provider_id='health_001',
    appointment_type='checkup',
    date_time='2024-01-15T10:00:00'
)
```

### Resource Library
Provides access to educational resources.

```python
from resources import ResourceLibrary

resources = ResourceLibrary()
housing_resources = resources.search_resources(category='housing')
resource = resources.get_resource(resource_id)
```

### Case Management
Smart case tracking and management.

```python
from case_management import CaseManager

case_mgr = CaseManager()
case = case_mgr.create_case(
    client_id=client_id,
    needs=['housing', 'employment'],
    priority='high'
)

# Set goals
case_mgr.set_case_goals(case_id, [
    {'description': 'Secure housing', 'target_date': '2024-02-01'},
    {'description': 'Find employment', 'target_date': '2024-03-01'}
])

# Track progress
case_mgr.track_progress(case_id, 'job_applications', 5)
```

### Self-Help Tools
Interactive tools for client empowerment.

```python
from self_help_tools import SelfHelpTools

tools = SelfHelpTools()

# Budget planning
budget = tools.use_budgeting_tool(
    client_id=client_id,
    income=2000,
    expenses={'housing': 800, 'food': 400}
)

# Wellness tracking
wellness = tools.use_wellness_tracker(
    client_id=client_id,
    mood=7,
    sleep_hours=8
)

# Goal planning
goal = tools.use_goal_planner(
    client_id=client_id,
    goal='Find new job',
    steps=['Update resume', 'Apply to jobs'],
    target_date='2024-02-15'
)
```

## Configuration

Edit `config.py` to customize system settings:

```python
# Application Settings
APP_NAME = "KioskHelp"
APP_VERSION = "1.0.0"

# Database Settings
DATABASE = {
    'type': 'sqlite',
    'name': 'kioskhelp.db',
    'path': 'data/'
}

# Session Settings
SESSION_TIMEOUT = 300  # 5 minutes

# Enable/disable modules
MODULES = {
    'registration': True,
    'consent': True,
    'intake': True,
    'assessment': True,
    # ... more modules
}
```

## Privacy & Security

- **Data Encryption**: All sensitive data is encrypted
- **Consent Required**: Explicit consent for all data processing
- **Anonymous Mode**: Support for anonymous client registration
- **GDPR Compliant**: Follows data protection regulations
- **Session Timeout**: Automatic logout for security
- **Audit Logging**: Complete activity tracking

## Accessibility Features

- Large text mode support
- High contrast display options
- Audio support for visually impaired users
- Simple, clear navigation
- Multi-language support (configurable)
- Touch-friendly interface design

## Target Users

This system is designed for:
- Vulnerable individuals seeking support services
- Homeless individuals
- Those experiencing food insecurity
- People needing mental health support
- Job seekers
- Individuals requiring legal assistance
- Anyone needing access to community resources

## Service Provider Integration

The system supports integration with various service providers:
- Housing services (emergency shelter, transitional, permanent)
- Food banks and meal programs
- Healthcare clinics
- Mental health centers
- Workforce development programs
- Legal aid societies
- Family service organizations

## Benefits

### For Clients
- **Empowerment**: Self-service tools for independence
- **Privacy**: Anonymous options and secure data handling
- **Comprehensive**: All-in-one platform for multiple needs
- **Accessible**: Easy-to-use interface with accessibility features
- **Supportive**: Compassionate, judgment-free assistance

### For Service Providers
- **Efficiency**: Automated referral and case management
- **Coordination**: Better communication between providers
- **Insights**: Data-driven understanding of client needs
- **Tracking**: Progress monitoring and outcome measurement
- **Integration**: Connect clients with appropriate services

### For Organizations
- **Impact**: Measurable outcomes and client success tracking
- **Scalability**: Serve more clients with existing resources
- **Quality**: Consistent, professional service delivery
- **Reporting**: Comprehensive data for grants and reporting
- **Innovation**: Modern approach to social services

## Future Enhancements

- Mobile app integration
- Video counseling capabilities
- AI-powered need prediction
- Multi-language interface
- Voice interaction support
- Integration with government assistance programs
- Blockchain for secure credential verification
- Predictive analytics for intervention timing

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is created to serve vulnerable populations and improve access to social services.

## Support

For questions, issues, or support, please contact the project maintainers or open an issue on GitHub.

## Acknowledgments

This system is designed with compassion and respect for the dignity of all individuals seeking help. It aims to provide professional support while empowering clients on their journey toward positive life changes.

---

**KioskHelp** - Professional and Compassionate Support for Those Who Need It Most