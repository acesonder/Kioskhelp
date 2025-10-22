# KioskHelp API Reference

Complete API documentation for the KioskHelp system modules.

## Table of Contents

- [Main System (kioskhelp.py)](#main-system)
- [Registration (registration.py)](#registration-module)
- [Consent (consent.py)](#consent-module)
- [Intake (intake.py)](#intake-module)
- [Assessment (assessment.py)](#assessment-module)
- [Referral (referral.py)](#referral-module)
- [Communication (communication.py)](#communication-module)
- [Resources (resources.py)](#resources-module)
- [Case Management (case_management.py)](#case-management-module)
- [Self-Help Tools (self_help_tools.py)](#self-help-tools-module)

---

## Main System

### KioskHelpSystem

Main application class integrating all modules.

#### Methods

**`start_session(client_type='new')`**
- Starts a new kiosk session
- Returns: Session information with session_id

**`complete_registration_workflow(session_id, client_data)`**
- Completes full registration for new client
- Returns: Client ID and intake ID

**`complete_intake_workflow(intake_id, responses)`**
- Completes intake assessment
- Returns: Priority needs and assessment ID

**`generate_comprehensive_plan(client_id, assessment_id)`**
- Generates complete support plan
- Returns: Case ID, referrals, resources, next steps

**`get_client_dashboard(client_id)`**
- Gets comprehensive client dashboard
- Returns: Dashboard with all client metrics

**`end_session(session_id)`**
- Ends kiosk session
- Returns: Session summary

---

## Registration Module

### ClientRegistration

Manages client registration and identity.

#### Methods

**`register_new_client(data)`**
- Registers a new client
- Parameters:
  - `data` (dict): Client information
    - `email` (str, optional): Client email
    - `name` (str, optional): Client name
    - `anonymous` (bool): Anonymous registration
- Returns: Registration result with client_id

**`get_existing_client(client_id)`**
- Retrieves existing client information
- Returns: Client record or None

**`update_client(client_id, data)`**
- Updates client information
- Returns: Update result

### ClientVerification

Handles identity verification for returning clients.

#### Methods

**`verify_by_id(client_id, verification_code)`**
- Verifies client identity
- Returns: Boolean verification result

**`send_verification_code(contact, method='email')`**
- Sends verification code
- Returns: Send result with code

---

## Consent Module

### ConsentManager

Manages client consent and permissions.

#### Consent Types
- `data_processing`
- `data_sharing`
- `service_referral`
- `communication`
- `case_management`
- `research_participation`

#### Methods

**`record_consent(client_id, consent_data)`**
- Records client consent
- Parameters:
  - `consent_data` (dict):
    - `consent_type` (str): Type of consent
    - `granted` (bool): Consent status
    - `notes` (str, optional): Additional notes
- Returns: Consent record confirmation

**`check_consent(client_id, consent_type)`**
- Checks if consent is granted
- Returns: Boolean consent status

**`revoke_consent(client_id, consent_type)`**
- Revokes a specific consent
- Returns: Revocation result

**`get_consent_summary(client_id)`**
- Gets summary of all consents
- Returns: Consent summary dict

---

## Intake Module

### IntakeAssessment

Manages initial client intake process.

#### Methods

**`start_intake(client_id)`**
- Starts intake assessment
- Returns: Intake ID and questions

**`record_response(intake_id, question_id, response)`**
- Records response to intake question
- Returns: Recording confirmation

**`complete_intake(intake_id)`**
- Completes intake and analyzes needs
- Returns: Priority needs and summary

**`get_intake_summary(intake_id)`**
- Gets intake assessment summary
- Returns: Complete intake data

---

## Assessment Module

### ClientAssessment

Handles detailed client assessments.

#### Assessment Categories
- `housing`
- `mental_health`
- `employment`
- `healthcare`

#### Methods

**`create_assessment(client_id, categories)`**
- Creates new assessment
- Parameters:
  - `categories` (list): Assessment categories to include
- Returns: Assessment ID and questions

**`submit_response(assessment_id, question_id, category, response)`**
- Submits response to assessment question
- Returns: Submission confirmation

**`complete_assessment(assessment_id)`**
- Completes assessment and generates insights
- Returns: Insights, services, priority level

**`get_assessment_results(assessment_id)`**
- Retrieves assessment results
- Returns: Complete assessment data

---

## Referral Module

### ServiceProvider

Service provider information class.

#### Properties
- `provider_id` (str): Unique identifier
- `name` (str): Provider name
- `services` (list): Services offered
- `contact` (dict): Contact information
- `capacity` (str): Current capacity status

### ReferralSystem

Manages client referrals to service providers.

#### Methods

**`find_providers_for_need(need_category)`**
- Finds matching providers for need
- Returns: List of ServiceProvider objects

**`create_referral(client_id, need_category, priority='medium', notes='')`**
- Creates single referral
- Returns: Referral info with provider details

**`create_multiple_referrals(client_id, needs, priority='medium')`**
- Creates multiple referrals
- Returns: All created referrals

**`update_referral_status(referral_id, status, notes='')`**
- Updates referral status
- Status options: pending, contacted, scheduled, completed, cancelled
- Returns: Update confirmation

**`get_client_referrals(client_id)`**
- Gets all client referrals
- Returns: List of referrals

**`get_referral_details(referral_id)`**
- Gets detailed referral information
- Returns: Complete referral with provider details

---

## Communication Module

### CommunicationSystem

Manages client communication and messaging.

#### Methods

**`send_message(client_id, message_type, content, method='email')`**
- Sends message to client
- Methods: email, sms, app
- Returns: Send confirmation

**`get_client_messages(client_id, unread_only=False)`**
- Gets client messages
- Returns: List of messages

**`mark_message_read(client_id, message_id)`**
- Marks message as read
- Returns: Update confirmation

**`create_notification(client_id, notification_type, title, content, priority='normal')`**
- Creates client notification
- Priority: low, normal, high, urgent
- Returns: Notification info

**`get_notifications(client_id, active_only=True)`**
- Gets client notifications
- Returns: List of notifications

**`dismiss_notification(client_id, notification_id)`**
- Dismisses notification
- Returns: Dismissal confirmation

### AppointmentScheduler

Manages client appointments.

#### Methods

**`schedule_appointment(client_id, provider_id, appointment_type, date_time, notes='')`**
- Schedules new appointment
- Returns: Appointment details

**`get_client_appointments(client_id, upcoming_only=False)`**
- Gets client appointments
- Returns: List of appointments

**`update_appointment_status(appointment_id, status)`**
- Updates appointment status
- Status: scheduled, confirmed, completed, cancelled, no_show
- Returns: Update confirmation

**`send_appointment_reminder(appointment_id, communication_system)`**
- Sends appointment reminder
- Returns: Send confirmation

---

## Resources Module

### ResourceLibrary

Provides access to educational resources.

#### Resource Types
- article
- video
- guide
- form
- link

#### Methods

**`search_resources(category=None, keyword=None)`**
- Searches for resources
- Returns: List of matching resources

**`get_resource(resource_id)`**
- Gets specific resource details
- Returns: Complete resource information

**`log_resource_access(client_id, resource_id)`**
- Logs resource access
- Returns: Logging confirmation

**`get_client_history(client_id)`**
- Gets client's resource access history
- Returns: List of accessed resources

**`get_recommended_resources(needs)`**
- Gets recommended resources for needs
- Returns: List of recommended resources

**`get_all_categories()`**
- Gets all resource categories
- Returns: List of categories

---

## Case Management Module

### CaseManager

Smart case management system.

#### Case Status
- open
- in_progress
- pending
- resolved
- closed

#### Case Priority
- critical
- high
- medium
- low

#### Methods

**`create_case(client_id, needs, priority='medium', description='')`**
- Creates new case
- Returns: Case ID and details

**`update_case_status(case_id, status, notes='')`**
- Updates case status
- Returns: Update confirmation

**`add_case_note(case_id, note, author='system')`**
- Adds note to case
- Returns: Note confirmation

**`set_case_goals(case_id, goals)`**
- Sets case goals
- Parameters:
  - `goals` (list): List of goal dicts with description and target_date
- Returns: Created goals

**`update_goal_status(case_id, goal_id, status)`**
- Updates goal status
- Status: not_started, in_progress, completed, cancelled
- Returns: Update confirmation

**`track_progress(case_id, metric, value)`**
- Tracks progress metric
- Returns: Tracking confirmation

**`get_case_summary(case_id)`**
- Gets comprehensive case summary
- Returns: Complete case data with progress

**`get_client_cases(client_id, active_only=False)`**
- Gets client cases
- Returns: List of cases

**`generate_case_insights(case_id)`**
- Generates intelligent insights
- Returns: Recommendations, risk factors, success indicators

---

## Self-Help Tools Module

### SelfHelpTools

Collection of interactive self-help tools.

#### Available Tools
1. Budget Planning Tool
2. Housing Search Checklist
3. Wellness Tracker
4. Goal Planning Tool
5. Job Search Organizer
6. Personal Crisis Plan
7. Community Resource Finder

#### Methods

**`get_available_tools()`**
- Gets list of all tools
- Returns: List of tool information

**`use_budgeting_tool(client_id, income, expenses)`**
- Creates budget analysis
- Parameters:
  - `income` (float): Monthly income
  - `expenses` (dict): Expense categories and amounts
- Returns: Budget analysis with recommendations

**`use_wellness_tracker(client_id, mood, sleep_hours, notes='')`**
- Tracks daily wellness
- Parameters:
  - `mood` (int): Mood rating 1-10
  - `sleep_hours` (float): Hours of sleep
- Returns: Wellness entry with insights

**`use_goal_planner(client_id, goal, steps, target_date)`**
- Creates goal plan
- Parameters:
  - `goal` (str): Goal description
  - `steps` (list): Steps to achieve goal
  - `target_date` (str): Target completion date
- Returns: Goal plan

**`use_job_search_organizer(client_id, company, position, application_date, status)`**
- Tracks job application
- Returns: Application entry

**`create_crisis_plan(client_id, warning_signs, coping_strategies, support_contacts)`**
- Creates personal crisis plan
- Parameters:
  - `warning_signs` (list): Warning signs to watch for
  - `coping_strategies` (list): Coping strategies
  - `support_contacts` (list): Support contact dicts
- Returns: Crisis plan

**`get_tool_history(client_id, tool_id=None)`**
- Gets tool usage history
- Returns: List of usage entries

**`get_saved_tool_data(client_id, tool_id)`**
- Gets saved tool data
- Returns: Saved data or None

---

## Response Formats

### Success Response
```python
{
    'success': True,
    'message': 'Operation completed successfully',
    # Additional data specific to operation
}
```

### Error Response
```python
{
    'success': False,
    'message': 'Error description'
}
```

## Common Data Types

### Client Data
```python
{
    'client_id': str,
    'name': str (optional),
    'anonymous': bool,
    'registration_date': str (ISO format),
    'status': str
}
```

### Referral Data
```python
{
    'referral_id': str,
    'client_id': str,
    'need_category': str,
    'priority': str,
    'status': str,
    'providers': [ServiceProvider],
    'created_at': str (ISO format)
}
```

### Case Data
```python
{
    'case_id': str,
    'client_id': str,
    'needs': [str],
    'priority': str,
    'status': str,
    'goals': [dict],
    'created_at': str (ISO format)
}
```

---

For complete examples, see `example_usage.py` and `QUICKSTART.md`.
