import streamlit as st
import pandas as pd
from database.connection import init_connection

def get_total_cases_by_date_range(start_date, end_date):
    """Get total number of cases within date range"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT SUM(crime_facts.incident_count) AS total_incidents 
        FROM crime_facts 
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return int(df['total_incidents'].iloc[0]) if not df.empty and df['total_incidents'].iloc[0] is not None else 0
    except Exception as e:
        st.error(f"Error fetching total cases: {e}")
        return 0

def get_crime_hotspot_category_by_date_range(start_date, end_date):
    """Get the location category with highest crime count within date range"""
    engine = init_connection()
    if engine is None:
        return None, 0
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT dim_location_category.location_category, SUM(crime_facts.incident_count) as total_cases
        FROM crime_facts
        JOIN dim_location ON dim_location.id_location = crime_facts.id_location
        JOIN dim_location_category ON dim_location.id_location_category = dim_location_category.id_location_category
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_location_category.id_location_category, dim_location_category.location_category
        ORDER BY total_cases DESC
        LIMIT 1
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        if not df.empty:
            return df['location_category'].iloc[0], int(df['total_cases'].iloc[0])
        return None, 0
    except Exception as e:
        st.error(f"Error fetching crime hotspot category: {e}")
        return None, 0

def get_crime_hotspot_by_date_range(start_date, end_date):
    """Get the location with highest crime count within date range (kept for backward compatibility)"""
    engine = init_connection()
    if engine is None:
        return None, 0
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT dim_location.location_description, SUM(crime_facts.incident_count) as total_cases
        FROM crime_facts
        JOIN dim_location ON dim_location.id_location = crime_facts.id_location
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_location.id_location, dim_location.location_description
        ORDER BY total_cases DESC
        LIMIT 1
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        if not df.empty:
            return df['location_description'].iloc[0], int(df['total_cases'].iloc[0])
        return None, 0
    except Exception as e:
        st.error(f"Error fetching crime hotspot: {e}")
        return None, 0

def get_risky_area_by_date_range(start_date, end_date):
    """Get the riskiest location type within date range"""
    engine = init_connection()
    if engine is None:
        return None, 0
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT dim_location.location_description, SUM(crime_facts.incident_count) as total_cases
        FROM crime_facts
        JOIN dim_location ON dim_location.id_location = crime_facts.id_location
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_location.id_location, dim_location.location_description
        ORDER BY total_cases DESC
        LIMIT 1
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        if not df.empty:
            return df['location_description'].iloc[0], int(df['total_cases'].iloc[0])
        return None, 0
    except Exception as e:
        st.error(f"Error fetching risky area: {e}")
        return None, 0

def get_total_areas():
    """Get total number of areas in database"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        query = "SELECT COUNT(*) as total_areas FROM dim_location"
        df = pd.read_sql_query(query, engine)
        return int(df['total_areas'].iloc[0]) if not df.empty else 0
    except Exception as e:
        st.error(f"Error fetching total areas: {e}")
        return 0

def get_map_data_by_date_range(start_date, end_date):
    """Get geographical data for map visualization"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            crime_facts.latitude,
            crime_facts.longitude,
            dim_crime.primary_type,
            dim_crime_category.crime_category,
            dim_location.location_description,
            dim_location_category.location_category,
            SUM(crime_facts.incident_count) as total_incidents
        FROM crime_facts
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_crime_category ON dim_crime.id_crime_category = dim_crime_category.id_crime_category
        JOIN dim_location ON crime_facts.id_location = dim_location.id_location
        JOIN dim_location_category ON dim_location.id_location_category = dim_location_category.id_location_category
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        AND crime_facts.latitude IS NOT NULL 
        AND crime_facts.longitude IS NOT NULL
        GROUP BY crime_facts.latitude, crime_facts.longitude, dim_crime.primary_type, 
                 dim_crime_category.crime_category, dim_location.location_description,
                 dim_location_category.location_category
        ORDER BY total_incidents DESC
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching map data: {e}")
        return pd.DataFrame()

def get_crime_by_location_category(start_date, end_date):
    """Get crime data grouped by location category for doughnut chart"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            dim_location_category.location_category,
            dim_crime_category.crime_category,
            SUM(crime_facts.incident_count) as total_incidents
        FROM crime_facts
        JOIN dim_location ON crime_facts.id_location = dim_location.id_location
        JOIN dim_location_category ON dim_location.id_location_category = dim_location_category.id_location_category
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_crime_category ON dim_crime.id_crime_category = dim_crime_category.id_crime_category
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_location_category.location_category, dim_crime_category.crime_category
        ORDER BY dim_location_category.location_category, total_incidents DESC
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime by location category: {e}")
        return pd.DataFrame()

def get_top_location_descriptions(start_date, end_date, limit=5):
    """Get top location descriptions for bar chart"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            dim_location.location_description,
            dim_location_category.location_category,
            dim_crime_category.crime_category,
            SUM(crime_facts.incident_count) as total_incidents
        FROM crime_facts
        JOIN dim_location ON crime_facts.id_location = dim_location.id_location
        JOIN dim_location_category ON dim_location.id_location_category = dim_location_category.id_location_category
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_crime_category ON dim_crime.id_crime_category = dim_crime_category.id_crime_category
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_location.location_description, dim_location_category.location_category, dim_crime_category.crime_category
        ORDER BY total_incidents DESC
        LIMIT %(limit)s
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day,
            'limit': limit
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching top location descriptions: {e}")
        return pd.DataFrame()

def get_crime_details_by_date_range(start_date, end_date, location_category=None, crime_category=None):
    """Get detailed crime data for table display"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day

        query = """
        SELECT 
            dim_crime_category.crime_category,
            dim_crime.primary_type,
            dim_crime.description as crime_description,
            dim_date.day,
            dim_date.month,
            dim_date.year,
            dim_date.daytime,
            crime_facts.arrest_status,
            dim_location.location_description,
            dim_location_category.location_category,
            crime_facts.incident_count
        FROM crime_facts
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_crime_category ON dim_crime.id_crime_category = dim_crime_category.id_crime_category
        JOIN dim_location ON crime_facts.id_location = dim_location.id_location
        JOIN dim_location_category ON dim_location.id_location_category = dim_location_category.id_location_category
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }

        if location_category and location_category != "Semua Area":
            query += " AND dim_location_category.location_category = %(location_category)s"
            params['location_category'] = location_category

        if crime_category and crime_category != "Semua Kategori":
            query += " AND dim_crime_category.crime_category = %(crime_category)s"
            params['crime_category'] = crime_category
        
        query += """
        ORDER BY dim_date.year DESC, dim_date.month DESC, dim_date.day DESC
        """
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime details: {e}")
        return pd.DataFrame()

def get_location_categories():
    """Get all location categories for dropdown"""
    engine = init_connection()
    if engine is None:
        return []
    
    try:
        query = "SELECT DISTINCT location_category FROM dim_location_category ORDER BY location_category"
        df = pd.read_sql_query(query, engine)
        categories = ["Semua Area"] + df['location_category'].tolist()
        return categories
    except Exception as e:
        st.error(f"Error fetching location categories: {e}")
        return ["Semua Area"]

def get_crime_categories():
    """Get all crime categories for dropdown"""
    engine = init_connection()
    if engine is None:
        return []
    
    try:
        query = "SELECT DISTINCT crime_category FROM dim_crime_category ORDER BY crime_category"
        df = pd.read_sql_query(query, engine)
        categories = ["Semua Kategori"] + df['crime_category'].tolist()
        return categories
    except Exception as e:
        st.error(f"Error fetching crime categories: {e}")
        return ["Semua Kategori"]
    
def get_filtered_total_incidents_geographic(start_date, end_date, location_category_filter=None, crime_category_filter=None):
    """Get total incidents with geographic filters applied (aggregated by incident_count, not row count)"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            SUM(cf.incident_count) AS total_incidents
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_location dl ON cf.id_location = dl.id_location
        JOIN dim_location_category dlc ON dl.id_location_category = dlc.id_location_category
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE (dd.year > %(start_year)s OR 
               (dd.year = %(start_year)s AND dd.month > %(start_month)s) OR
               (dd.year = %(start_year)s AND dd.month = %(start_month)s AND dd.day >= %(start_day)s))
        AND (dd.year < %(end_year)s OR 
             (dd.year = %(end_year)s AND dd.month < %(end_month)s) OR
             (dd.year = %(end_year)s AND dd.month = %(end_month)s AND dd.day <= %(end_day)s))
        """
        
        params = {
            'start_year': start_year,
            'start_month': start_month, 
            'start_day': start_day,
            'end_year': end_year,
            'end_month': end_month,
            'end_day': end_day
        }

        if location_category_filter:
            query += " AND dlc.location_category = %(location_category_filter)s"
            params['location_category_filter'] = location_category_filter
        
        if crime_category_filter:
            query += " AND dcc.crime_category = %(crime_category_filter)s"
            params['crime_category_filter'] = crime_category_filter
        
        df = pd.read_sql_query(query, engine, params=params)
        return int(df['total_incidents'].iloc[0]) if not df.empty and df['total_incidents'].iloc[0] is not None else 0
    except Exception as e:
        st.error(f"Error fetching filtered total incidents: {e}")
        return 0