# Deployment Instructions

## 📦 What You Have

This package contains a complete Field Operations Tracking System built with Flask for Occamy Bioscience.

## 📋 Files Included

```
occamy-field-ops/
├── app.py                      # Main Flask application (500+ lines)
├── requirements.txt            # Python dependencies
├── Procfile                    # For Heroku deployment
├── runtime.txt                 # Python version specification
├── .gitignore                  # Git ignore rules
├── README.md                   # Complete documentation
├── QUICKSTART.md              # Quick start guide
├── PROJECT_OVERVIEW.md        # Detailed project overview
├── DEPLOYMENT.md              # This file
├── create_demo_data.py        # Script to create sample data
├── test_system.py             # System verification script
├── templates/
│   ├── login.html             # Login page
│   ├── admin_dashboard.html   # Admin dashboard
│   └── field_dashboard.html   # Field officer dashboard
└── static/
    └── uploads/               # Directory for file uploads
```

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install Flask Flask-SQLAlchemy Flask-Login Werkzeug python-dotenv
```

Or using the requirements file:
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The server will start on `http://localhost:5000` and automatically create:
- Database file: `occamy.db`
- Default admin account: `admin` / `admin123`

### Step 3: Access the System
1. Open browser: `http://localhost:5000`
2. Login as admin: `admin` / `admin123`
3. Create field officers and start tracking!

## 📱 Optional: Add Demo Data

To test with realistic data:
```bash
python create_demo_data.py
```

This creates:
- 3 sample field officers
- 7 days of activity logs
- Sample meetings, sales, and distributions

Demo officer credentials:
- `rajesh_kumar` / `demo123` (Lucknow, UP)
- `priya_sharma` / `demo123` (Ludhiana, Punjab)
- `amit_patel` / `demo123` (Ahmedabad, Gujarat)

## 🔧 System Verification

Test that everything is working:
```bash
python test_system.py
```

This will check:
- ✓ All required packages installed
- ✓ File structure correct
- ✓ Database accessible
- ✓ Routes working

## 🌐 Production Deployment Options

### Option 1: Heroku (Easiest)

1. **Install Heroku CLI**: Download from https://devcenter.heroku.com/articles/heroku-cli

2. **Login and Create App**:
```bash
heroku login
heroku create your-app-name
```

3. **Add PostgreSQL** (optional, for production):
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Deploy**:
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

5. **Initialize Database**:
```bash
heroku run python app.py
```

6. **Open App**:
```bash
heroku open
```

### Option 2: Docker

1. **Create Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

2. **Build and Run**:
```bash
docker build -t occamy-field-ops .
docker run -p 5000:5000 occamy-field-ops
```

### Option 3: DigitalOcean App Platform

1. Connect your GitHub repository
2. Select Python as the language
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`
5. Deploy

### Option 4: AWS EC2

1. **Launch EC2 Instance** (Ubuntu 20.04 or later)

2. **SSH into instance and install**:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx -y
```

3. **Setup application**:
```bash
git clone your-repo
cd occamy-field-ops
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. **Create systemd service** (`/etc/systemd/system/occamy.service`):
```ini
[Unit]
Description=Occamy Field Operations
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/occamy-field-ops
Environment="PATH=/home/ubuntu/occamy-field-ops/venv/bin"
ExecStart=/home/ubuntu/occamy-field-ops/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

5. **Start service**:
```bash
sudo systemctl start occamy
sudo systemctl enable occamy
```

6. **Configure Nginx** as reverse proxy

### Option 5: Google Cloud Run

1. **Install gcloud CLI**

2. **Build and deploy**:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/occamy
gcloud run deploy --image gcr.io/PROJECT_ID/occamy --platform managed
```

## 🔐 Production Security Checklist

Before deploying to production:

- [ ] Change admin password from default
- [ ] Set SECRET_KEY environment variable
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS/SSL
- [ ] Set up regular database backups
- [ ] Configure CORS if needed
- [ ] Add rate limiting
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure logging
- [ ] Review and update security settings

## 🗄️ Database Migration (SQLite → PostgreSQL)

For production, migrate to PostgreSQL:

1. **Install PostgreSQL driver**:
```bash
pip install psycopg2-binary
```

2. **Update app.py** database URI:
```python
# Replace SQLite URI with PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or \
    'postgresql://user:password@localhost/occamy_db'
```

3. **Create database**:
```bash
createdb occamy_db
```

4. **Run application** to create tables:
```bash
python app.py
```

## 📊 Performance Optimization

For high traffic:

1. **Use Gunicorn** with multiple workers:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Add Redis** for session management:
```bash
pip install redis flask-session
```

3. **Enable caching** for static assets

4. **Use CDN** for static files

5. **Database indexing** - already implemented in models

## 🔍 Monitoring & Logging

### Basic Logging
Add to app.py:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Production Monitoring
- **Sentry**: Error tracking
- **New Relic**: Application monitoring
- **DataDog**: Infrastructure monitoring

## 🌍 Environment Variables

Set these in production:

```bash
export SECRET_KEY='your-secret-key-here'
export DATABASE_URL='postgresql://user:pass@host/db'
export FLASK_ENV='production'
```

For Heroku:
```bash
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set FLASK_ENV='production'
```

## 📱 Mobile Access

The application is mobile-optimized and works on:
- ✅ Chrome Mobile
- ✅ Safari iOS
- ✅ Firefox Mobile
- ✅ Samsung Internet

### PWA Setup (Optional)
To make it installable as a mobile app, add:
1. `manifest.json` for PWA
2. Service worker for offline support
3. App icons

## 🧪 Testing in Production

After deployment:

1. **Verify login** works
2. **Create test user** as field officer
3. **Test location** services work (requires HTTPS)
4. **Log sample activities**
5. **Check admin dashboard** updates
6. **Test on mobile device**

## 🔄 Backup & Recovery

### Database Backup (SQLite)
```bash
# Backup
cp occamy.db occamy.db.backup

# Restore
cp occamy.db.backup occamy.db
```

### Database Backup (PostgreSQL)
```bash
# Backup
pg_dump occamy_db > backup.sql

# Restore
psql occamy_db < backup.sql
```

### Automated Backups
Set up cron job:
```bash
# Add to crontab
0 2 * * * pg_dump occamy_db > /backups/occamy_$(date +\%Y\%m\%d).sql
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Find and kill process
lsof -ti:5000 | xargs kill -9

# Or use different port
export FLASK_RUN_PORT=8000
python app.py
```

### Database Issues
```bash
# Reset database
rm occamy.db
python app.py
```

### Location Not Working
- Ensure HTTPS in production
- Check browser permissions
- Verify geolocation API is enabled

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

## 📞 Support & Resources

### Documentation
- README.md - Complete documentation
- QUICKSTART.md - Quick start guide
- PROJECT_OVERVIEW.md - Technical details

### API Endpoints
All documented in README.md under "API Endpoints" section

### Demo Video Script
Available in PROJECT_OVERVIEW.md under "Video Demo Points"

## ✅ Pre-Flight Checklist

Before going live:

**Technical**
- [ ] All dependencies installed
- [ ] Database initialized
- [ ] Admin account created
- [ ] Environment variables set
- [ ] HTTPS configured
- [ ] Domain configured

**Testing**
- [ ] Login works
- [ ] Field officer can log work
- [ ] Location tracking works
- [ ] Admin dashboard shows data
- [ ] Mobile responsive
- [ ] Forms validate correctly

**Security**
- [ ] Default passwords changed
- [ ] Secret keys updated
- [ ] Database secured
- [ ] Backups configured
- [ ] Error pages don't leak info

**Performance**
- [ ] Load tested
- [ ] Database optimized
- [ ] Static files cached
- [ ] Gunicorn configured

## 🎉 You're Ready!

Your Occamy Field Operations system is ready to deploy!

**Quick Deploy Commands:**
```bash
# Local testing
python app.py

# Production with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With demo data
python create_demo_data.py
```

**Default Credentials:**
- Admin: `admin` / `admin123`
- Demo Officers: username / `demo123`

---

**Built for Occamy Bioscience Hackathon**
*Track the truth. Scale the impact.* 🐄
