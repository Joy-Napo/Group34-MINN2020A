 # app.py - African Critical Minerals Platform with Enhanced Features
# Group 34 | MINN2020A Project 2025

"""
MAIN APPLICATION FILE
----------------------
A comprehensive Flask web application for African critical minerals data.
Features include user authentication, interactive data visualization, 
market intelligence, and RESTful APIs.
"""

from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, send_from_directory
from functools import wraps
import os
import json
from datetime import datetime, timedelta
import random


# FLASK APPLICATION INITIALISATION


app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key for session management


# DATABASE


MINERALS = [
    {
        "id": 1,
        "name": "Cobalt",
        "description": "Essential for rechargeable batteries and superalloys",
        "price": 52000,
        "unit": "USD/tonne",
        "trend": "increasing",
        "reserves": "7.1 million tonnes",
        "production": "170,000 tonnes/year",
        "major_producers": ["DRC", "Russia", "Australia"],
        "demand_growth": "12% YoY",
        "applications": ["EV Batteries", "Aerospace", "Medical Devices"],
        "risk_factors": ["Supply Chain", "Geopolitical", "Environmental"]
    },
    {
        "id": 2,
        "name": "Lithium",
        "description": "Critical for lithium-ion batteries in electric vehicles",
        "price": 18000,
        "unit": "USD/tonne",
        "trend": "stable",
        "reserves": "21 million tonnes",
        "production": "100,000 tonnes/year",
        "major_producers": ["Australia", "Chile", "China"],
        "demand_growth": "18% YoY",
        "applications": ["EV Batteries", "Energy Storage", "Consumer Electronics"],
        "risk_factors": ["Water Usage", "Price Volatility", "Processing"]
    },
    {
        "id": 3,
        "name": "Graphite",
        "description": "Used in batteries and high-temperature applications",
        "price": 2500,
        "unit": "USD/tonne",
        "trend": "increasing",
        "reserves": "320 million tonnes",
        "production": "1.1 million tonnes/year",
        "major_producers": ["China", "Mozambique", "Brazil"],
        "demand_growth": "8% YoY",
        "applications": ["Anode Material", "Refractories", "Lubricants"],
        "risk_factors": ["Chinese Dominance", "Processing Costs", "Quality Variance"]
    },
    {
        "id": 4,
        "name": "Manganese",
        "description": "Essential for steel production and batteries",
        "price": 4200,
        "unit": "USD/tonne",
        "trend": "stable",
        "reserves": "1.3 billion tonnes",
        "production": "20 million tonnes/year",
        "major_producers": ["South Africa", "Australia", "Gabon"],
        "demand_growth": "6% YoY",
        "applications": ["Steel Production", "Batteries", "Fertilizers"],
        "risk_factors": ["Steel Demand", "Logistics", "Infrastructure"]
    }
]

COUNTRIES = [
    {
        "id": 1,
        "name": "Democratic Republic of Congo",
        "capital": "Kinshasa",
        "gdp": "49.87 billion USD",
        "population": "95.89 million",
        "mining_contribution": "25% of GDP",
        "key_minerals": ["Cobalt", "Copper", "Diamonds", "Gold"],
        "mining_employment": "2 million+",
        "investment_rating": "B-",
        "coordinates": {"lat": -4.0383, "lng": 21.7587},
        "area": "2,344,858 km²",
        "mining_regulations": "Moderate",
        "infrastructure": "Developing",
        "political_stability": "Medium Risk"
    },
    {
        "id": 2,
        "name": "South Africa",
        "capital": "Pretoria",
        "gdp": "405.71 billion USD",
        "population": "60.14 million",
        "mining_contribution": "8% of GDP",
        "key_minerals": ["Platinum", "Gold", "Manganese", "Chromium"],
        "mining_employment": "460,000",
        "investment_rating": "BB-",
        "coordinates": {"lat": -30.5595, "lng": 22.9375},
        "area": "1,221,037 km²",
        "mining_regulations": "Established",
        "infrastructure": "Developed",
        "political_stability": "Medium Risk"
    },
    {
        "id": 3,
        "name": "Mozambique",
        "capital": "Maputo",
        "gdp": "15.78 billion USD",
        "population": "32.16 million",
        "mining_contribution": "5% of GDP",
        "key_minerals": ["Graphite", "Coal", "Titanium", "Ruby"],
        "mining_employment": "45,000",
        "investment_rating": "CCC+",
        "coordinates": {"lat": -18.6657, "lng": 35.5296},
        "area": "801,590 km²",
        "mining_regulations": "Developing",
        "infrastructure": "Basic",
        "political_stability": "High Risk"
    },
    {
        "id": 4,
        "name": "Namibia",
        "capital": "Windhoek",
        "gdp": "12.31 billion USD",
        "population": "2.55 million",
        "mining_contribution": "12% of GDP",
        "key_minerals": ["Uranium", "Diamonds", "Lithium", "Copper"],
        "mining_employment": "16,000",
        "investment_rating": "BB",
        "coordinates": {"lat": -22.9576, "lng": 18.4904},
        "area": "825,615 km²",
        "mining_regulations": "Established",
        "infrastructure": "Good",
        "political_stability": "Low Risk"
    }
]

MINING_SITES = [
    {
        "id": 1,
        "name": "Tenke Fungurume Mine",
        "country": "Democratic Republic of Congo",
        "mineral": "Cobalt",
        "lat": -10.5833,
        "lng": 26.5167,
        "production": "20,000 tonnes/year",
        "operator": "China Molybdenum",
        "reserves": "150 million tonnes",
        "status": "Active",
        "employment": "5,000",
        "year_established": 2009,
        "estimated_lifespan": "25 years",
        "environmental_rating": "B"
    },
    {
        "id": 2,
        "name": "Kalahari Manganese Field",
        "country": "South Africa",
        "mineral": "Manganese",
        "lat": -27.4667,
        "lng": 23.0833,
        "production": "5.3 million tonnes/year",
        "operator": "South32 & Assmang",
        "reserves": "450 million tonnes",
        "status": "Active",
        "employment": "8,000",
        "year_established": 1970,
        "estimated_lifespan": "40 years",
        "environmental_rating": "A-"
    },
    {
        "id": 3,
        "name": "Balama Graphite Project",
        "country": "Mozambique",
        "mineral": "Graphite",
        "lat": -13.2500,
        "lng": 38.8333,
        "production": "350,000 tonnes/year",
        "operator": "Syrah Resources",
        "reserves": "118 million tonnes",
        "status": "Active",
        "employment": "1,200",
        "year_established": 2018,
        "estimated_lifespan": "50 years",
        "environmental_rating": "B+"
    },
    {
        "id": 4,
        "name": "Uis Tin Mine & Lithium Project",
        "country": "Namibia",
        "mineral": "Lithium",
        "lat": -21.2333,
        "lng": 14.8667,
        "production": "5,000 tonnes/year",
        "operator": "Andrada Mining",
        "reserves": "71 million tonnes",
        "status": "Active",
        "employment": "800",
        "year_established": 1920,
        "estimated_lifespan": "30 years",
        "environmental_rating": "A"
    }
]

MARKET_INTELLIGENCE = {
    "price_trends": [
        {"mineral": "Cobalt", "current_price": 52000, "change_percentage": 5.2, "trend": "up"},
        {"mineral": "Lithium", "current_price": 18000, "change_percentage": -1.8, "trend": "down"},
        {"mineral": "Graphite", "current_price": 2500, "change_percentage": 2.1, "trend": "up"},
        {"mineral": "Manganese", "current_price": 4200, "change_percentage": 0.5, "trend": "stable"}
    ],
    "market_news": [
        {
            "title": "DRC Announces New Mining Regulations",
            "summary": "New environmental standards expected to impact cobalt production",
            "date": "2024-01-15",
            "impact": "medium"
        },
        {
            "title": "Electric Vehicle Demand Drives Lithium Prices",
            "summary": "Global EV sales growth continues to fuel lithium demand",
            "date": "2024-01-12",
            "impact": "high"
        },
        {
            "title": "Mozambique Infrastructure Improvements",
            "summary": "New port facilities to boost graphite export capacity",
            "date": "2024-01-10",
            "impact": "low"
        }
    ]
}

INVESTMENT_OPPORTUNITIES = [
    {
        "id": 1,
        "title": "Greenfield Lithium Project",
        "country": "Namibia",
        "mineral": "Lithium",
        "investment_required": "USD 150M",
        "estimated_roi": "22%",
        "risk_level": "Medium",
        "timeline": "3-5 years",
        "status": "Feasibility"
    },
    {
        "id": 2,
        "title": "Cobalt Processing Facility",
        "country": "DRC",
        "mineral": "Cobalt",
        "investment_required": "USD 80M",
        "estimated_roi": "18%",
        "risk_level": "High",
        "timeline": "2-3 years",
        "status": "Planning"
    },
    {
        "id": 3,
        "title": "Graphite Expansion Project",
        "country": "Mozambique",
        "mineral": "Graphite",
        "investment_required": "USD 45M",
        "estimated_roi": "15%",
        "risk_level": "Low",
        "timeline": "1-2 years",
        "status": "Approved"
    }
]

USERS = {
    "admin01": {"password": "hash123", "role": "admin", "name": "System Administrator", "last_login": None},
    "investor01": {"password": "hash456", "role": "investor", "name": "Investment Analyst", "last_login": None},
    "research01": {"password": "hash789", "role": "researcher", "name": "Research Specialist", "last_login": None}
}

# =============================================================================
# AUTHENTICATION & AUTHORIZATION SYSTEM
# =============================================================================

def login_required(f):
    """Decorator to ensure user is logged in before accessing protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(role):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('login'))
            user_role = USERS.get(session['username'], {}).get('role')
            if user_role != role and user_role != 'admin':
                return "Access denied: Insufficient permissions", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def track_activity(activity_description):
    """Track user activities in session for monitoring"""
    if 'username' in session:
        user_activity = session.get('user_activity', [])
        user_activity.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'activity': activity_description
        })
        session['user_activity'] = user_activity[-10:]


# STATIC FILE HANDLING


@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, images) from static directory"""
    return send_from_directory('static', filename)


# HTML TEMPLATES 


INDEX_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>African Critical Minerals Platform - Group 34</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        }

        h1 {
            font-size: 3em;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 1.2em;
            color: #94a3b8;
            margin-bottom: 20px;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 10px;
        }

        .section {
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
        }

        h2 {
            color: #60a5fa;
            font-size: 2em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3 {
            color: #93c5fd;
            font-size: 1.5em;
            margin: 25px 0 15px 0;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .feature-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }

        .feature-card h4 {
            color: #60a5fa;
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        .feature-card p {
            color: #cbd5e1;
            font-size: 0.95em;
        }

        .credentials-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 10px;
            overflow: hidden;
        }

        .credentials-table th,
        .credentials-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        }

        .credentials-table th {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            font-weight: bold;
        }

        .credentials-table tr:last-child td {
            border-bottom: none;
        }

        .credentials-table code {
            background: rgba(59, 130, 246, 0.2);
            padding: 5px 10px;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            color: #93c5fd;
        }

        .url-box {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
            border: 2px solid rgba(59, 130, 246, 0.4);
        }

        .url-box a {
            color: #60a5fa;
            text-decoration: none;
            font-size: 1.3em;
            font-weight: bold;
            transition: color 0.3s ease;
        }

        .url-box a:hover {
            color: #93c5fd;
        }

        .checklist {
            list-style: none;
            padding: 0;
        }

        .checklist li {
            padding: 12px 15px;
            margin: 10px 0;
            background: rgba(34, 197, 94, 0.1);
            border-left: 4px solid #22c55e;
            border-radius: 5px;
        }

        .checklist li::before {
            content: "✅ ";
            margin-right: 10px;
        }

        .highlight-box {
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
            padding: 25px;
            border-radius: 12px;
            margin: 20px 0;
            border: 1px solid rgba(139, 92, 246, 0.4);
        }

        .icon {
            font-size: 1.5em;
            margin-right: 10px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #60a5fa;
            display: block;
        }

        .stat-card .label {
            color: #94a3b8;
            font-size: 0.9em;
            margin-top: 5px;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid rgba(59, 130, 246, 0.3);
            color: #94a3b8;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border: none;
            padding: 12px 30px;
            font-weight: bold;
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            transform: translateY(-2px);
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }

            .container {
                padding: 20px;
            }

            .feature-grid,
            .stats-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏔️ African Critical Minerals Platform</h1>
            <p class="subtitle">Strategic Intelligence Platform for African Mineral Resources</p>
            <div class="badge">Group 34 | MINN2020A Project 2025</div>
        </header>

        <!-- Live Application Section -->
        <div class="section">
            <h2><span class="icon">🌐</span>Live Application</h2>
            <div class="url-box">
                <p style="margin-bottom: 10px; color: #94a3b8;">Production URL:</p>
                <a href="https://y0h0i3c8og5x.manus.space" target="_blank">https://y0h0i3c8og5x.manus.space</a>
            </div>

            <h3>Login Credentials</h3>
            <table class="credentials-table">
                <thead>
                    <tr>
                        <th>Role</th>
                        <th>Username</th>
                        <th>Password</th>
                        <th>Access Level</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Administrator</strong></td>
                        <td><code>admin01</code></td>
                        <td><code>hash123</code></td>
                        <td>Full system access</td>
                    </tr>
                    <tr>
                        <td><strong>Investor</strong></td>
                        <td><code>investor01</code></td>
                        <td><code>hash456</code></td>
                        <td>Financial data & analytics</td>
                    </tr>
                    <tr>
                        <td><strong>Researcher</strong></td>
                        <td><code>research01</code></td>
                        <td><code>hash789</code></td>
                        <td>Data viewing & export</td>
                    </tr>
                </tbody>
            </table>
            
            <div class="text-center mt-4">
                <a href="/login" class="btn btn-primary btn-lg">Access Platform</a>
            </div>
        </div>

        <!-- GUI Features Section -->
        <div class="section">
            <h2><span class="icon">🎨</span>Enhanced GUI Features</h2>
            
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🔐 Redesigned Login Page</h4>
                    <p>Split-screen layout with animated floating background, feature highlights, and professional testimonial section</p>
                </div>
                <div class="feature-card">
                    <h4>📊 Animated Dashboard</h4>
                    <p>Statistics cards with pulse effects, gradient accents, and smooth hover transformations</p>
                </div>
                <div class="feature-card">
                    <h4>🎭 Modern Theme</h4>
                    <p>Professional dark theme with blue-to-purple gradients and glassmorphism effects</p>
                </div>
                <div class="feature-card">
                    <h4>📱 Responsive Design</h4>
                    <p>Fully responsive interface that adapts beautifully to all screen sizes</p>
                </div>
                <div class="feature-card">
                    <h4>✨ Smooth Animations</h4>
                    <p>Fade-in effects, floating elements, and smooth transitions throughout</p>
                </div>
                <div class="feature-card">
                    <h4>🎯 Enhanced UX</h4>
                    <p>Icon animations, focus effects, and professional typography</p>
                </div>
            </div>
        </div>

        <!-- Project Statistics -->
        <div class="section">
            <h2><span class="icon">📊</span>Project Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="number">4</span>
                    <span class="label">Critical Minerals</span>
                </div>
                <div class="stat-card">
                    <span class="number">4</span>
                    <span class="label">African Countries</span>
                </div>
                <div class="stat-card">
                    <span class="number">4</span>
                    <span class="label">Mining Sites</span>
                </div>
                <div class="stat-card">
                    <span class="number">15+</span>
                    <span class="label">API Endpoints</span>
                </div>
            </div>
        </div>

        <!-- Key Features Section -->
        <div class="section">
            <h2><span class="icon">🌟</span>Key Features</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>🔒 Secure Authentication</h4>
                    <p>JWT-based authentication with role-based access control for administrators, investors, and researchers</p>
                </div>
                <div class="feature-card">
                    <h4>💎 Mineral Database</h4>
                    <p>Comprehensive data on Cobalt, Lithium, Graphite, and Manganese with market prices and descriptions</p>
                </div>
                <div class="feature-card">
                    <h4>🌍 Country Profiles</h4>
                    <p>Detailed profiles for DRC, South Africa, Mozambique, and Namibia with economic data</p>
                </div>
                <div class="feature-card">
                    <h4>🗺️ Interactive Map</h4>
                    <p>Geospatial visualization of mining sites across Africa using Leaflet technology</p>
                </div>
                <div class="feature-card">
                    <h4>📈 Analytics Dashboard</h4>
                    <p>Production trends, export values, and market dynamics with interactive charts</p>
                </div>
                <div class="feature-card">
                    <h4>🚀 RESTful API</h4>
                    <p>15+ endpoints for minerals, countries, production data, and site information</p>
                </div>
            </div>
        </div>

        <footer>
            <p><strong>Created by Group 34</strong></p>
            <p>MINN2020A - Computer Programming for Mining</p>
            <p>University of the Witwatersrand, Johannesburg</p>
            <p style="margin-top: 20px; color: #60a5fa;">© 2025 African Critical Minerals Platform</p>
        </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

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
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 500px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        header {
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        }

        h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 1.1em;
            color: #94a3b8;
            margin-bottom: 20px;
        }

        .section {
            margin-bottom: 30px;
            padding: 25px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
        }

        .form-control {
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(59, 130, 246, 0.3);
            color: #e2e8f0;
            padding: 12px;
        }

        .form-control:focus {
            background: rgba(15, 23, 42, 0.9);
            border-color: #3b82f6;
            color: #e2e8f0;
            box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.25);
        }

        .form-label {
            color: #93c5fd;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border: none;
            padding: 12px;
            font-weight: bold;
            width: 100%;
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            transform: translateY(-2px);
        }

        .alert {
            border: none;
            border-left: 4px solid #dc3545;
            background: rgba(220, 53, 69, 0.1);
            color: #f8d7da;
        }

        .table {
            color: #e2e8f0;
        }

        .table-dark {
            background: rgba(15, 23, 42, 0.7);
        }

        footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid rgba(59, 130, 246, 0.3);
            color: #94a3b8;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            margin-top: 10px;
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
                    <thead>
                        <tr>
                            <th>Role</th>
                            <th>Username</th>
                            <th>Password</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Administrator</td>
                            <td><code>admin01</code></td>
                            <td><code>hash123</code></td>
                        </tr>
                        <tr>
                            <td>Investor</td>
                            <td><code>investor01</code></td>
                            <td><code>hash456</code></td>
                        </tr>
                        <tr>
                            <td>Researcher</td>
                            <td><code>research01</code></td>
                            <td><code>hash789</code></td>
                        </tr>
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

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - African Critical Minerals Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- MULTIPLE LEAFLET CDN FALLBACKS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" 
          integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" 
          crossorigin=""/>
    <!-- Fallback CDN -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css" 
          integrity="sha512-puBpdR0798OZvTTbP4A8Ix/l+A4dHDD0DGqYW6RQ+9jxkRFclaxxQb/SJAWZfWAkuyeQUytO7+7N4QKrDh+drA==" 
          crossorigin="anonymous" referrerpolicy="no-referrer" />
    <style>
        /* All existing styles remain the same */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        }

        h1 {
            font-size: 3em;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 1.2em;
            color: #94a3b8;
            margin-bottom: 20px;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 10px;
        }

        .section {
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
        }

        h2 {
            color: #60a5fa;
            font-size: 2em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        h3 {
            color: #93c5fd;
            font-size: 1.5em;
            margin: 25px 0 15px 0;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #60a5fa;
            display: block;
        }

        .stat-card .label {
            color: #94a3b8;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .mineral-card, .country-card, .site-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            border-left: 4px solid #3b82f6;
            cursor: pointer;
            transition: transform 0.3s ease;
        }

        .country-card {
            border-left: 4px solid #22c55e;
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        }

        .site-card {
            border-left: 4px solid #f59e0b;
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
        }

        .mineral-card:hover, .country-card:hover, .site-card:hover {
            transform: translateY(-5px);
        }

        .api-endpoint {
            background: rgba(15, 23, 42, 0.7);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            border-left: 4px solid #8b5cf6;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid rgba(59, 130, 246, 0.3);
            color: #94a3b8;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
            transform: translateY(-2px);
        }

        .btn-warning {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border: none;
        }

        .btn-outline-info {
            border-color: #3b82f6;
            color: #3b82f6;
        }

        .btn-outline-info:hover {
            background: #3b82f6;
            color: white;
        }

        /* MAP STYLES */
        #interactiveMap {
            height: 500px;
            width: 100%;
            border-radius: 12px;
            margin: 20px 0;
            border: 2px solid rgba(59, 130, 246, 0.3);
        }

        .map-container {
            position: relative;
        }

        .map-overlay {
            position: absolute;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: rgba(15, 23, 42, 0.95);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .map-info {
            background: rgba(15, 23, 42, 0.9);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            margin-top: 10px;
        }

        .legend-item {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }

        .legend-color {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            margin-right: 10px;
            border: 2px solid white;
        }

        .country-color {
            background: #22c55e;
        }

        .mineral-color {
            background: #3b82f6;
        }

        .site-color {
            background: #f59e0b;
        }

        /* Fallback for map container */
        .map-fallback {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            height: 500px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 12px;
            border: 2px dashed rgba(59, 130, 246, 0.3);
            color: #94a3b8;
            text-align: center;
            padding: 20px;
        }

        /* NEW STYLES FOR ENHANCED FEATURES */
        .market-trends {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .trend-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .trend-up {
            color: #22c55e;
        }

        .trend-down {
            color: #ef4444;
        }

        .trend-stable {
            color: #f59e0b;
        }

        .news-item {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #3b82f6;
        }

        .impact-high {
            border-left-color: #ef4444;
        }

        .impact-medium {
            border-left-color: #f59e0b;
        }

        .impact-low {
            border-left-color: #22c55e;
        }

        .investment-card {
            background: linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 15px;
            border-left: 4px solid #22c55e;
        }

        .risk-high { color: #ef4444; }
        .risk-medium { color: #f59e0b; }
        .risk-low { color: #22c55e; }

        .quick-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
            margin: 15px 0;
        }

        .quick-stat {
            background: rgba(59, 130, 246, 0.1);
            padding: 10px;
            border-radius: 8px;
            text-align: center;
        }

        @media (max-width: 768px) {
            h1 {
                font-size: 2em;
            }

            .container {
                padding: 20px;
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            #interactiveMap {
                height: 300px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Dashboard</h1>
            <p class="subtitle">Welcome, {{ user_data.name }} ({{ user_data.role }})</p>
            <div class="badge">
                <a href="/logout" style="color: white; text-decoration: none;">
                    <i class="fas fa-sign-out-alt"></i> Logout
                </a>
            </div>
        </header>

        <!-- NEW: Quick Stats Bar -->
        <div class="quick-stats">
            <div class="quick-stat">
                <small>Session Time</small>
                <div id="sessionTimer">00:00</div>
            </div>
            <div class="quick-stat">
                <small>Last Login</small>
                <div>{{ session.get('login_time', 'First visit') }}</div>
            </div>
            <div class="quick-stat">
                <small>Your Role</small>
                <div>{{ user_data.role|title }}</div>
            </div>
        </div>

        <!-- Project Statistics -->
        <div class="section">
            <h2><span class="icon">📊</span>Platform Overview</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="number">{{ minerals|length }}</span>
                    <span class="label">Critical Minerals</span>
                </div>
                <div class="stat-card">
                    <span class="number">{{ countries|length }}</span>
                    <span class="label">African Countries</span>
                </div>
                <div class="stat-card">
                    <span class="number">{{ mining_sites|length }}</span>
                    <span class="label">Mining Sites</span>
                </div>
                <div class="stat-card">
                    <span class="number">20+</span>
                    <span class="label">Data Points</span>
                </div>
            </div>
        </div>

        <!-- NEW: Market Intelligence Section -->
        <div class="section">
            <h2><span class="icon">📈</span>Market Intelligence</h2>
            
            <h3>Price Trends</h3>
            <div class="market-trends">
                {% for trend in market_intelligence.price_trends %}
                <div class="trend-card">
                    <h5>{{ trend.mineral }}</h5>
                    <div class="number">${{ "{:,}".format(trend.current_price) }}</div>
                    <div class="trend-{{ trend.trend }}">
                        {% if trend.trend == 'up' %}
                        ↗ +{{ trend.change_percentage }}%
                        {% elif trend.trend == 'down' %}
                        ↘ {{ trend.change_percentage }}%
                        {% else %}
                        → {{ trend.change_percentage }}%
                        {% endif %}
                    </div>
                </div>
                {% endfor %}
            </div>

            <h3>Latest News</h3>
            {% for news in market_intelligence.market_news %}
            <div class="news-item impact-{{ news.impact }}">
                <h6>{{ news.title }}</h6>
                <p class="mb-1">{{ news.summary }}</p>
                <small class="text-muted">{{ news.date }} • Impact: {{ news.impact|title }}</small>
            </div>
            {% endfor %}
        </div>

        <!-- Interactive Map Section -->
        <div class="section">
            <h2><span class="icon">🗺️</span>Interactive Mineral Map</h2>
            <div class="map-container">
                <div id="interactiveMap">
                    <div class="map-fallback" id="mapFallback">
                        <div>
                            <i class="fas fa-sync fa-spin fa-3x mb-3" style="color: #3b82f6;"></i>
                            <h4>Loading Interactive Map...</h4>
                            <p>If the map doesn't load, we'll show a static version instead.</p>
                        </div>
                    </div>
                </div>
                <div class="map-overlay">
                    <h5 style="color: #60a5fa; margin-bottom: 15px;">Map Legend</h5>
                    <div class="legend-item">
                        <div class="legend-color country-color"></div>
                        <span>African Countries</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color site-color"></div>
                        <span>Mining Sites</span>
                    </div>
                </div>
            </div>
            <div class="map-info">
                <p><strong>Interactive Features:</strong> Click on any country or mining site marker to view detailed information. Click on the cards below to zoom to specific locations on the map.</p>
                <p>This interactive map shows the distribution of critical mineral resources across Africa, highlighting major mining operations and country-level mineral wealth.</p>
            </div>
        </div>

        <!-- NEW: Investment Opportunities (Visible to investors and admin) -->
        {% if user_data.role in ['investor', 'admin'] %}
        <div class="section">
            <h2><span class="icon">💼</span>Investment Opportunities</h2>
            {% for opportunity in investment_opportunities %}
            <div class="investment-card">
                <h4>{{ opportunity.title }}</h4>
                <div class="row">
                    <div class="col-md-6">
                        <strong>Country:</strong> {{ opportunity.country }}<br>
                        <strong>Mineral:</strong> {{ opportunity.mineral }}<br>
                        <strong>Investment Required:</strong> {{ opportunity.investment_required }}
                    </div>
                    <div class="col-md-6">
                        <strong>Estimated ROI:</strong> {{ opportunity.estimated_roi }}<br>
                        <strong>Risk Level:</strong> <span class="risk-{{ opportunity.risk_level|lower }}">{{ opportunity.risk_level }}</span><br>
                        <strong>Status:</strong> {{ opportunity.status }}
                    </div>
                </div>
                <small class="text-muted">Timeline: {{ opportunity.timeline }}</small>
            </div>
            {% endfor %}
        </div>
        {% endif %}

        <!-- Minerals Section -->
        <div class="section">
            <h2><span class="icon">💎</span>Critical Minerals</h2>
            <div class="row">
                {% for mineral in minerals %}
                <div class="col-md-6 mb-4">
                    <div class="mineral-card" onclick="showMineralOnMap('{{ mineral.name }}')">
                        <h4>{{ mineral.name }}</h4>
                        <p class="text-muted">{{ mineral.description }}</p>
                        <div class="row mt-3">
                            <div class="col-6">
                                <strong>Price:</strong><br>
                                <span class="text-warning">{{ mineral.price }} {{ mineral.unit }}</span>
                            </div>
                            <div class="col-6">
                                <strong>Trend:</strong><br>
                                {% if mineral.trend == 'increasing' %}
                                <span class="text-success">↗ Increasing</span>
                                {% else %}
                                <span class="text-warning">→ Stable</span>
                                {% endif %}
                            </div>
                        </div>
                        <div class="mt-2">
                            <small><strong>Demand Growth:</strong> {{ mineral.demand_growth }}</small><br>
                            <small><strong>Applications:</strong> {{ mineral.applications|join(', ') }}</small>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Countries Section -->
        <div class="section">
            <h2><span class="icon">🌍</span>Country Profiles</h2>
            <div class="row">
                {% for country in countries %}
                <div class="col-md-6 mb-4">
                    <div class="country-card" onclick="showCountryOnMap({{ country.id }})">
                        <h4>{{ country.name }}</h4>
                        <p class="text-muted">Capital: {{ country.capital }}</p>
                        <div class="row mt-3">
                            <div class="col-6">
                                <strong>GDP:</strong><br>
                                <span class="text-info">{{ country.gdp }}</span>
                            </div>
                            <div class="col-6">
                                <strong>Population:</strong><br>
                                <span class="text-info">{{ country.population }}</span>
                            </div>
                        </div>
                        <div class="mt-2">
                            <small><strong>Political Stability:</strong> {{ country.political_stability }}</small><br>
                            <small><strong>Infrastructure:</strong> {{ country.infrastructure }}</small><br>
                            <small><strong>Key Minerals:</strong> {{ country.key_minerals|join(', ') }}</small>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- Mining Sites Section -->
        <div class="section">
            <h2><span class="icon">⛏️</span>Mining Sites</h2>
            <div class="row">
                {% for site in mining_sites %}
                <div class="col-md-6 mb-4">
                    <div class="site-card" onclick="showSiteOnMap({{ site.id }})">
                        <h4>{{ site.name }}</h4>
                        <p class="text-muted">{{ site.country }} • {{ site.mineral }}</p>
                        <div class="row mt-3">
                            <div class="col-6">
                                <strong>Production:</strong><br>
                                <span class="text-warning">{{ site.production }}</span>
                            </div>
                            <div class="col-6">
                                <strong>Status:</strong><br>
                                <span class="text-success">{{ site.status }}</span>
                            </div>
                        </div>
                        <div class="mt-2">
                            <small><strong>Employment:</strong> {{ site.employment }}</small><br>
                            <small><strong>Established:</strong> {{ site.year_established }}</small><br>
                            <small><strong>Environmental Rating:</strong> {{ site.environmental_rating }}</small>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <!-- API Access Section -->
        <div class="section">
            <h2><span class="icon">🔌</span>API Access</h2>
            <p>Access our RESTful API endpoints to integrate mineral data into your applications:</p>
            
            <div class="api-endpoint">
                <h5><code>GET /api/minerals</code></h5>
                <p>Retrieve all critical minerals data with pricing and production information</p>
            </div>
            
            <div class="api-endpoint">
                <h5><code>GET /api/countries</code></h5>
                <p>Access comprehensive country profiles and economic data</p>
            </div>
            
            <div class="api-endpoint">
                <h5><code>GET /api/mining-sites</code></h5>
                <p>Get detailed information about mining locations and operations</p>
            </div>

            <div class="api-endpoint">
                <h5><code>GET /api/market-intelligence</code></h5>
                <p>Access real-time market trends and news (NEW)</p>
            </div>
            
            <div class="api-endpoint">
                <h5><code>GET /api/investment-opportunities</code></h5>
                <p>Get curated investment opportunities (Role-based access)</p>
            </div>

            <div class="text-center mt-4">
                <a href="/api/minerals" class="btn btn-outline-info me-2" target="_blank">Test Minerals API</a>
                <a href="/api/countries" class="btn btn-outline-info me-2" target="_blank">Test Countries API</a>
                <a href="/api/market-intelligence" class="btn btn-outline-info me-2" target="_blank">Market Data</a>
                {% if user_data.role in ['investor', 'admin'] %}
                <a href="/api/investment-opportunities" class="btn btn-outline-success" target="_blank">Investment Data</a>
                {% endif %}
            </div>
        </div>

        {% if user_data.role == 'admin' %}
        <div class="text-center mt-4">
            <a href="/admin" class="btn btn-warning">
                <i class="fas fa-cog"></i> Admin Panel
            </a>
        </div>
        {% endif %}

        <footer>
            <p><strong>Created by Group 34</strong> | Logged in as: {{ user_data.name }} ({{ user_data.role }})</p>
            <p>MINN2020A - Computer Programming for Mining | Enhanced with Market Intelligence & Investment Features</p>
            <p style="margin-top: 20px; color: #60a5fa;">© 2025 African Critical Minerals Platform</p>
        </footer>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <!-- MULTIPLE LEAFLET JS FALLBACKS -->
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
            integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo="
            crossorigin=""></script>
    <!-- Fallback CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"
            integrity="sha512-20cQSSNb8Rm4Hq+3eY1dvdSwWGLcPhvF+0I2F5k5C8tCMmKk1ZzK5K5vzqE3xEprZSeMb1pG0SwW3kXcZ2Qj6Q=="
            crossorigin="anonymous" referrerpolicy="no-referrer"></script>
    
    <script>
        // Enhanced map initialization with multiple fallbacks
        function initializeMap() {
            // Check if Leaflet is available
            if (typeof L === 'undefined') {
                console.warn('Leaflet not loaded, showing static map fallback');
                showStaticMap();
                return;
            }

            try {
                // Initialize the map
                var map = L.map('interactiveMap').setView([-8.7832, 34.5085], 4);

                // Try multiple tile providers with fallbacks
                var tileLayers = [
                    {
                        name: 'OpenStreetMap',
                        url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        attribution: '© OpenStreetMap contributors',
                        maxZoom: 18
                    },
                    {
                        name: 'OpenStreetMap Hot',
                        url: 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
                        attribution: '© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team',
                        maxZoom: 18
                    },
                    {
                        name: 'CartoDB',
                        url: 'https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
                        attribution: '© OpenStreetMap contributors, © CartoDB',
                        maxZoom: 18
                    }
                ];

                // Add the first tile layer
                var baseLayer = L.tileLayer(tileLayers[0].url, {
                    attribution: tileLayers[0].attribution,
                    maxZoom: tileLayers[0].maxZoom
                }).addTo(map);

                // Remove fallback message
                document.getElementById('mapFallback').style.display = 'none';

                // Country data
                var countries = {
                    {% for country in countries %}
                    {{ country.id }}: {
                        name: "{{ country.name }}",
                        lat: {{ country.coordinates.lat }},
                        lng: {{ country.coordinates.lng }},
                        capital: "{{ country.capital }}",
                        gdp: "{{ country.gdp }}",
                        population: "{{ country.population }}",
                        mining_contribution: "{{ country.mining_contribution }}",
                        key_minerals: {{ country.key_minerals | tojson }},
                        area: "{{ country.area }}",
                        investment_rating: "{{ country.investment_rating }}"
                    }{% if not loop.last %},{% endif %}
                    {% endfor %}
                };

                // Mining sites data
                var miningSites = {
                    {% for site in mining_sites %}
                    {{ site.id }}: {
                        name: "{{ site.name }}",
                        country: "{{ site.country }}",
                        mineral: "{{ site.mineral }}",
                        lat: {{ site.lat }},
                        lng: {{ site.lng }},
                        production: "{{ site.production }}",
                        operator: "{{ site.operator }}",
                        reserves: "{{ site.reserves }}",
                        status: "{{ site.status }}"
                    }{% if not loop.last %},{% endif %}
                    {% endfor %}
                };

                // Custom icons
                var countryIcon = L.divIcon({
                    className: 'custom-country-marker',
                    html: '<div style="background-color: #22c55e; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>',
                    iconSize: [16, 16],
                    iconAnchor: [8, 8]
                });

                var siteIcon = L.divIcon({
                    className: 'custom-site-marker',
                    html: '<div style="background-color: #f59e0b; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white;"></div>',
                    iconSize: [16, 16],
                    iconAnchor: [8, 8]
                });

                // Add country markers to the map
                Object.values(countries).forEach(function(country) {
                    var marker = L.marker([country.lat, country.lng], {icon: countryIcon})
                        .addTo(map)
                        .bindPopup(`
                            <div style="min-width: 250px; color: #1e293b;">
                                <h4 style="color: #22c55e; margin-bottom: 10px; border-bottom: 2px solid #22c55e; padding-bottom: 5px;">${country.name}</h4>
                                <p><strong>🏛️ Capital:</strong> ${country.capital}</p>
                                <p><strong>💰 GDP:</strong> ${country.gdp}</p>
                                <p><strong>👥 Population:</strong> ${country.population}</p>
                                <p><strong>⛏️ Mining Contribution:</strong> ${country.mining_contribution}</p>
                                <p><strong>📊 Investment Rating:</strong> ${country.investment_rating}</p>
                                <p><strong>🗺️ Area:</strong> ${country.area}</p>
                                <p><strong>💎 Key Minerals:</strong> ${country.key_minerals.join(', ')}</p>
                            </div>
                        `);
                });

                // Add mining site markers to the map
                Object.values(miningSites).forEach(function(site) {
                    var marker = L.marker([site.lat, site.lng], {icon: siteIcon})
                        .addTo(map)
                        .bindPopup(`
                            <div style="min-width: 250px; color: #1e293b;">
                                <h4 style="color: #f59e0b; margin-bottom: 10px; border-bottom: 2px solid #f59e0b; padding-bottom: 5px;">${site.name}</h4>
                                <p><strong>🌍 Country:</strong> ${site.country}</p>
                                <p><strong>💎 Mineral:</strong> ${site.mineral}</p>
                                <p><strong>📈 Production:</strong> ${site.production}</p>
                                <p><strong>🏢 Operator:</strong> ${site.operator}</p>
                                <p><strong>📦 Reserves:</strong> ${site.reserves}</p>
                                <p><strong>🟢 Status:</strong> ${site.status}</p>
                                <p><strong>📍 Coordinates:</strong> ${site.lat}, ${site.lng}</p>
                            </div>
                        `);
                });

                // Store map and data globally for other functions
                window.mineralsMap = map;
                window.mapCountries = countries;
                window.mapMiningSites = miningSites;

                // Add map loaded event
                map.whenReady(function() {
                    console.log('African Critical Minerals Map loaded successfully!');
                });

            } catch (error) {
                console.error('Error initializing map:', error);
                showStaticMap();
            }
        }

        // Static map fallback
        function showStaticMap() {
            var mapContainer = document.getElementById('interactiveMap');
            mapContainer.innerHTML = `
                <div class="static-map">
                    <div style="position: relative; width: 100%; height: 100%; background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%); border-radius: 12px;">
                        <!-- Africa outline points -->
                        <div class="map-point country-point" style="top: 45%; left: 48%;" title="DRC - Cobalt, Copper"></div>
                        <div class="map-point country-point" style="top: 75%; left: 52%;" title="South Africa - Platinum, Gold"></div>
                        <div class="map-point country-point" style="top: 60%; left: 58%;" title="Mozambique - Graphite, Coal"></div>
                        <div class="map-point country-point" style="top: 65%; left: 45%;" title="Namibia - Uranium, Lithium"></div>
                        
                        <div class="map-point site-point" style="top: 42%; left: 50%;" title="Tenke Fungurume Mine - Cobalt"></div>
                        <div class="map-point site-point" style="top: 78%; left: 50%;" title="Kalahari Manganese Field - Manganese"></div>
                        <div class="map-point site-point" style="top: 58%; left: 60%;" title="Balama Graphite Project - Graphite"></div>
                        <div class="map-point site-point" style="top: 68%; left: 43%;" title="Uis Tin Mine - Lithium"></div>
                        
                        <div style="position: absolute; bottom: 20px; left: 20px; background: rgba(15, 23, 42, 0.9); padding: 15px; border-radius: 8px; color: white;">
                            <h5 style="color: #60a5fa; margin-bottom: 10px;">Static Map View</h5>
                            <p>Interactive map unavailable. Showing mineral distribution across Africa.</p>
                            <div class="legend-item">
                                <div class="legend-color country-color"></div>
                                <span>Countries</span>
                            </div>
                            <div class="legend-item">
                                <div class="legend-color site-color"></div>
                                <span>Mining Sites</span>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Global functions for map interaction
        window.showCountryOnMap = function(countryId) {
            if (!window.mineralsMap || !window.mapCountries) {
                alert('Interactive map is not available. Please check your connection.');
                return;
            }
            
            var country = window.mapCountries[countryId];
            if (country) {
                window.mineralsMap.setView([country.lat, country.lng], 6);
            }
        }

        window.showSiteOnMap = function(siteId) {
            if (!window.mineralsMap || !window.mapMiningSites) {
                alert('Interactive map is not available. Please check your connection.');
                return;
            }
            
            var site = window.mapMiningSites[siteId];
            if (site) {
                window.mineralsMap.setView([site.lat, site.lng], 8);
            }
        }

        window.showMineralOnMap = function(mineralName) {
            if (!window.mineralsMap || !window.mapMiningSites) {
                alert('Interactive map is not available. Please check your connection.');
                return;
            }
            
            var sitesForMineral = Object.values(window.mapMiningSites).filter(site => 
                site.mineral.toLowerCase() === mineralName.toLowerCase()
            );
            
            if (sitesForMineral.length > 0) {
                var group = new L.featureGroup();
                sitesForMineral.forEach(site => {
                    group.addLayer(L.marker([site.lat, site.lng]));
                });
                window.mineralsMap.fitBounds(group.getBounds().pad(0.1));
            }
        }

        // NEW: Session timer
        let sessionStart = Date.now();
        function updateSessionTimer() {
            const now = Date.now();
            const diff = now - sessionStart;
            const minutes = Math.floor(diff / 60000);
            const seconds = Math.floor((diff % 60000) / 1000);
            document.getElementById('sessionTimer').textContent = 
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        }
        setInterval(updateSessionTimer, 1000);

        // Initialize map when page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Wait a bit for Leaflet to load, then initialize
            setTimeout(initializeMap, 100);
            
            // Fallback: if Leaflet isn't loaded after 3 seconds, show static map
            setTimeout(function() {
                if (typeof L === 'undefined') {
                    showStaticMap();
                }
            }, 3000);
        });
    </script>
</body>
</html>
'''

ADMIN_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel - African Critical Minerals Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        }

        header {
            text-align: center;
            margin-bottom: 50px;
            padding-bottom: 30px;
            border-bottom: 2px solid rgba(59, 130, 246, 0.3);
        }

        h1 {
            font-size: 2.5em;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            font-weight: bold;
        }

        .subtitle {
            font-size: 1.2em;
            color: #94a3b8;
            margin-bottom: 20px;
        }

        .badge {
            display: inline-block;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            font-weight: bold;
            margin-top: 10px;
        }

        .section {
            margin-bottom: 40px;
            padding: 30px;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 15px;
            border-left: 4px solid #3b82f6;
        }

        h2 {
            color: #60a5fa;
            font-size: 2em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }

        .stat-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .stat-card .number {
            font-size: 2.5em;
            font-weight: bold;
            color: #60a5fa;
            display: block;
        }

        .stat-card .label {
            color: #94a3b8;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .credentials-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: rgba(15, 23, 42, 0.5);
            border-radius: 10px;
            overflow: hidden;
        }

        .credentials-table th,
        .credentials-table td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid rgba(59, 130, 246, 0.2);
        }

        .credentials-table th {
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            font-weight: bold;
        }

        .credentials-table tr:last-child td {
            border-bottom: none;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .feature-card {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            padding: 25px;
            border-radius: 12px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        }

        .feature-card h4 {
            color: #60a5fa;
            margin-bottom: 10px;
            font-size: 1.2em;
        }

        .feature-card p {
            color: #cbd5e1;
            font-size: 0.95em;
        }

        footer {
            text-align: center;
            margin-top: 50px;
            padding-top: 30px;
            border-top: 2px solid rgba(59, 130, 246, 0.3);
            color: #94a3b8;
        }

        .btn-primary {
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
            border: none;
            padding: 10px 20px;
            font-weight: bold;
        }

        .btn-outline-primary, .btn-outline-success, .btn-outline-warning, .btn-outline-danger {
            border-width: 2px;
            font-weight: 600;
        }

        /* NEW: Activity log styles */
        .activity-log {
            max-height: 300px;
            overflow-y: auto;
            background: rgba(15, 23, 42, 0.3);
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
        }

        .activity-item {
            padding: 8px 12px;
            margin-bottom: 8px;
            background: rgba(59, 130, 246, 0.1);
            border-radius: 6px;
            border-left: 3px solid #3b82f6;
        }

        .activity-time {
            font-size: 0.8em;
            color: #94a3b8;
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }

            .stats-grid, .feature-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⚙️ Admin Panel</h1>
            <p class="subtitle">System Administration & Management</p>
            <div class="badge">
                <a href="/dashboard" style="color: white; text-decoration: none;">
                    <i class="fas fa-arrow-left"></i> Back to Dashboard
                </a>
            </div>
        </header>

        <div class="section">
            <h2><span class="icon">👥</span>User Management</h2>
            
            <table class="credentials-table">
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Role</th>
                        <th>Name</th>
                        <th>Last Login</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for username, user in users.items() %}
                    <tr>
                        <td><code>{{ username }}</code></td>
                        <td>
                            <span class="badge {% if user.role == 'admin' %}bg-danger{% else %}bg-primary{% endif %}" style="background: {% if user.role == 'admin' %}linear-gradient(135deg, #dc2626 0%, #b91c1c 100%){% else %}linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%){% endif %} !important;">
                                {{ user.role }}
                            </span>
                        </td>
                        <td>{{ user.name }}</td>
                        <td>{{ user.last_login or 'Never' }}</td>
                        <td>
                            <button class="btn btn-sm btn-outline-warning">Edit</button>
                            <button class="btn btn-sm btn-outline-danger">Reset Password</button>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- NEW: Activity Log Section -->
        <div class="section">
            <h2><span class="icon">📋</span>Activity Log</h2>
            <div class="activity-log">
                {% if session.get('user_activity') %}
                    {% for activity in session.user_activity %}
                    <div class="activity-item">
                        <div>{{ activity.activity }}</div>
                        <div class="activity-time">{{ activity.timestamp }}</div>
                    </div>
                    {% endfor %}
                {% else %}
                    <p class="text-muted">No recent activity recorded.</p>
                {% endif %}
            </div>
        </div>

        <div class="section">
            <h2><span class="icon">📈</span>System Statistics</h2>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="number">{{ minerals|length }}</span>
                    <span class="label">Minerals in DB</span>
                </div>
                <div class="stat-card">
                    <span class="number">{{ countries|length }}</span>
                    <span class="label">Countries</span>
                </div>
                <div class="stat-card">
                    <span class="number">{{ mining_sites|length }}</span>
                    <span class="label">Mining Sites</span>
                </div>
                <div class="stat-card">
                    <span class="number">{{ users|length }}</span>
                    <span class="label">Active Users</span>
                </div>
            </div>
        </div>

        <div class="section">
            <h2><span class="icon">🛠️</span>Database Operations</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <h4>📥 Import Data</h4>
                    <p>Bulk import mineral and country data from CSV files</p>
                    <button class="btn btn-outline-primary btn-sm mt-2">Import</button>
                </div>
                <div class="feature-card">
                    <h4>📤 Export Data</h4>
                    <p>Export database to JSON, CSV, or Excel formats</p>
                    <button class="btn btn-outline-success btn-sm mt-2">Export</button>
                </div>
                <div class="feature-card">
                    <h4>🔄 Update Prices</h4>
                    <p>Refresh mineral prices from market data feeds</p>
                    <button class="btn btn-outline-warning btn-sm mt-2">Update</button>
                </div>
                <div class="feature-card">
                    <h4>🧹 Clean Database</h4>
                    <p>Remove duplicate entries and clean data</p>
                    <button class="btn btn-outline-danger btn-sm mt-2">Clean</button>
                </div>
            </div>
        </div>

        <footer>
            <p><strong>Admin Panel</strong> | Logged in as: {{ user_data.name }} ({{ user_data.role }})</p>
            <p style="margin-top: 20px; color: #60a5fa;">© 2025 African Critical Minerals Platform - Group 34</p>
        </footer>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

# CORE APPLICATION ROUTES


@app.route('/')
def index():
    """Display the main landing page with project information"""
    return render_template_string(INDEX_HTML)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user authentication with credential validation"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = USERS.get(username)
        if user and user['password'] == password:
            # Successful login
            session['username'] = username
            session['role'] = user['role']
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update last login time
            USERS[username]['last_login'] = session['login_time']
            
            # Track login activity
            track_activity(f"User {username} logged in")
            
            return redirect(url_for('dashboard'))
        else:
            return render_template_string(LOGIN_HTML, error="Invalid credentials")
    
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    """Clear user session and redirect to home page"""
    if 'username' in session:
        track_activity(f"User {session['username']} logged out")
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Display the main application dashboard with all features"""
    user_data = USERS.get(session['username'])
    track_activity("Accessed dashboard")
    
    return render_template_string(
        DASHBOARD_HTML, 
        minerals=MINERALS,
        countries=COUNTRIES,
        mining_sites=MINING_SITES,
        market_intelligence=MARKET_INTELLIGENCE,
        investment_opportunities=INVESTMENT_OPPORTUNITIES,
        user_data=user_data
    )

@app.route('/admin')
@login_required
@role_required('admin')
def admin_panel():
    """Display administrative control panel (admin only)"""
    user_data = USERS.get(session['username'])
    track_activity("Accessed admin panel")
    
    return render_template_string(
        ADMIN_HTML,
        users=USERS,
        minerals=MINERALS,
        countries=COUNTRIES,
        mining_sites=MINING_SITES,
        user_data=user_data
    )

]
# RESTful API ENDPOINTS


@app.route('/api/minerals')
@login_required
def api_minerals():
    """API endpoint: Returns JSON data for all critical minerals"""
    track_activity("Accessed minerals API")
    return jsonify({
        "status": "success",
        "data": MINERALS,
        "count": len(MINERALS),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/countries')
@login_required
def api_countries():
    """API endpoint: Returns JSON data for all African countries"""
    track_activity("Accessed countries API")
    return jsonify({
        "status": "success",
        "data": COUNTRIES,
        "count": len(COUNTRIES),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/mining-sites')
@login_required
def api_mining_sites():
    """API endpoint: Returns JSON data for all mining sites"""
    track_activity("Accessed mining sites API")
    return jsonify({
        "status": "success",
        "data": MINING_SITES,
        "count": len(MINING_SITES),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/market-intelligence')
@login_required
def api_market_intelligence():
    """API endpoint: Returns real-time market data and news"""
    track_activity("Accessed market intelligence API")
    return jsonify({
        "status": "success",
        "data": MARKET_INTELLIGENCE,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/investment-opportunities')
@login_required
def api_investment_opportunities():
    """API endpoint: Returns investment projects (investor/admin only)"""
    user_role = USERS.get(session['username'], {}).get('role')
    if user_role not in ['investor', 'admin']:
        return jsonify({"status": "error", "message": "Access denied"}), 403
    
    track_activity("Accessed investment opportunities API")
    return jsonify({
        "status": "success",
        "data": INVESTMENT_OPPORTUNITIES,
        "count": len(INVESTMENT_OPPORTUNITIES),
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/mineral/<int:mineral_id>')
@login_required
def api_mineral(mineral_id):
    """API endpoint: Returns detailed data for a specific mineral by ID"""
    mineral = next((m for m in MINERALS if m['id'] == mineral_id), None)
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
    country = next((c for c in COUNTRIES if c['id'] == country_id), None)
    if country:
        track_activity(f"Accessed country data: {country['name']}")
        return jsonify({
            "status": "success",
            "data": country,
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"status": "error", "message": "Country not found"}), 404

@app.route('/api/stats')
@login_required
def api_stats():
    """API endpoint: Returns comprehensive platform statistics"""
    track_activity("Accessed platform statistics")
    return jsonify({
        "status": "success",
        "data": {
            "minerals_count": len(MINERALS),
            "countries_count": len(COUNTRIES),
            "mining_sites_count": len(MINING_SITES),
            "users_count": len(USERS),
            "market_news_count": len(MARKET_INTELLIGENCE['market_news']),
            "investment_opportunities_count": len(INVESTMENT_OPPORTUNITIES)
        },
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


# APPLICATION STARTUP


if __name__ == '__main__':
    """Application entry point - starts the Flask development server"""
    
    # Display startup information
    print("=" * 70)
    print("🏔️  African Critical Minerals Platform - Group 34")
    print("MINN2020A Project 2025 - University of the Witwatersrand")
    print("=" * 70)
    print("\n🚀 Starting Enhanced Flask application...")
    print("📊 Available data:")
    print(f"   • {len(MINERALS)} critical minerals (enhanced with market data)")
    print(f"   • {len(COUNTRIES)} African countries (enhanced with risk profiles)")
    print(f"   • {len(MINING_SITES)} mining sites (enhanced with operational data)")
    print(f"   • {len(USERS)} user accounts")
    print(f"   • {len(MARKET_INTELLIGENCE['market_news'])} market news items")
    print(f"   • {len(INVESTMENT_OPPORTUNITIES)} investment opportunities")
    print("\n🔑 Demo Login Credentials:")
    for username, user in USERS.items():
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
    
    # Start Flask development server
    app.run(debug=True, host='0.0.0.0', port=8080)
