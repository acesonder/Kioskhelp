# KioskHelp System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     KIOSKHELP MAIN SYSTEM                       │
│                      (kioskhelp.py)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  REGISTRATION │    │    INTAKE     │    │  ASSESSMENT   │
│  & CONSENT    │    │               │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  NEED ANALYSIS   │
                    │  & INSIGHTS      │
                    └──────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   REFERRAL    │    │    CASE       │    │   RESOURCES   │
│   SYSTEM      │    │  MANAGEMENT   │    │   LIBRARY     │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  COMMUNICATION   │
                    │  & APPOINTMENTS  │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  SELF-HELP       │
                    │  TOOLS           │
                    └──────────────────┘
```

## Client Journey Workflow

```
START KIOSK SESSION
        │
        ▼
┌───────────────────┐
│ New or Existing?  │
└───────────────────┘
    │           │
    │ New       │ Existing
    ▼           ▼
┌─────────┐  ┌─────────────┐
│Register │  │  Verify ID  │
│& Consent│  └─────────────┘
└─────────┘          │
    │                │
    └────────┬───────┘
             ▼
    ┌─────────────────┐
    │ Intake          │
    │ Assessment      │
    │ (8 questions)   │
    └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Identify        │
    │ Priority Needs  │
    └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Detailed        │
    │ Assessment      │
    │ (by category)   │
    └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ Generate        │
    │ Insights        │
    └─────────────────┘
             │
        ┌────┴────┐
        │         │
        ▼         ▼
    ┌────────┐ ┌────────┐
    │Create  │ │Generate│
    │Case    │ │Referral│
    └────────┘ └────────┘
        │         │
        └────┬────┘
             ▼
    ┌─────────────────┐
    │ Provide         │
    │ Resources &     │
    │ Self-Help Tools │
    └─────────────────┘
             │
             ▼
    ┌─────────────────┐
    │ View Dashboard  │
    │ & Next Steps    │
    └─────────────────┘
             │
             ▼
      END SESSION
```

## Data Flow

```
CLIENT INPUT
     │
     ▼
┌─────────────────┐
│  Intake Form    │
│  Responses      │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│  Assessment     │
│  Responses      │
└─────────────────┘
     │
     ▼
┌─────────────────┐
│  Need Analysis  │
│  Engine         │
└─────────────────┘
     │
     ├──────────────────┐
     │                  │
     ▼                  ▼
┌─────────┐      ┌──────────────┐
│Priority │      │Recommended   │
│Needs    │      │Services      │
└─────────┘      └──────────────┘
     │                  │
     │    ┌─────────────┘
     │    │
     ▼    ▼
┌──────────────────┐
│Service Provider  │
│Matching Engine   │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│Generated         │
│Referrals         │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│Case Created      │
│with Goals        │
└──────────────────┘
     │
     ▼
CLIENT OUTPUT
```

## Module Dependencies

```
kioskhelp.py (Main System)
    │
    ├── registration.py
    │   └── Client identity management
    │
    ├── consent.py
    │   └── Consent tracking
    │
    ├── intake.py
    │   └── Initial assessment
    │
    ├── assessment.py
    │   └── Detailed evaluation
    │
    ├── referral.py
    │   └── Service provider matching
    │
    ├── communication.py
    │   ├── Messaging
    │   ├── Notifications
    │   └── Appointments
    │
    ├── resources.py
    │   └── Educational materials
    │
    ├── case_management.py
    │   ├── Case tracking
    │   ├── Goal management
    │   └── Progress monitoring
    │
    ├── self_help_tools.py
    │   ├── Budgeting
    │   ├── Wellness tracking
    │   ├── Goal planning
    │   └── Crisis planning
    │
    └── config.py
        └── System configuration
```

## Service Provider Integration

```
CLIENT NEEDS
     │
     ▼
┌──────────────────────┐
│ Referral System      │
│ - Need Categories    │
│ - Priority Levels    │
└──────────────────────┘
     │
     ├─────────────────────────────┐
     │                             │
     ▼                             ▼
┌─────────────┐            ┌─────────────┐
│Housing      │            │Healthcare   │
│Services     │            │Services     │
│             │            │             │
│• Emergency  │            │• Primary    │
│• Transitional│           │• Mental     │
│• Permanent  │            │• Dental     │
└─────────────┘            └─────────────┘
     │                             │
     ▼                             ▼
┌─────────────┐            ┌─────────────┐
│Food         │            │Employment   │
│Services     │            │Services     │
│             │            │             │
│• Food Bank  │            │• Job        │
│• Meal Prog. │            │  Placement  │
│• Nutrition  │            │• Training   │
└─────────────┘            └─────────────┘
     │                             │
     └─────────────┬───────────────┘
                   ▼
          ┌─────────────────┐
          │ Referral Record │
          │ - Status Track  │
          │ - Follow-up     │
          └─────────────────┘
```

## Case Management Flow

```
CASE CREATION
     │
     ▼
┌──────────────────┐
│ Initial Needs    │
│ - Housing        │
│ - Employment     │
│ - Healthcare     │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│ Set Goals        │
│ - Short-term     │
│ - Long-term      │
│ - Target Dates   │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│ Assign Priority  │
│ - Critical       │
│ - High           │
│ - Medium         │
│ - Low            │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│ Track Progress   │
│ - Metrics        │
│ - Activities     │
│ - Notes          │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│ Generate         │
│ Insights         │
│ - Risks          │
│ - Success        │
│ - Recommendations│
└──────────────────┘
     │
     ▼
┌──────────────────┐
│ Case Resolution  │
│ or Continuation  │
└──────────────────┘
```

## Self-Help Tools Integration

```
CLIENT NEEDS
     │
     ▼
┌─────────────────────────────────┐
│     Self-Help Tool Selection    │
└─────────────────────────────────┘
     │
     ├──────┬──────┬──────┬──────┬──────┬──────┐
     ▼      ▼      ▼      ▼      ▼      ▼      ▼
 ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐ ┌────┐
 │Budg│ │Well│ │Goal│ │Job │ │Cris│ │House││Rsrc│
 │et  │ │ness│ │Plan│ │Srch│ │Plan│ │Srch││Find│
 └────┘ └────┘ └────┘ └────┘ └────┘ └────┘ └────┘
   │      │      │      │      │      │      │
   └──────┴──────┴──────┴──────┴──────┴──────┘
                    │
                    ▼
          ┌──────────────────┐
          │ Usage Logging    │
          │ & History        │
          └──────────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │ Progress         │
          │ Tracking         │
          └──────────────────┘
```

## Security & Privacy Architecture

```
┌────────────────────────────────────┐
│       Client Interface             │
└────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────┐
│   Session Management               │
│   - Timeout: 5 minutes             │
│   - Anonymous option               │
└────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────┐
│   Consent Validation               │
│   - Required for all operations    │
│   - Granular permissions           │
└────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────┐
│   Data Processing                  │
│   - Encrypted storage              │
│   - Privacy-first design           │
│   - GDPR compliant                 │
└────────────────────────────────────┘
              │
              ▼
┌────────────────────────────────────┐
│   Data Storage                     │
│   - Client data                    │
│   - Case records                   │
│   - Audit logs                     │
└────────────────────────────────────┘
```

## Assessment Categories

```
INTAKE ASSESSMENT
├── Housing Status
├── Food Security
├── Healthcare Access
├── Mental Health Support
├── Employment Status
├── Legal Issues
├── Transportation
└── Immediate Needs

DETAILED ASSESSMENT
├── Housing
│   ├── Current Situation
│   ├── Stability
│   ├── Safety Concerns
│   └── Affordability
│
├── Mental Health
│   ├── Current Support
│   ├── Medication
│   ├── Interest in Services
│   └── Crisis Needs
│
├── Employment
│   ├── Work History
│   ├── Job Search Status
│   ├── Barriers
│   └── Training Interest
│
└── Healthcare
    ├── Insurance Status
    ├── Primary Care
    ├── Ongoing Conditions
    └── Medication Access
```

## Technology Stack

```
┌─────────────────────────────────────┐
│        Application Layer            │
│                                     │
│  Python 3.7+                        │
│  - Standard Library                 │
│  - Object-Oriented Design           │
│  - Modular Architecture             │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        Business Logic Layer         │
│                                     │
│  - Registration & Consent           │
│  - Assessment Engine                │
│  - Matching Algorithms              │
│  - Case Management Logic            │
│  - Self-Help Tools                  │
└─────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────┐
│        Data Layer                   │
│                                     │
│  - In-memory storage (current)      │
│  - SQLite ready                     │
│  - Encryption support               │
└─────────────────────────────────────┘
```

---

For implementation details, see:
- README.md - Full documentation
- QUICKSTART.md - Getting started guide
- API_REFERENCE.md - API documentation
- example_usage.py - Working examples
