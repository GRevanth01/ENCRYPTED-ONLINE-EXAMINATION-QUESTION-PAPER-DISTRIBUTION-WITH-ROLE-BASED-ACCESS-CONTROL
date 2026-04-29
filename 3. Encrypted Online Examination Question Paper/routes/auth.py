from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from tinydb import Query
from datetime import datetime
import uuid

bp = Blueprint('auth', __name__)

def get_db():
    from app import users_table, logs_table
    return users_table, logs_table

def log_activity(user_id, user_type, action, details=""):
    _, logs_table = get_db()
    logs_table.insert({
        'id': str(uuid.uuid4()),
        'user_id': user_id,
        'user_type': user_type,
        'action': action,
        'details': details,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })


@bp.route('/home')
def home():
    return render_template('home.html')


@bp.route('/ea/signup', methods=['GET', 'POST'])
def ea_signup():
    if request.method == 'POST':
        users_table, _ = get_db()
        User = Query()
        
        email = request.form.get('email')
        employee_id = request.form.get('employee_id')
        
        if users_table.search((User.email == email) | (User.employee_id == employee_id)):
            flash('Email or Employee ID already exists!', 'error')
            return redirect(url_for('auth.ea_signup'))
        
        user_data = {
            'id': str(uuid.uuid4()),
            'full_name': request.form.get('full_name'),
            'email': email,
            'employee_id': employee_id,
            'department': request.form.get('department'),
            'designation': request.form.get('designation'),
            'contact_number': request.form.get('contact_number'),
            'office_location': request.form.get('office_location'),
            'password_hash': generate_password_hash(request.form.get('password')),
            'user_type': 'EA',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }
        
        users_table.insert(user_data)
        log_activity(user_data['id'], 'EA', 'SIGNUP', f"New EA registered: {email}")
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.ea_login'))
    
    return render_template('ea_signup.html')


@bp.route('/ea/login', methods=['GET', 'POST'])
def ea_login():
    if request.method == 'POST':
        users_table, _ = get_db()
        User = Query()
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users_table.search((User.email == email) & (User.user_type == 'EA'))
        
        if user and check_password_hash(user[0]['password_hash'], password):
            session['user_id'] = user[0]['id']
            session['user_type'] = 'EA'
            session['user_name'] = user[0]['full_name']
            session['user_email'] = user[0]['email']
            log_activity(user[0]['id'], 'EA', 'LOGIN', f"EA logged in: {email}")
            return redirect(url_for('ea.dashboard'))
        
        flash('Invalid email or password!', 'error')
    
    return render_template('ea_login.html')


@bp.route('/aef/signup', methods=['GET', 'POST'])
def aef_signup():
    if request.method == 'POST':
        users_table, _ = get_db()
        User = Query()
        
        email = request.form.get('email')
        faculty_id = request.form.get('faculty_id')
        
        if users_table.search((User.email == email) | (User.faculty_id == faculty_id)):
            flash('Email or Faculty ID already exists!', 'error')
            return redirect(url_for('auth.aef_signup'))
        
        user_data = {
            'id': str(uuid.uuid4()),
            'full_name': request.form.get('full_name'),
            'email': email,
            'faculty_id': faculty_id,
            'department': request.form.get('department'),
            'subject_expertise': request.form.get('subject_expertise'),
            'qualification': request.form.get('qualification'),
            'contact_number': request.form.get('contact_number'),
            'experience_years': request.form.get('experience_years'),
            'password_hash': generate_password_hash(request.form.get('password')),
            'user_type': 'AEF',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True,
            'is_authorized': False
        }
        
        users_table.insert(user_data)
        log_activity(user_data['id'], 'AEF', 'SIGNUP', f"New AEF registered: {email}")
        flash('Registration successful! Please login. Note: You need authorization from an Administrator to access exam papers.', 'success')
        return redirect(url_for('auth.aef_login'))
    
    return render_template('aef_signup.html')


@bp.route('/aef/login', methods=['GET', 'POST'])
def aef_login():
    if request.method == 'POST':
        users_table, _ = get_db()
        User = Query()
        
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = users_table.search((User.email == email) & (User.user_type == 'AEF'))
        
        if user and check_password_hash(user[0]['password_hash'], password):
            session['user_id'] = user[0]['id']
            session['user_type'] = 'AEF'
            session['user_name'] = user[0]['full_name']
            session['user_email'] = user[0]['email']
            log_activity(user[0]['id'], 'AEF', 'LOGIN', f"AEF logged in: {email}")
            return redirect(url_for('aef.dashboard'))
        
        flash('Invalid email or password!', 'error')
    
    return render_template('aef_login.html')


@bp.route('/logout')
def logout():
    user_id = session.get('user_id')
    user_type = session.get('user_type')
    if user_id:
        log_activity(user_id, user_type, 'LOGOUT', 'User logged out')
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.home'))
