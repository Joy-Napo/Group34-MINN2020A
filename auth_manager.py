# =============================================================================
# AUTHENTICATION & SECURITY MANAGER
# Thatoyaone: Authentication & Security System
# =============================================================================

from flask import session, redirect, url_for
from functools import wraps
from datetime import datetime

# User database with enhanced security features
USERS = {
    "admin01": {
        "password": "hash123", 
        "role": "admin", 
        "name": "System Administrator", 
        "last_login": None,
        "email": "admin@chronominerals.com",
        "created_at": "2024-01-01"
    },
    "investor01": {
        "password": "hash456", 
        "role": "investor", 
        "name": "Investment Analyst", 
        "last_login": None,
        "email": "investor@chronominerals.com",
        "created_at": "2024-01-01"
    },
    "research01": {
        "password": "hash789", 
        "role": "researcher", 
        "name": "Research Specialist", 
        "last_login": None,
        "email": "research@chronominerals.com",
        "created_at": "2024-01-01"
    }
}

# Session configuration
SESSION_CONFIG = {
    'timeout_minutes': 60,
    'max_activities': 20,
    'secure_cookies': True
}

def login_required(f):
    """Decorator to ensure user is logged in before accessing protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        
        # Check session timeout
        if is_session_expired():
            logout_user()
            return redirect(url_for('login'))
            
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """Decorator for role-based access control with enhanced security"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('login'))
            
            user_role = USERS.get(session['username'], {}).get('role')
            if user_role != role and user_role != 'admin':
                track_activity(f"Access denied for {session['username']} to {role}-restricted resource")
                return "Access denied: Insufficient permissions", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def authenticate_user(username, password):
    """Enhanced user authentication with validation"""
    user = USERS.get(username)
    if user and user['password'] == password:
        return user
    return None

def update_user_login(username):
    """Update user's last login time and session data"""
    if username in USERS:
        USERS[username]['last_login'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        session['login_time'] = USERS[username]['last_login']

def track_activity(activity_description):
    """Enhanced activity tracking with session management"""
    if 'username' in session:
        user_activity = session.get('user_activity', [])
        user_activity.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activity': activity_description,
            'username': session['username'],
            'role': session.get('role', 'unknown')
        })
        # Keep only the most recent activities
        session['user_activity'] = user_activity[-SESSION_CONFIG['max_activities']:]

def get_user_data(username):
    """Get user data by username with privacy protection"""
    user = USERS.get(username)
    if user:
        # Return copy without sensitive data
        return {
            'username': username,
            'role': user['role'],
            'name': user['name'],
            'last_login': user['last_login']
        }
    return None

def get_all_users():
    """Get all users data for admin purposes"""
    return USERS

def logout_user():
    """Enhanced logout with comprehensive session cleanup"""
    if 'username' in session:
        track_activity(f"User {session['username']} logged out")
    session.clear()

def is_session_expired():
    """Check if user session has expired"""
    login_time = session.get('login_time')
    if not login_time:
        return True
    
    login_dt = datetime.strptime(login_time, '%Y-%m-%d %H:%M:%S')
    session_duration = datetime.now() - login_dt
    return session_duration.total_seconds() > SESSION_CONFIG['timeout_minutes'] * 60

def get_user_permissions(role):
    """Get permissions for different user roles"""
    permissions = {
        'admin': ['read', 'write', 'delete', 'manage_users', 'view_reports'],
        'investor': ['read', 'export_data', 'view_investments', 'view_market_data'],
        'researcher': ['read', 'export_data', 'view_reports']
    }
    return permissions.get(role, ['read'])

# HTML Template for login (kept here for authentication context)
LOGIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - African Critical Minerals Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0; line-height: 1.6; padding: 20px; min-height: 100vh;
        }
        .container {
            max-width: 500px; margin: 0 auto;
            background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(10px);
            border-radius: 20px; padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }
        header { text-align: center; margin-bottom: 40px; padding-bottom: 20px; border-bottom: 2px solid rgba(59, 130, 246, 0.3); }
        h1 {
            font-size: 2.5em; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
            margin-bottom: 10px; font-weight: bold;
        }
        .subtitle { font-size: 1.1em; color: #94a3b8; margin-bottom: 20px; }
        .section {
            margin-bottom: 30px; padding: 25px; background: rgba(15, 23, 42, 0.5);
            border-radius: 15px; border-left: 4px solid #3b82f6;
        }
        .form-control {
            background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(59, 130, 246, 0.3);
            color: #e2e8f0; padding: 12px;
        }
        .form-control:focus {
            background: rgba(15, 23, 42, 0.9); border-color: #3b82f6; color: #e2e8f0;
            box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.25);
        }
        .form-label { color: #93c5fd; font-weight: 600; margin-bottom: 8px; }
        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border: none; padding: 12px; font-weight: bold; width: 100%;
        }
        .btn-primary:hover { background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%); transform: translateY(-2px); }
        .alert { border: none; border-left: 4px solid #dc3545; background: rgba(220, 53, 69, 0.1); color: #f8d7da; }
        .table { color: #e2e8f0; }
        .table-dark { background: rgba(15, 23, 42, 0.7); }
        footer { text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid rgba(59, 130, 246, 0.3); color: #94a3b8; }
        .badge {
            display: inline-block; background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white; padding: 8px 20px; border-radius: 20px; font-weight: bold; margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🔐 Login</h1>
            <p class="subtitle">Access the African Critical Minerals Platform</p>
            <div class="badge">Group 34 | MINN2020A</div>
        </header>

        <div class="section">
            {% if error %}
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle"></i> {{ error }}
            </div>
            {% endif %}

            <form method="POST">
                <div class="mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input type="text" class="form-control" id="username" name="username" required>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Password</label>
                    <input type="password" class="form-control" id="password" name="password" required>
                </div>
                <button type="submit" class="btn btn-primary">Login</button>
            </form>

            <div class="mt-4">
                <h5 style="color: #93c5fd; margin-bottom: 15px;">Demo Credentials:</h5>
                <table class="table table-dark table-sm">
                    <thead><tr><th>Role</th><th>Username</th><th>Password</th></tr></thead>
                    <tbody>
                        <tr><td>Administrator</td><td><code>admin01</code></td><td><code>hash123</code></td></tr>
                        <tr><td>Investor</td><td><code>investor01</code></td><td><code>hash456</code></td></tr>
                        <tr><td>Researcher</td><td><code>research01</code></td><td><code>hash789</code></td></tr>
                    </tbody>
                </table>
            </div>
        </div>

        <footer>
            <p><strong>African Critical Minerals Platform</strong></p>
            <p>Group 34 | MINN2020A Project 2025</p>
        </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''
  


       


   


 

   
          
                    
      
   
