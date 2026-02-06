# Quick Start Guide - Occamy Field Operations System

## 🚀 Get Started in 5 Minutes

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start the Application
```bash
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
Default admin created: username='admin', password='admin123'
```

### Step 3: (Optional) Load Demo Data
In a new terminal:
```bash
python create_demo_data.py
```

This creates:
- 3 sample field officers
- 7 days of activity data
- Sample meetings, sales, and distributions

### Step 4: Access the Application
Open your browser: `http://localhost:5000`

## 📱 Testing the System

### As Admin
1. Login with:
   - Username: `admin`
   - Password: `admin123`

2. Create a field officer:
   - Go to "Field Officers" tab
   - Click "+ Add Officer"
   - Fill in details
   - Save

3. View dashboard:
   - Check Overview statistics
   - Review Activities
   - Analyze Meetings & Sales

### As Field Officer
1. Login with demo credentials:
   - Username: `rajesh_kumar`
   - Password: `demo123`

2. Start work day:
   - Allow location access
   - Enter odometer: `1000`

3. Log activities:
   - Click "Log Meeting"
   - Click "Sample Distribution"
   - Click "Record Sale"

4. End work day:
   - Enter odometer: `1050`
   - View your statistics

## 🎯 Key Features to Test

### ✅ Authentication
- [x] Admin login
- [x] Field officer login
- [x] Role-based access
- [x] Logout functionality

### ✅ Admin Dashboard
- [x] Real-time statistics
- [x] Create field officers
- [x] View all activities
- [x] Monitor meetings & sales
- [x] State-wise analysis

### ✅ Field Officer Dashboard
- [x] Start/end work day
- [x] Log one-on-one meetings
- [x] Log group meetings
- [x] Distribute samples
- [x] Record B2C sales
- [x] Record B2B sales
- [x] GPS location tracking
- [x] Weekly statistics

## 📊 Sample Data Overview

If you ran `create_demo_data.py`, you have:
- **3 Field Officers** across 3 states
- **7 Days** of activity logs
- **42-84 Meetings** logged
- **21-42 Sample Distributions**
- **14-28 Sales** recorded
- **Distance Traveled**: 210-560 km per officer

## 🔧 Troubleshooting

### Port Already in Use
```bash
# Kill the process
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
python create_demo_data.py
```

### Location Not Working
- Use Chrome or Firefox
- Allow location permissions
- Test on localhost first
- HTTPS required for production

## 📝 Default Credentials

### Admin Account
```
Username: admin
Password: admin123
```

### Demo Field Officers (after running create_demo_data.py)
```
1. Username: rajesh_kumar
   Password: demo123
   Location: Lucknow, Uttar Pradesh

2. Username: priya_sharma
   Password: demo123
   Location: Ludhiana, Punjab

3. Username: amit_patel
   Password: demo123
   Location: Ahmedabad, Gujarat
```

## 🎨 Customization Tips

### Change Branding
Edit templates:
- `templates/login.html` - Update title and logo
- `templates/admin_dashboard.html` - Customize admin UI
- `templates/field_dashboard.html` - Customize field UI

### Add Products
Create a products dropdown in:
- Sample distribution form
- Sales form

### Add States/Districts
Update form options in:
- Admin user creation
- Field officer profile

## 📱 Mobile Testing

### Best Experience On:
- Chrome Mobile
- Safari iOS
- Firefox Mobile

### Testing Checklist:
- [ ] Responsive layout
- [ ] Touch-friendly buttons
- [ ] Location access works
- [ ] Forms are easy to fill
- [ ] Bottom navigation works

## 🚀 Deployment Ready

The system is production-ready with:
- ✅ Secure authentication
- ✅ Role-based access control
- ✅ Mobile-optimized UI
- ✅ Location tracking
- ✅ Data analytics
- ✅ Audit trails

## 📞 Support

For help:
1. Check README.md
2. Review error messages
3. Test with demo data
4. Check browser console

## 🎉 You're All Set!

Start exploring:
1. Admin Dashboard: Monitor operations
2. Field Dashboard: Log activities
3. Analytics: Make data-driven decisions

**Happy Tracking! 🐄**
