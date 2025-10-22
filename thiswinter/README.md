# KioskHelp Web Portal - Winter Edition

## Overview

This is a comprehensive web-based version of the KioskHelp system, featuring:

- **Advanced Questionnaire System**: Extended assessment that creates cases and assigns tasks automatically
- **Admin Portal**: Complete administrative control with troubleshooting tools
- **20 Different Themes**: Customizable visual themes for different preferences
- **10 Dashboard Layouts**: Multiple layout options for organizing information
- **10 Widgets**: Configurable dashboard widgets
- **Feature Toggles**: Enable/disable features from admin panel
- **Full Customization**: Customize layouts, themes, and styles from admin panel

## Installation

1. Install dependencies:
```bash
pip install flask
```

2. Run the application:
```bash
cd thiswinter
python app.py
```

3. Access the application:
- Main site: http://localhost:5000
- Admin portal: http://localhost:5000/admin/login
  - Username: admin
  - Password: changeme123

## Features

### Client Portal
- **Registration**: New client registration with consent management
- **Comprehensive Questionnaire**: Extended assessment covering:
  - Housing status and safety
  - Food security
  - Healthcare access
  - Mental health support
  - Employment status and training
  - Legal assistance needs
  - Transportation
  - Immediate needs identification
  
- **Automatic Case Creation**: Cases are created automatically from questionnaire responses
- **Task Assignment**: Tasks are automatically assigned to clients and staff based on identified needs
- **Dashboard**: Personal dashboard showing cases, tasks, appointments, and resources
- **Resources**: Access to educational materials and support resources
- **Appointments**: View and manage appointments with service providers
- **Messages**: Communication with case managers and staff

### Admin Portal
- **Client Management**: View and manage all registered clients
- **Case Management**: Monitor all active cases and their progress
- **Task Management**: View and assign tasks to clients and staff
- **Theme Management**: Configure and customize 20 different themes
- **Layout Management**: Configure 10 different dashboard layouts
- **Widget Management**: Enable/disable and configure 10 dashboard widgets
- **Feature Toggles**: Turn features on/off system-wide
- **Troubleshooting Tools**:
  - System health checks
  - Diagnostic tools
  - System logs viewer
  - Automatic repair functions
  - Performance monitoring
- **Analytics Dashboard**: View system usage and performance metrics
- **Report Generation**: Generate comprehensive reports
- **Settings**: Configure system-wide settings

### Themes (20 Available)
1. Professional Blue (Default)
2. Modern Dark
3. Light Minimal
4. Warm Orange
5. Cool Green
6. Corporate Grey
7. Vibrant Purple
8. Ocean Blue
9. Sunset Red
10. Forest Green
11. Midnight Black
12. Pastel Pink
13. Earth Tone
14. High Contrast
15. Accessibility Friendly
16. Classic White
17. Gradient Blue
18. Material Design
19. Bootstrap Inspired
20. Custom Branded

### Dashboard Layouts (10 Available)
1. Default - Standard two-column layout
2. Compact - Minimalist single-column
3. Expanded - Full-width with all widgets
4. Grid 3-Column - Three-column grid
5. Grid 4-Column - Four-column grid
6. Sidebar Left - Layout with left sidebar
7. Sidebar Right - Layout with right sidebar
8. Split Screen - Equal split layout
9. Tabbed - Tabbed interface
10. Accordion - Collapsible sections

### Widgets (10 Available)
1. Welcome Widget - Greeting and quick stats
2. Quick Actions - Action buttons
3. Recent Cases - Recently updated cases
4. Pending Tasks - Task list
5. Notifications - System alerts
6. Calendar - Appointments and events
7. Statistics - Performance metrics
8. Resource Links - Quick links
9. Announcements - System announcements
10. Help Tips - Contextual help

## Architecture

```
thiswinter/
├── app.py                          # Main Flask application
├── config/
│   └── settings.py                 # Configuration settings
├── app/
│   ├── routes/
│   │   ├── client_routes.py        # Client-facing routes
│   │   └── admin_routes.py         # Admin routes
│   ├── models/
│   │   ├── theme_manager.py        # Theme management
│   │   ├── widget_manager.py       # Widget management
│   │   └── feature_manager.py      # Feature flags
│   └── utils/                      # Utility functions
├── templates/
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── client/                     # Client templates
│   │   ├── questionnaire.html      # Extended questionnaire
│   │   ├── dashboard.html          # Client dashboard
│   │   ├── cases.html              # View cases
│   │   ├── tasks.html              # View tasks
│   │   └── ...
│   └── admin/                      # Admin templates
│       ├── dashboard.html          # Admin dashboard
│       ├── login.html              # Admin login
│       ├── themes.html             # Theme management
│       ├── features.html           # Feature toggles
│       ├── troubleshoot.html       # Troubleshooting
│       └── ...
├── static/
│   ├── css/
│   │   └── main.css                # Main stylesheet
│   ├── js/
│   │   └── main.js                 # Main JavaScript
│   ├── themes/                     # 20 theme CSS files
│   └── images/                     # Images and assets
└── tests/                          # Test files
```

## API Endpoints

### Public
- `GET /` - Home page
- `GET /client/start` - Start client session
- `POST /client/register` - Register new client
- `GET /client/questionnaire` - Questionnaire page
- `POST /client/submit-questionnaire` - Submit questionnaire

### Client Portal
- `GET /client/dashboard` - Client dashboard
- `GET /client/cases` - View cases
- `GET /client/tasks` - View tasks
- `GET /client/resources` - Browse resources
- `GET /client/appointments` - View appointments
- `GET /client/messages` - View messages

### Admin Portal
- `POST /admin/login` - Admin login
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/clients` - Manage clients
- `GET /admin/cases` - Manage cases
- `GET /admin/tasks` - Manage tasks
- `GET /admin/themes` - Manage themes
- `POST /admin/themes/set` - Set default theme
- `POST /admin/themes/customize` - Customize theme
- `GET /admin/layouts` - Manage layouts
- `POST /admin/layouts/customize` - Customize layout
- `GET /admin/widgets` - Manage widgets
- `POST /admin/widgets/toggle` - Toggle widget
- `POST /admin/widgets/configure` - Configure widget
- `GET /admin/features` - Manage features
- `POST /admin/features/toggle` - Toggle feature
- `GET /admin/troubleshoot` - Troubleshooting dashboard
- `POST /admin/troubleshoot/system-check` - Run system check
- `POST /admin/troubleshoot/diagnostics` - Run diagnostics
- `POST /admin/troubleshoot/repair` - Repair issues
- `GET /admin/analytics` - Analytics dashboard
- `GET /admin/reports` - Reports
- `POST /admin/reports/generate` - Generate report

### API
- `GET /api/themes` - Get all themes
- `GET /api/widgets` - Get all widgets
- `GET /api/features` - Get all features

## Customization

### Changing Themes
Admin users can change themes from the admin portal:
1. Login to admin portal
2. Navigate to Theme Management
3. Select desired theme
4. Click "Set as Default"

### Configuring Widgets
1. Login to admin portal
2. Navigate to Widget Management
3. Toggle widgets on/off
4. Configure widget settings
5. Save changes

### Managing Features
1. Login to admin portal
2. Navigate to Feature Management
3. Toggle features on/off
4. Changes take effect immediately

### Customizing Layouts
1. Login to admin portal
2. Navigate to Layout Management
3. Select layout
4. Customize widget positions
5. Save changes

## Testing

The system includes comprehensive testing coverage:

```bash
cd thiswinter
python -m pytest tests/
```

## Troubleshooting

### System Check
From the admin portal, navigate to Troubleshooting > System Check to:
- Verify all modules are functioning
- Check database connectivity
- Monitor active sessions
- Verify external integrations
- Check system performance

### Diagnostics
Run diagnostics to identify:
- Clients with missing information
- Stalled cases
- Failed referrals
- Orphaned data

### Repair Tools
Automatic repair functions for:
- Stalled cases
- Orphaned data
- Failed referrals

## Security

- Session management with timeout
- Admin authentication required
- CSRF protection
- Input validation
- Secure password handling (use environment variables in production)

## Production Deployment

1. Change default admin password
2. Set SECRET_KEY environment variable
3. Use production database (PostgreSQL recommended)
4. Enable HTTPS
5. Configure proper logging
6. Set up backup system
7. Enable monitoring

## Support

For issues, questions, or feature requests, please contact the system administrator.

## License

This system is designed to support vulnerable populations and improve access to social services.
