# KioskHelp Web Portal - Quick Start Guide

## Getting Started in 3 Steps

### 1. Install Dependencies
```bash
cd thiswinter
pip install -r requirements.txt
```

### 2. Start the Server
```bash
python app.py
```

The server will start at: **http://localhost:5000**

### 3. Access the Portal

#### For Clients:
- Visit: **http://localhost:5000**
- Click "Get Started" to register
- Complete the comprehensive questionnaire
- View your dashboard, cases, and tasks

#### For Administrators:
- Visit: **http://localhost:5000/admin/login**
- Username: `admin`
- Password: `changeme123`
- Access all management and troubleshooting tools

## Quick Feature Overview

### Client Features
- **Registration**: New client registration with consent
- **Questionnaire**: 8-section comprehensive assessment
- **Dashboard**: Personal dashboard with cases, tasks, resources
- **Cases**: View all assigned cases
- **Tasks**: See tasks assigned to you
- **Resources**: Browse educational materials
- **Appointments**: Manage appointments
- **Messages**: Communication hub

### Admin Features
- **Dashboard**: System overview with statistics
- **Client Management**: View and manage all clients
- **Case Management**: Monitor and manage all cases
- **Task Management**: View and assign tasks
- **Theme Management**: Switch between 20 themes
- **Layout Management**: Configure 10 dashboard layouts
- **Widget Management**: Toggle and configure 10 widgets
- **Feature Toggles**: Enable/disable 20+ features
- **Troubleshooting**: Diagnostics and repair tools
- **Analytics**: System usage metrics
- **Reports**: Generate comprehensive reports

## What Makes This Special

### Automatic Case & Task Creation
When a client completes the questionnaire:
1. System analyzes responses
2. Creates case automatically
3. Generates tasks for client (e.g., "Complete housing application")
4. Generates tasks for staff (e.g., "Review housing options")
5. Assigns appropriate service providers
6. Creates comprehensive support plan

### 20 Themes
Switch instantly between themes:
- Professional Blue (Default)
- Modern Dark
- Light Minimal
- Warm Orange
- Cool Green
- Corporate Grey
- Vibrant Purple
- Ocean Blue
- Sunset Red
- Forest Green
- Midnight Black
- Pastel Pink
- Earth Tone
- High Contrast
- Accessibility Friendly
- Classic White
- Gradient Blue
- Material Design
- Bootstrap Inspired
- Custom Branded

### 10 Dashboard Layouts
Choose your preferred layout:
1. Default - Standard two-column
2. Compact - Minimalist single-column
3. Expanded - Full-width
4. Grid 3-Column
5. Grid 4-Column
6. Sidebar Left
7. Sidebar Right
8. Split Screen
9. Tabbed Interface
10. Accordion Sections

### 10 Configurable Widgets
Enable/disable and configure:
1. Welcome Widget
2. Quick Actions
3. Recent Cases
4. Pending Tasks
5. Notifications
6. Calendar
7. Statistics
8. Resource Links
9. Announcements
10. Help Tips

### Troubleshooting Tools
Admin portal includes:
- **System Check**: Verify all modules functioning
- **Diagnostics**: Identify issues (stalled cases, failed referrals)
- **Auto Repair**: Fix common problems automatically
- **Log Viewer**: Monitor system activity
- **Performance Monitor**: Track system health

## Testing

Run the comprehensive test suite:
```bash
python tests/test_all.py
```

Expected result: **6/6 tests passed (100%)**

## File Structure

```
thiswinter/
├── app.py                  # Main Flask application
├── config/                 # Configuration
├── app/
│   ├── routes/            # Client and admin routes
│   └── models/            # Theme, widget, feature managers
├── templates/             # HTML templates
│   ├── client/           # Client pages
│   └── admin/            # Admin pages
├── static/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript
│   └── themes/           # 20 theme CSS files
└── tests/                # Test suite
```

## Common Tasks

### Change Admin Password
Edit `config/settings.py`:
```python
ADMIN_PASSWORD = 'your-new-password'
```

### Change Default Theme
From admin portal:
1. Login as admin
2. Go to Theme Management
3. Select theme
4. Click "Set as Default"

### Enable/Disable Features
From admin portal:
1. Login as admin
2. Go to Feature Management
3. Toggle features on/off
4. Changes apply immediately

### View System Logs
From admin portal:
1. Login as admin
2. Go to Troubleshooting > View Logs
3. Review system activity

### Run Diagnostics
From admin portal:
1. Login as admin
2. Go to Troubleshooting
3. Click "Run System Check"
4. Review results
5. Use "Auto Repair" if issues found

## Production Deployment

For production use:
1. Change `SECRET_KEY` in settings
2. Change admin password
3. Use production WSGI server (gunicorn, uWSGI)
4. Enable HTTPS
5. Use production database (PostgreSQL)
6. Set up proper logging
7. Configure backup system

## Need Help?

- See `README.md` for full documentation
- See `IMPLEMENTATION.md` for technical details
- Check `tests/test_all.py` for usage examples

## Summary

You now have a fully functional web portal with:
✅ Extended questionnaire creating cases and tasks
✅ Advanced admin portal with troubleshooting
✅ 20 themes, 10 layouts, 10 widgets
✅ 20+ feature toggles
✅ Full customization capabilities
✅ Production-ready architecture

Enjoy using KioskHelp Web Portal!
