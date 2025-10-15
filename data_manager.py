# =============================================================================
# DATA ARCHITECT & BACKEND MANAGER
# Member 2: Data Management & Business Logic
# =============================================================================

from datetime import datetime
import json

# Comprehensive mineral database
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
        "risk_factors": ["Supply Chain", "Geopolitical", "Environmental"],
        "discovery_year": 1735,
        "chemical_symbol": "Co",
        "density": "8.9 g/cm³"
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
        "risk_factors": ["Water Usage", "Price Volatility", "Processing"],
        "discovery_year": 1817,
        "chemical_symbol": "Li",
        "density": "0.534 g/cm³"
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
        "risk_factors": ["Chinese Dominance", "Processing Costs", "Quality Variance"],
        "discovery_year": 1565,
        "chemical_symbol": "C",
        "density": "2.2 g/cm³"
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
        "risk_factors": ["Steel Demand", "Logistics", "Infrastructure"],
        "discovery_year": 1774,
        "chemical_symbol": "Mn",
        "density": "7.21 g/cm³"
    }
]

# Enhanced country profiles
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
        "political_stability": "Medium Risk",
        "currency": "Congolese Franc (CDF)",
        "languages": ["French", "Lingala", "Kikongo"],
        "mining_code": "Mining Code 2018"
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
        "political_stability": "Medium Risk",
        "currency": "South African Rand (ZAR)",
        "languages": ["English", "Afrikaans", "Zulu"],
        "mining_code": "Mining Charter 2018"
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
        "political_stability": "High Risk",
        "currency": "Mozambican Metical (MZN)",
        "languages": ["Portuguese", "Emakhuwa", "Xichangana"],
        "mining_code": "Mining Law 2014"
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
        "political_stability": "Low Risk",
        "currency": "Namibian Dollar (NAD)",
        "languages": ["English", "Afrikaans", "Oshiwambo"],
        "mining_code": "Minerals Act 1992"
    }
]

# Comprehensive mining sites data
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
        "environmental_rating": "B",
        "ownership": ["China Molybdenum (80%)", "Gécamines (20%)"],
        "mining_method": "Open Pit",
        "processing_capacity": "15,000 tpd"
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
        "environmental_rating": "A-",
        "ownership": ["South32", "Assmang"],
        "mining_method": "Underground & Open Pit",
        "processing_capacity": "6 million tpa"
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
        "environmental_rating": "B+",
        "ownership": ["Syrah Resources (100%)"],
        "mining_method": "Open Pit",
        "processing_capacity": "350,000 tpa"
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
        "environmental_rating": "A",
        "ownership": ["Andrada Mining (100%)"],
        "mining_method": "Open Pit",
        "processing_capacity": "5,000 tpa"
    }
]

# Market intelligence data
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
            "impact": "medium",
            "category": "Regulatory"
        },
        {
            "title": "Electric Vehicle Demand Drives Lithium Prices",
            "summary": "Global EV sales growth continues to fuel lithium demand",
            "date": "2024-01-12",
            "impact": "high",
            "category": "Market"
        },
        {
            "title": "Mozambique Infrastructure Improvements",
            "summary": "New port facilities to boost graphite export capacity",
            "date": "2024-01-10",
            "impact": "low",
            "category": "Infrastructure"
        }
    ],
    "supply_chain_analysis": {
        "cobalt": {"bottlenecks": ["DRC supply chain", "Refining capacity"], "outlook": "Tight"},
        "lithium": {"bottlenecks": ["Processing technology", "Water access"], "outlook": "Improving"},
        "graphite": {"bottlenecks": ["Chinese dominance", "Quality control"], "outlook": "Stable"},
        "manganese": {"bottlenecks": ["Logistics", "Infrastructure"], "outlook": "Good"}
    }
}

# Investment opportunities database
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
        "status": "Feasibility",
        "project_stage": "Exploration",
        "resource_estimate": "15Mt @ 1.2% Li2O",
        "infrastructure": "Good",
        "regulatory_approval": "Pending"
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
        "status": "Planning",
        "project_stage": "Development",
        "resource_estimate": "N/A",
        "infrastructure": "Basic",
        "regulatory_approval": "Approved"
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
        "status": "Approved",
        "project_stage": "Expansion",
        "resource_estimate": "50Mt @ 6% Cg",
        "infrastructure": "Developing",
        "regulatory_approval": "Granted"
    }
]

class DataManager:
    """Comprehensive data management class for the minerals platform"""
    
    def __init__(self):
        self.minerals = MINERALS
        self.countries = COUNTRIES
        self.mining_sites = MINING_SITES
        self.market_intelligence = MARKET_INTELLIGENCE
        self.investment_opportunities = INVESTMENT_OPPORTUNITIES
    
    def get_mineral_by_id(self, mineral_id):
        """Get specific mineral by ID"""
        return next((m for m in self.minerals if m['id'] == mineral_id), None)
    
    def get_country_by_id(self, country_id):
        """Get specific country by ID"""
        return next((c for c in self.countries if c['id'] == country_id), None)
    
    def get_mining_site_by_id(self, site_id):
        """Get specific mining site by ID"""
        return next((s for s in self.mining_sites if s['id'] == site_id), None)
    
    def search_minerals(self, query):
        """Search minerals by name, description, or applications"""
        query = query.lower()
        results = []
        for mineral in self.minerals:
            if (query in mineral['name'].lower() or 
                query in mineral['description'].lower() or
                any(query in app.lower() for app in mineral['applications'])):
                results.append(mineral)
        return results
    
    def get_countries_by_mineral(self, mineral_name):
        """Get countries that produce a specific mineral"""
        mineral_name = mineral_name.lower()
        producing_countries = []
        
        for country in self.countries:
            if any(mineral_name in mineral.lower() for mineral in country['key_minerals']):
                producing_countries.append(country)
        
        return producing_countries
    
    def get_sites_by_mineral(self, mineral_name):
        """Get mining sites for a specific mineral"""
        mineral_name = mineral_name.lower()
        return [site for site in self.mining_sites if site['mineral'].lower() == mineral_name]
    
    def get_sites_by_country(self, country_name):
        """Get mining sites in a specific country"""
        country_name = country_name.lower()
        return [site for site in self.mining_sites if site['country'].lower() == country_name]
    
    def get_market_trends(self, mineral_name=None):
        """Get market trends, optionally filtered by mineral"""
        trends = self.market_intelligence['price_trends']
        if mineral_name:
            mineral_name = mineral_name.lower()
            return [trend for trend in trends if trend['mineral'].lower() == mineral_name]
        return trends
    
    def get_investment_opportunities_by_risk(self, risk_level=None):
        """Get investment opportunities, optionally filtered by risk level"""
        if risk_level:
            risk_level = risk_level.lower()
            return [opp for opp in self.investment_opportunities if opp['risk_level'].lower() == risk_level]
        return self.investment_opportunities
    
    def get_platform_statistics(self):
        """Get comprehensive platform statistics"""
        return {
            "total_minerals": len(self.minerals),
            "total_countries": len(self.countries),
            "total_mining_sites": len(self.mining_sites),
            "total_investment_opportunities": len(self.investment_opportunities),
            "market_news_count": len(self.market_intelligence['market_news']),
            "data_last_updated": datetime.now().isoformat()
        }
    
    def export_data(self, data_type, format='json'):
        """Export data in specified format"""
        data_map = {
            'minerals': self.minerals,
            'countries': self.countries,
            'mining_sites': self.mining_sites,
            'market_intelligence': self.market_intelligence,
            'investment_opportunities': self.investment_opportunities
        }
        
        data = data_map.get(data_type)
        if not data:
            return None
            
        if format == 'json':
            return json.dumps(data, indent=2)
        # Could add CSV, Excel formats here
        
        return None

# Global data manager instance
data_manager = DataManager()

# Convenience functions for easy access
def load_mineral_data():
    return data_manager.minerals

def get_all_countries():
    return data_manager.countries

def get_all_mining_sites():
    return data_manager.mining_sites

def get_market_intelligence():
    return data_manager.market_intelligence

def get_investment_opportunities():
    return data_manager.investment_opportunities

def get_platform_stats():
    return data_manager.get_platform_statistics()

def search_minerals(query):
    return data_manager.search_minerals(query)

def get_countries_by_mineral(mineral_name):
    return data_manager.get_countries_by_mineral(mineral_name)