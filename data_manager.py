# =============================================================================
# DATA ARCHITECT & BACKEND MANAGER
# Member 2: Data Management
# =============================================================================

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

def load_mineral_data():
    """Load all mineral data"""
    return MINERALS

def get_country_profile(country_name):
    """Get specific country profile"""
    for country in COUNTRIES:
        if country['name'].lower() == country_name.lower():
            return country
    return None

def get_production_trends(mineral=None, country=None):
    """Get production trends with optional filters"""
    trends = []
    for site in MINING_SITES:
        if (mineral is None or site['mineral'].lower() == mineral.lower()) and \
           (country is None or site['country'].lower() == country.lower()):
            trends.append(site)
    return trends

def get_all_minerals():
    """Get all minerals"""
    return MINERALS

def search_minerals(query):
    """Search minerals by name or description"""
    results = []
    for mineral in MINERALS:
        if query.lower() in mineral['name'].lower() or query.lower() in mineral['description'].lower():
            results.append(mineral)
    return results

def get_all_countries():
    """Get all countries"""
    return COUNTRIES

def get_all_mining_sites():
    """Get all mining sites"""
    return MINING_SITES

def get_market_intelligence():
    """Get market intelligence data"""
    return MARKET_INTELLIGENCE

def get_investment_opportunities():
    """Get investment opportunities"""
    return INVESTMENT_OPPORTUNITIES

def get_platform_stats():
    """Get platform statistics"""
    return {
        "minerals_count": len(MINERALS),
        "countries_count": len(COUNTRIES),
        "mining_sites_count": len(MINING_SITES),
        "market_news_count": len(MARKET_INTELLIGENCE['market_news']),
        "investment_opportunities_count": len(INVESTMENT_OPPORTUNITIES)
    }
