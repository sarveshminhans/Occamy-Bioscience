from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'occamy-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///occamy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ============== MODELS ==============

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'field_officer'
    name = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50))
    district = db.Column(db.String(50))
    phone = db.Column(db.String(15))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    work_logs = db.relationship('WorkLog', backref='user', lazy=True)
    meetings = db.relationship('Meeting', backref='user', lazy=True)
    samples = db.relationship('SampleDistribution', backref='user', lazy=True)
    sales = db.relationship('Sale', backref='user', lazy=True)

class WorkLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    start_location_lat = db.Column(db.Float)
    start_location_lng = db.Column(db.Float)
    end_location_lat = db.Column(db.Float)
    end_location_lng = db.Column(db.Float)
    odometer_start = db.Column(db.Float)
    odometer_end = db.Column(db.Float)
    distance_traveled = db.Column(db.Float)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='started')  # started, ended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meeting_type = db.Column(db.String(20), nullable=False)  # 'one_on_one' or 'group'
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # One-on-One fields
    person_name = db.Column(db.String(100))
    person_category = db.Column(db.String(20))  # Farmer, Seller, Influencer
    contact_number = db.Column(db.String(15))
    business_potential = db.Column(db.String(50))
    
    # Group meeting fields
    village = db.Column(db.String(100))
    attendees_count = db.Column(db.Integer)
    group_meeting_type = db.Column(db.String(50))
    
    # Common fields
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    location_name = db.Column(db.String(200))
    notes = db.Column(db.Text)
    photos = db.Column(db.Text)  # JSON array of photo URLs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SampleDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_type = db.Column(db.String(50))  # Farmer, Distributor, etc.
    product_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))  # kg, gm, pieces
    purpose = db.Column(db.String(100))  # trial, demo, follow-up
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    location_name = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    sale_type = db.Column(db.String(10), nullable=False)  # B2C or B2B
    customer_name = db.Column(db.String(100), nullable=False)
    customer_type = db.Column(db.String(50))  # Farmer, Distributor, Reseller
    contact_number = db.Column(db.String(15))
    product_sku = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    pack_size = db.Column(db.String(50))
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    mode = db.Column(db.String(20))  # direct, via_distributor
    is_repeat_order = db.Column(db.Boolean, default=False)
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    location_name = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LocationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    accuracy = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    activity_type = db.Column(db.String(50))  # tracking, meeting, sale, etc.

# ============== HELPER FUNCTIONS ==============

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def field_officer_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'field_officer':
            return jsonify({'error': 'Field officer access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# ============== ROUTES ==============

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('field_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and check_password_hash(user.password_hash, data.get('password')):
            if not user.is_active:
                return jsonify({'error': 'Account is deactivated'}), 403
            login_user(user)
            return jsonify({
                'success': True,
                'role': user.role,
                'redirect': url_for('admin_dashboard') if user.role == 'admin' else url_for('field_dashboard')
            })
        return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# ============== ADMIN ROUTES ==============

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/api/admin/stats')
@login_required
@admin_required
def admin_stats():
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Active field officers today
    active_officers = WorkLog.query.filter(
        WorkLog.date == today,
        WorkLog.status == 'started'
    ).count()
    
    # Total meetings this month
    total_meetings = Meeting.query.filter(
        Meeting.date >= datetime.combine(month_ago, datetime.min.time())
    ).count()
    
    # Total sales this month
    total_sales = Sale.query.filter(
        Sale.date >= datetime.combine(month_ago, datetime.min.time())
    ).count()
    
    # Total distance traveled this month
    total_distance = db.session.query(db.func.sum(WorkLog.distance_traveled)).filter(
        WorkLog.date >= month_ago
    ).scalar() or 0
    
    # Sales by type
    b2c_sales = Sale.query.filter(
        Sale.date >= datetime.combine(month_ago, datetime.min.time()),
        Sale.sale_type == 'B2C'
    ).count()
    
    b2b_sales = Sale.query.filter(
        Sale.date >= datetime.combine(month_ago, datetime.min.time()),
        Sale.sale_type == 'B2B'
    ).count()
    
    # State-wise activity
    state_activity = db.session.query(
        User.state,
        db.func.count(Meeting.id).label('meetings'),
        db.func.count(Sale.id).label('sales')
    ).outerjoin(Meeting).outerjoin(Sale).filter(
        User.role == 'field_officer'
    ).group_by(User.state).all()
    
    return jsonify({
        'active_officers': active_officers,
        'total_meetings': total_meetings,
        'total_sales': total_sales,
        'total_distance': round(total_distance, 2),
        'b2c_sales': b2c_sales,
        'b2b_sales': b2b_sales,
        'state_activity': [{'state': s[0], 'meetings': s[1], 'sales': s[2]} for s in state_activity]
    })

@app.route('/api/admin/users')
@login_required
@admin_required
def get_users():
    users = User.query.filter_by(role='field_officer').all()
    return jsonify([{
        'id': u.id,
        'name': u.name,
        'username': u.username,
        'email': u.email,
        'phone': u.phone,
        'state': u.state,
        'district': u.district,
        'is_active': u.is_active,
        'created_at': u.created_at.isoformat()
    } for u in users])

@app.route('/api/admin/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    data = request.get_json()
    
    # Check if username or email exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role='field_officer',
        name=data['name'],
        state=data.get('state'),
        district=data.get('district'),
        phone=data.get('phone')
    )
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'success': True, 'user_id': user.id})

@app.route('/api/admin/activities')
@login_required
@admin_required
def get_activities():
    days = request.args.get('days', 7, type=int)
    user_id = request.args.get('user_id', type=int)
    
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.session.query(
        User.name,
        User.state,
        WorkLog.date,
        WorkLog.distance_traveled,
        db.func.count(Meeting.id).label('meetings_count'),
        db.func.count(Sale.id).label('sales_count')
    ).join(User).outerjoin(Meeting, db.and_(
        Meeting.user_id == WorkLog.user_id,
        db.func.date(Meeting.date) == WorkLog.date
    )).outerjoin(Sale, db.and_(
        Sale.user_id == WorkLog.user_id,
        db.func.date(Sale.date) == WorkLog.date
    )).filter(WorkLog.date >= start_date.date())
    
    if user_id:
        query = query.filter(WorkLog.user_id == user_id)
    
    results = query.group_by(User.name, User.state, WorkLog.date, WorkLog.distance_traveled).all()
    
    return jsonify([{
        'name': r[0],
        'state': r[1],
        'date': r[2].isoformat(),
        'distance': r[3] or 0,
        'meetings': r[4],
        'sales': r[5]
    } for r in results])

@app.route('/api/admin/meetings')
@login_required
@admin_required
def get_all_meetings():
    meetings = Meeting.query.join(User).order_by(Meeting.date.desc()).limit(100).all()
    return jsonify([{
        'id': m.id,
        'officer_name': m.user.name,
        'type': m.meeting_type,
        'date': m.date.isoformat(),
        'person_name': m.person_name,
        'category': m.person_category,
        'village': m.village,
        'attendees': m.attendees_count,
        'location': m.location_name,
        'business_potential': m.business_potential
    } for m in meetings])

@app.route('/api/admin/sales')
@login_required
@admin_required
def get_all_sales():
    sales = Sale.query.join(User).order_by(Sale.date.desc()).limit(100).all()
    return jsonify([{
        'id': s.id,
        'officer_name': s.user.name,
        'date': s.date.isoformat(),
        'type': s.sale_type,
        'customer': s.customer_name,
        'product': s.product_name,
        'quantity': s.quantity,
        'amount': s.total_amount,
        'location': s.location_name,
        'repeat_order': s.is_repeat_order
    } for s in sales])

# ============== FIELD OFFICER ROUTES ==============

@app.route('/field/dashboard')
@login_required
@field_officer_required
def field_dashboard():
    return render_template('field_dashboard.html')

@app.route('/api/field/worklog/start', methods=['POST'])
@login_required
@field_officer_required
def start_work():
    data = request.get_json()
    today = datetime.utcnow().date()
    
    # Check if already started today
    existing = WorkLog.query.filter_by(
        user_id=current_user.id,
        date=today,
        status='started'
    ).first()
    
    if existing:
        return jsonify({'error': 'Work already started today'}), 400
    
    work_log = WorkLog(
        user_id=current_user.id,
        date=today,
        start_time=datetime.utcnow(),
        start_location_lat=data.get('latitude'),
        start_location_lng=data.get('longitude'),
        odometer_start=data.get('odometer'),
        notes=data.get('notes')
    )
    db.session.add(work_log)
    db.session.commit()
    
    return jsonify({'success': True, 'worklog_id': work_log.id})

@app.route('/api/field/worklog/end', methods=['POST'])
@login_required
@field_officer_required
def end_work():
    data = request.get_json()
    today = datetime.utcnow().date()
    
    work_log = WorkLog.query.filter_by(
        user_id=current_user.id,
        date=today,
        status='started'
    ).first()
    
    if not work_log:
        return jsonify({'error': 'No active work session found'}), 400
    
    work_log.end_time = datetime.utcnow()
    work_log.end_location_lat = data.get('latitude')
    work_log.end_location_lng = data.get('longitude')
    work_log.odometer_end = data.get('odometer')
    work_log.status = 'ended'
    
    if work_log.odometer_start and work_log.odometer_end:
        work_log.distance_traveled = work_log.odometer_end - work_log.odometer_start
    
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/field/worklog/status')
@login_required
@field_officer_required
def worklog_status():
    today = datetime.utcnow().date()
    work_log = WorkLog.query.filter_by(
        user_id=current_user.id,
        date=today
    ).first()
    
    if not work_log:
        return jsonify({'status': 'not_started'})
    
    return jsonify({
        'status': work_log.status,
        'start_time': work_log.start_time.isoformat() if work_log.start_time else None,
        'end_time': work_log.end_time.isoformat() if work_log.end_time else None
    })

@app.route('/api/field/meeting', methods=['POST'])
@login_required
@field_officer_required
def create_meeting():
    data = request.get_json()
    
    meeting = Meeting(
        user_id=current_user.id,
        meeting_type=data['meeting_type'],
        date=datetime.utcnow(),
        person_name=data.get('person_name'),
        person_category=data.get('person_category'),
        contact_number=data.get('contact_number'),
        business_potential=data.get('business_potential'),
        village=data.get('village'),
        attendees_count=data.get('attendees_count'),
        group_meeting_type=data.get('group_meeting_type'),
        location_lat=data.get('latitude'),
        location_lng=data.get('longitude'),
        location_name=data.get('location_name'),
        notes=data.get('notes'),
        photos=json.dumps(data.get('photos', []))
    )
    db.session.add(meeting)
    db.session.commit()
    
    return jsonify({'success': True, 'meeting_id': meeting.id})

@app.route('/api/field/sample', methods=['POST'])
@login_required
@field_officer_required
def create_sample():
    data = request.get_json()
    
    sample = SampleDistribution(
        user_id=current_user.id,
        date=datetime.utcnow(),
        recipient_name=data['recipient_name'],
        recipient_type=data.get('recipient_type'),
        product_name=data['product_name'],
        quantity=data['quantity'],
        unit=data.get('unit', 'kg'),
        purpose=data.get('purpose'),
        location_lat=data.get('latitude'),
        location_lng=data.get('longitude'),
        location_name=data.get('location_name'),
        notes=data.get('notes')
    )
    db.session.add(sample)
    db.session.commit()
    
    return jsonify({'success': True, 'sample_id': sample.id})

@app.route('/api/field/sale', methods=['POST'])
@login_required
@field_officer_required
def create_sale():
    data = request.get_json()
    
    sale = Sale(
        user_id=current_user.id,
        date=datetime.utcnow(),
        sale_type=data['sale_type'],
        customer_name=data['customer_name'],
        customer_type=data.get('customer_type'),
        contact_number=data.get('contact_number'),
        product_sku=data['product_sku'],
        product_name=data['product_name'],
        pack_size=data.get('pack_size'),
        quantity=data['quantity'],
        unit_price=data.get('unit_price'),
        total_amount=data.get('total_amount'),
        mode=data.get('mode'),
        is_repeat_order=data.get('is_repeat_order', False),
        location_lat=data.get('latitude'),
        location_lng=data.get('longitude'),
        location_name=data.get('location_name'),
        notes=data.get('notes')
    )
    db.session.add(sale)
    db.session.commit()
    
    return jsonify({'success': True, 'sale_id': sale.id})

@app.route('/api/field/location', methods=['POST'])
@login_required
@field_officer_required
def log_location():
    data = request.get_json()
    
    location = LocationLog(
        user_id=current_user.id,
        latitude=data['latitude'],
        longitude=data['longitude'],
        accuracy=data.get('accuracy'),
        activity_type=data.get('activity_type', 'tracking')
    )
    db.session.add(location)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/field/my-activities')
@login_required
@field_officer_required
def my_activities():
    days = request.args.get('days', 7, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    meetings = Meeting.query.filter(
        Meeting.user_id == current_user.id,
        Meeting.date >= start_date
    ).count()
    
    sales = Sale.query.filter(
        Sale.user_id == current_user.id,
        Sale.date >= start_date
    ).count()
    
    samples = SampleDistribution.query.filter(
        SampleDistribution.user_id == current_user.id,
        SampleDistribution.date >= start_date
    ).count()
    
    distance = db.session.query(db.func.sum(WorkLog.distance_traveled)).filter(
        WorkLog.user_id == current_user.id,
        WorkLog.date >= start_date.date()
    ).scalar() or 0
    
    return jsonify({
        'meetings': meetings,
        'sales': sales,
        'samples': samples,
        'distance': round(distance, 2)
    })

# ============== INITIALIZATION ==============

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create default admin if doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@occamy.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                name='System Administrator'
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username='admin', password='admin123'")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
