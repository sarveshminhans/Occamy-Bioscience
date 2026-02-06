# Occamy Field Operations Tracking System

A comprehensive mobile-first web application for tracking field operations, meetings, sales, and distribution activities in rural supply chains.

## 🎯 Problem Statement

Occamy Bioscience operates through field officers and distributors across rural India. This system replaces manual WhatsApp-based tracking with a structured, auditable, data-driven platform that:

- Tracks daily on-ground activities of field officers
- Monitors travel, meetings, and interactions
- Centralizes sales, farmer interactions, and distribution data
- Provides real-time dashboards and analytics for admins

## ✨ Key Features

### 🔐 Authentication & Authorization
- **Secure Login System**: Username/password authentication with session management
- **Role-Based Access Control (RBAC)**: 
  - Admin: Full system access, user management, analytics
  - Field Officer: Activity logging, location tracking, meeting/sales recording
- **Protected Routes**: All endpoints secured based on user roles
- **Password Hashing**: Werkzeug security for password protection

### 👥 Admin Features
- **Comprehensive Dashboard**: Real-time statistics and KPIs
- **User Management**: Create and manage field officers
- **Activity Monitoring**: View all field activities across states
- **Analytics**: 
  - Active officers tracking
  - Meeting and sales statistics
  - Distance traveled metrics
  - B2C vs B2B sales breakdown
  - State-wise performance analysis
- **Data Tables**: Sortable views for meetings, sales, and activities

### 📱 Field Officer Features

#### Work Log Management
- **Start/End Work Day**: GPS-tagged work session tracking
- **Odometer Readings**: Record vehicle mileage
- **Automatic Distance Calculation**: Based on odometer readings
- **Location Logging**: Periodic GPS tracking throughout the day

#### Meeting Management
**One-on-One Meetings:**
- Person name and contact details
- Category: Farmer/Seller/Influencer
- Business potential estimation
- GPS location capture
- Notes and photos support

**Group Meetings:**
- Village location
- Number of attendees
- Meeting type (training, demo, etc.)
- GPS location capture
- Farm photos

#### Sample Distribution Tracking
- Recipient information
- Product details and quantity
- Distribution purpose (trial, demo, follow-up)
- Location-tagged records
- Notes for follow-up

#### Sales & Order Capture
**B2C Sales (Direct to Farmer):**
- Customer details
- Product SKU and name
- Pack size and quantity
- Pricing information
- Repeat order tracking

**B2B Sales (Distributor/Reseller):**
- Business customer details
- Bulk ordering support
- Distribution mode tracking
- Location-tagged transactions

#### Personal Dashboard
- Weekly activity summary
- Meeting count
- Sales count
- Samples distributed
- Total distance traveled

## 🏗️ Technical Architecture

### Backend (Flask)
- **Framework**: Flask 3.0.0
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Security**: Werkzeug password hashing
- **API**: RESTful JSON endpoints

### Frontend
- **Design**: Mobile-first responsive UI
- **Styling**: Pure CSS (no external frameworks for offline capability)
- **JavaScript**: Vanilla JS for interactivity
- **Location Services**: HTML5 Geolocation API

### Database Schema

**User Model:**
- id, username, email, password_hash
- role (admin/field_officer)
- name, state, district, phone
- is_active, created_at

**WorkLog Model:**
- Daily work sessions
- Start/end times and locations
- Odometer readings
- Distance calculations

**Meeting Model:**
- Meeting type (one-on-one/group)
- Contact details or village info
- Business potential
- Location data

**SampleDistribution Model:**
- Recipient information
- Product and quantity
- Purpose tracking
- Location data

**Sale Model:**
- Sale type (B2C/B2B)
- Customer details
- Product information
- Pricing and quantities
- Location data

**LocationLog Model:**
- Continuous GPS tracking
- Activity type tagging
- Timestamp records

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser with geolocation support

### Step 1: Clone/Download the Project
```bash
# If using git
git clone <repository-url>
cd occamy-field-ops

# Or extract the zip file
unzip occamy-field-ops.zip
cd occamy-field-ops
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Access the System
1. Open your browser and go to `http://localhost:5000`
2. Login with default admin credentials:
   - Username: `admin`
   - Password: `admin123`

## 🚀 Usage Guide

### For Administrators

#### First Login
1. Login with admin credentials
2. Navigate to "Field Officers" tab
3. Click "+ Add Officer" to create field officer accounts

#### Creating Field Officers
Required information:
- Full Name
- Username (unique)
- Email (unique)
- Password
- Phone (optional)
- State and District (optional)

#### Monitoring Activities
- **Overview Tab**: View real-time statistics and KPIs
- **Activities Tab**: Track daily field work and distance traveled
- **Meetings Tab**: Review all meeting logs
- **Sales Tab**: Monitor sales performance

### For Field Officers

#### Starting Your Work Day
1. Login with your credentials
2. Click "Start Work Day"
3. Allow location access when prompted
4. Enter your vehicle's odometer reading
5. System will track your location automatically

#### Logging a Meeting

**One-on-One Meeting:**
1. Click "Log Meeting" quick action
2. Select "One-on-One Meeting"
3. Enter person details:
   - Name
   - Category (Farmer/Seller/Influencer)
   - Contact number (optional)
   - Business potential estimate
4. Add notes
5. Location is captured automatically
6. Submit

**Group Meeting:**
1. Click "Log Meeting" quick action
2. Select "Group Meeting"
3. Enter details:
   - Village name
   - Number of attendees
   - Meeting type
4. Add notes
5. Submit

#### Distributing Samples
1. Click "Sample Distribution" quick action
2. Enter recipient details
3. Select product and quantity
4. Choose purpose (trial/demo/follow-up)
5. Add any notes
6. Submit

#### Recording a Sale
1. Click "Record Sale" quick action
2. Select sale type (B2C or B2B)
3. Enter customer information
4. Fill in product details:
   - Product SKU
   - Product name
   - Pack size
   - Quantity
   - Pricing
5. Select mode (direct/via distributor)
6. Check if repeat order
7. Submit

#### Ending Your Work Day
1. Click "End Work Day"
2. Enter final odometer reading
3. System calculates distance traveled
4. Work session is logged

## 📊 Data & Analytics

### Available Metrics
- Active officers count (daily)
- Total meetings (monthly)
- Total sales (monthly)
- Total distance traveled (monthly)
- B2C vs B2B sales breakdown
- State-wise activity comparison
- Individual officer performance

### Export Capabilities
Data can be accessed via API endpoints for integration with:
- Excel/CSV exports (future enhancement)
- Business intelligence tools
- Custom reporting systems

## 🔒 Security Features

### Authentication
- Password hashing using Werkzeug
- Session-based authentication
- Automatic session expiry
- Logout functionality

### Authorization
- Role-based access control
- Protected API endpoints
- Admin-only routes
- Field officer restrictions

### Data Security
- SQL injection prevention (SQLAlchemy)
- XSS protection (Jinja2 auto-escaping)
- CSRF token support (built into Flask forms)

## 🌐 Offline Capability

### Design Considerations
- Minimal external dependencies
- Pure CSS styling (no CDN requirements)
- Vanilla JavaScript (no external libraries)
- Graceful degradation for poor connectivity

### Future Enhancements for Offline Mode
- Service Worker implementation
- Local storage for offline data
- Background sync when connectivity returns
- Progressive Web App (PWA) capabilities

## 📱 Mobile Optimization

### Responsive Design
- Mobile-first approach
- Touch-friendly interface
- Optimized for small screens
- Bottom navigation for easy thumb access

### Performance
- Lightweight CSS (no frameworks)
- Minimal JavaScript
- Fast page loads
- Optimized for 2G/3G networks

## 🛣️ API Endpoints

### Authentication
- `POST /login` - User login
- `GET /logout` - User logout

### Admin Routes
- `GET /admin/dashboard` - Admin dashboard
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/users` - List field officers
- `POST /api/admin/users` - Create field officer
- `GET /api/admin/activities` - Activity logs
- `GET /api/admin/meetings` - Meeting logs
- `GET /api/admin/sales` - Sales logs

### Field Officer Routes
- `GET /field/dashboard` - Field officer dashboard
- `POST /api/field/worklog/start` - Start work session
- `POST /api/field/worklog/end` - End work session
- `GET /api/field/worklog/status` - Check work status
- `POST /api/field/meeting` - Log meeting
- `POST /api/field/sample` - Log sample distribution
- `POST /api/field/sale` - Record sale
- `POST /api/field/location` - Log GPS location
- `GET /api/field/my-activities` - Personal statistics

## 🧪 Testing the System

### Sample Workflow

1. **Admin Setup:**
   ```
   - Login as admin
   - Create a test field officer
   - Username: "test_officer"
   - Password: "test123"
   ```

2. **Field Officer Workflow:**
   ```
   - Login as test_officer
   - Start work day (odometer: 1000)
   - Log a meeting with a farmer
   - Distribute a sample
   - Record a sale
   - End work day (odometer: 1050)
   ```

3. **Admin Monitoring:**
   ```
   - View overview dashboard
   - Check distance traveled: 50 km
   - Review meeting details
   - Verify sale record
   ```

## 🚀 Deployment Options

### Development Server (Current)
```bash
python app.py
```
Runs on `http://localhost:5000`

### Production Deployment

#### Option 1: Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

#### Option 3: Cloud Platforms
- **Heroku**: Deploy with Procfile
- **AWS Elastic Beanstalk**: Deploy Flask application
- **Google Cloud Run**: Containerized deployment
- **DigitalOcean App Platform**: Direct GitHub integration

## 📈 Scalability Considerations

### Current Limitations
- SQLite database (single file)
- Single server deployment
- No caching layer

### Scaling Recommendations
1. **Database**: Migrate to PostgreSQL or MySQL
2. **Caching**: Implement Redis for session management
3. **File Storage**: Use S3 or similar for photos
4. **Load Balancing**: Nginx reverse proxy
5. **Background Jobs**: Celery for async tasks

## 🔮 Future Enhancements

### High Priority
- [ ] Photo upload and storage
- [ ] Offline data sync
- [ ] Push notifications
- [ ] Excel/PDF export
- [ ] Map view of activities

### Medium Priority
- [ ] SMS/WhatsApp integration
- [ ] Multi-language support
- [ ] Voice notes
- [ ] Farmer feedback forms
- [ ] Inventory management

### Low Priority
- [ ] Mobile apps (iOS/Android)
- [ ] AI-powered insights
- [ ] Predictive analytics
- [ ] Integration with accounting software

## 🐛 Troubleshooting

### Common Issues

**Database locked error:**
```bash
# Delete the database and recreate
rm occamy.db
python app.py
```

**Location not working:**
- Ensure HTTPS (required for geolocation in production)
- Check browser permissions
- Test on localhost first

**Login issues:**
- Clear browser cache and cookies
- Check that database was initialized
- Verify admin credentials

**Port already in use:**
```bash
# Use a different port
export FLASK_RUN_PORT=8000
python app.py
```

## 📝 Development Notes

### File Structure
```
occamy-field-ops/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── login.html             # Login page
│   ├── admin_dashboard.html   # Admin dashboard
│   └── field_dashboard.html   # Field officer dashboard
├── static/                     # Static files
│   ├── css/                   # CSS files (if needed)
│   ├── js/                    # JavaScript files (if needed)
│   └── uploads/               # Uploaded files
└── occamy.db                  # SQLite database (auto-generated)
```

### Database Initialization
The database is automatically created on first run with:
- All necessary tables
- Default admin account

### Customization
- **Branding**: Update logos and colors in CSS
- **States/Districts**: Add to form dropdowns
- **Product List**: Create a products table
- **Validation**: Add custom validation rules

## 🤝 Contributing

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Keep functions small and focused

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push and create pull request
git push origin feature/new-feature
```

## 📄 License

This project is developed for Occamy Bioscience hackathon submission.

## 👥 Support

For issues or questions:
- Check this README first
- Review error logs in console
- Test with sample data
- Contact development team

## 🎉 Acknowledgments

Built for Occamy Bioscience Field Operations Hackathon
- Focus: Rural supply chain management
- Goal: Replace WhatsApp-based tracking
- Impact: Better accountability and data-driven insights

---

**Built with ❤️ for rural India's farming community**
