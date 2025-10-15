# =============================================================================
# APPLICATION INTEGRATOR & PROJECT MANAGER
# Member 4: Application Integration & Project Management
# =============================================================================

from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, send_from_directory
import os
from datetime import datetime
import random

# Import modules from other team members
from auth_manager import (
    login_required, role_required, authenticate_user, 
    update_user_login, track_activity, get_user_data, 
    get_all_users, logout_user, LOGIN_HTML
)
from data_manager import (
    data_manager, load_mineral_data, get_all_countries, get_all_mining_sites,
    get_market_intelligence, get_investment_opportunities, get_platform_stats
)
from visualization_manager import (
    get_index_template, get_dashboard_template, get_admin_template
)

# Initialize Flask application
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management

# =============================================================================
# STATIC FILE HANDLING
# =============================================================================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images) from static directory"""
    return send_from_directory('static', filename)

# =============================================================================
# CORE APPLICATION ROUTES
# =============================================================================

@app.route('/')
def index():
    """Display the main landing page with project information"""
    return render_template_string(get_index_template())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication with credential validation"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = authenticate_user(username, password)
        if user:
            # Successful login
            session['username'] = username
            session['role'] = user['role']
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update last login time
            update_user_login(username)
            
            # Track login activity
            track_activity(f"User {username} logged in")
            
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_HTML, error="Invalid credentials")
    
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    """Clear user session and redirect to home page"""
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Display the main application dashboard with all features"""
    user_data = get_user_data(session['username'])
    track_activity("Accessed dashboard")
    
    return render_template_string(
        get_dashboard_template(), 
        minerals=load_mineral_data(),
        countries=get_all_countries(),
        mining_sites=get_all_mining_sites(),
        market_intelligence=get_market_intelligence(),
        investment_opportunities=get_investment_opportunities(),
        user_data=user_data
    )

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    """Display administrative control panel (admin only)"""
    user_data = get_user_data(session['username'])
    track_activity("Accessed admin panel")
    
    return render_template_string(
        get_admin_template(),
        users=get_all_users(),
        minerals=load_mineral_data(),
        countries=get_all_countries(),
        mining_sites=get_all_mining_sites(),
        user_data=user_data
    )

# =============================================================================
# RESTful API ENDPOINTS
# =============================================================================

@app.route('/api/minerals')
@login_required
def api_minerals():
    """API endpoint: Returns JSON data for all critical minerals"""
    track_activity("Accessed minerals API")
    return jsonify({
        "status": "success",
        "data": load_mineral_data(),
        "count": len(load_mineral_data()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/countries')
@login_required
def api_countries():
    """API endpoint: Returns JSON data for all African countries"""
    track_activity("Accessed countries API")
    return jsonify({
        "status": "success",
        "data": get_all_countries(),
        "count": len(get_all_countries()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/mining-sites')
@login_required
def api_mining_sites():
    """API endpoint: Returns JSON data for all mining sites"""
    track_activity("Accessed mining sites API")
    return jsonify({
        "status": "success",
        "data": get_all_mining_sites(),
        "count": len(get_all_mining_sites()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/market-intelligence')
@login_required
def api_market_intelligence():
    """API endpoint: Returns real-time market data and news"""
    track_activity("Accessed market intelligence API")
    return jsonify({
        "status": "success",
        "data": get_market_intelligence(),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/investment-opportunities')
@login_required
def api_investment_opportunities():
    """API endpoint: Returns investment projects (investor/admin only)"""
    user_role = get_user_data(session['username']).get('role')
    if user_role not in ['investor', 'admin']:
        return jsonify({"status": "error", "message": "Access denied"}), 403
    
    track_activity("Accessed investment opportunities API")
    return jsonify({
        "status": "success",
        "data": get_investment_opportunities(),
        "count": len(get_investment_opportunities()),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/mineral/<int:mineral_id>')
@login_required
def api_mineral(mineral_id):
    """API endpoint: Returns detailed data for a specific mineral by ID"""
    mineral = data_manager.get_mineral_by_id(mineral_id)
    if mineral:
        track_activity(f"Accessed mineral data: {mineral['name']}")
        return jsonify({
            "status": "success",
            "data": mineral,
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"status": "error", "message": "Mineral not found"}), 404

@app.route('/api/country/<int:country_id>')
@login_required
def api_country(country_id):
    """API endpoint: Returns detailed profile for a specific country by ID"""
    country = data_manager.get_country_by_id(country_id)
    if country:
        track_activity(f"Accessed country data: {country['name']}")
        return jsonify({
            "status": "success",
            "data": country,
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"status": "error", "message": "Country not found"}), 404

@app.route('/api/mining-site/<int:site_id>')
@login_required
def api_mining_site(site_id):
    """API endpoint: Returns detailed data for a specific mining site by ID"""
    site = data_manager.get_mining_site_by_id(site_id)
    if site:
        track_activity(f"Accessed mining site data: {site['name']}")
        return jsonify({
            "status": "success",
            "data": site,
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"status": "error", "message": "Mining site not found"}), 404

@app.route('/api/search/minerals/<query>')
@login_required
def api_search_minerals(query):
    """API endpoint: Search minerals by name, description, or applications"""
    results = data_manager.search_minerals(query)
    track_activity(f"Searched minerals for: {query}")
    return jsonify({
        "status": "success",
        "query": query,
        "results": results,
        "count": len(results),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint: Returns comprehensive platform statistics"""
    track_activity("Accessed platform statistics")
    return jsonify({
        "status": "success",
        "data": get_platform_stats(),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/user-activity')
@login_required
@role_required('admin')
def api_user_activity():
    """API endpoint: Returns activity tracking data (admin only)"""
    track_activity("Accessed user activity API")
    return jsonify({
        "status": "success",
        "data": session.get('user_activity', []),
        "timestamp": datetime.now().isoformat()
    })

# =============================================================================
# ERROR HANDLERS
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({
        "status": "error",
        "message": "Resource not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "status": "error", 
        "message": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

@app.errorhandler(403)
def forbidden_error(error):
    """Handle 403 errors"""
    return jsonify({
        "status": "error",
        "message": "Access forbidden",
        "timestamp": datetime.now().isoformat()
    }), 403

# =============================================================================
# APPLICATION STARTUP AND MANAGEMENT
# =============================================================================

class ApplicationManager:
    """Manager for application startup and configuration"""
    
    def __init__(self, flask_app):
        self.app = flask_app
        self.port = 8080
        self.host = '0.0.0.0'
        self.debug = True
    
    def display_startup_info(self):
        """Display comprehensive startup information"""
        print("=" * 70)
        print("🏔️  African Critical Minerals Platform - Group 34")
        print("MINN2020A Project 2025 - University of the Witwatersrand")
        print("=" * 70)
        print("\n🚀 Starting Enhanced Flask application...")
        print("📊 Available data:")
        print(f"   • {len(load_mineral_data())} critical minerals (enhanced with market data)")
        print(f"   • {len(get_all_countries())} African countries (enhanced with risk profiles)")
        print(f"   • {len(get_all_mining_sites())} mining sites (enhanced with operational data)")
        print(f"   • {len(get_all_users())} user accounts")
        print(f"   • {len(get_market_intelligence()['market_news'])} market news items")
        print(f"   • {len(get_investment_opportunities())} investment opportunities")
        print("\n🔑 Demo Login Credentials:")
        for username, user in get_all_users().items():
            print(f"   • {username} ({user['role']}) - Password: {user['password']}")
        print("\n🌟 NEW ENHANCED FEATURES:")
        print("   • Market Intelligence Dashboard")
        print("   • Investment Opportunities (Role-based)")
        print("   • User Activity Tracking")
        print("   • Enhanced Mineral & Country Profiles")
        print("   • Session Timer & Quick Stats")
        print("   • Additional API Endpoints")
        print("\n🌐 Application will be available at: http://localhost:8080")
        print("🗺️  Interactive map with enhanced data visualization!")
        print("🎯 Smart features for investors, researchers, and administrators!")
        print("=" * 70)
    
    def run_application(self):
        """Start the Flask application"""
        self.display_startup_info()
        self.app.run(
            debug=self.debug, 
            host=self.host, 
            port=self.port,
            threaded=True
        )
    
    def get_application_status(self):
        """Get current application status"""
        return {
            "status": "running",
            "port": self.port,
            "host": self.host,
            "debug_mode": self.debug,
            "data_loaded": {
                "minerals": len(load_mineral_data()),
                "countries": len(get_all_countries()),
                "mining_sites": len(get_all_mining_sites()),
                "users": len(get_all_users())
            },
            "timestamp": datetime.now().isoformat()
        }

# Create application manager instance
app_manager = ApplicationManager(app)

# =============================================================================
# MAIN EXECUTION BLOCK
# =============================================================================

if __name__ == '__main__':
    """Application entry point - starts the Flask development server"""
    app_manager.run_application()
    