import streamlit as st
import pandas as pd
from database.connection import init_connection

def get_total_cases():
    """Get total number of cases"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        query = "SELECT SUM(crime_facts.incident_count) AS total_incidents FROM crime_facts;"
        df = pd.read_sql_query(query, engine)
        return int(df['total_incidents'].iloc[0]) if not df.empty and df['total_incidents'].iloc[0] is not None else 0
    except Exception as e:
        st.error(f"Error fetching total cases: {e}")
        return 0

def get_common_crime():
    """Get most common crime type"""
    engine = init_connection()
    if engine is None:
        return {"primary_type": "N/A", "incident_count": 0}
    
    try:
        query = """
        SELECT crime_facts.id_crime, dim_crime.primary_type, COUNT(*) AS incident_count
        FROM crime_facts
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        GROUP BY crime_facts.id_crime, dim_crime.primary_type
        ORDER BY incident_count DESC
        LIMIT 1;
        """
        df = pd.read_sql_query(query, engine)
        if not df.empty:
            return {
                "primary_type": df['primary_type'].iloc[0],
                "incident_count": int(df['incident_count'].iloc[0])
            }
        return {"primary_type": "N/A", "incident_count": 0}
    except Exception as e:
        st.error(f"Error fetching common crime: {e}")
        return {"primary_type": "N/A", "incident_count": 0}

def get_trend_case():
    """Get trending case for current month"""
    engine = init_connection()
    if engine is None:
        return {"primary_type": "N/A", "month": 0, "year": 0}
    
    try:
        query = """
        SELECT 
            dim_crime.primary_type, dim_date.month, dim_date.year,
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE dim_date.month = EXTRACT(MONTH FROM CURRENT_DATE)
          AND dim_date.year = EXTRACT(YEAR FROM CURRENT_DATE)
        GROUP BY dim_crime.primary_type, dim_date.month, dim_date.year
        ORDER BY total_incidents DESC
        LIMIT 1;
        """
        df = pd.read_sql_query(query, engine)
        if not df.empty:
            return {
                "primary_type": df['primary_type'].iloc[0],
                "month": int(df['month'].iloc[0]),
                "year": int(df['year'].iloc[0])
            }
        return {"primary_type": "N/A", "month": 0, "year": 0}
    except Exception as e:
        st.error(f"Error fetching trend case: {e}")
        return {"primary_type": "N/A", "month": 0, "year": 0}

def get_arrest_rate():
    """Get overall arrest rate percentage"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        query = """
        SELECT 
            ROUND(
                100.0 * SUM(CASE WHEN arrest_status = TRUE THEN 1 ELSE 0 END) / COUNT(*), 
                2
            ) AS arrest_true_percentage
        FROM crime_facts;
        """
        df = pd.read_sql_query(query, engine)
        return float(df['arrest_true_percentage'].iloc[0]) if not df.empty and df['arrest_true_percentage'].iloc[0] is not None else 0
    except Exception as e:
        st.error(f"Error fetching arrest rate: {e}")
        return 0
    
def get_crime_history_data():
    """Get total cases per year for crime history chart including arrest data"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dim_date.year,
            SUM(crime_facts.incident_count) AS total_cases,
            SUM(CASE WHEN crime_facts.arrest_status = TRUE THEN crime_facts.incident_count ELSE 0 END) AS arrested_cases
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        GROUP BY dim_date.year
        ORDER BY dim_date.year;
        """
        df = pd.read_sql_query(query, engine)
        df = df.rename(columns={
            'year': 'Year', 
            'total_cases': 'Total Crime',
            'arrested_cases': 'Arrested Cases'
        })
        return df
    except Exception as e:
        st.error(f"Error fetching crime history data: {e}")
        return pd.DataFrame()

def get_arrest_rates_by_category():
    """Get arrest rate for each crime category"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            cc.crime_category,
            ROUND(100.0 * SUM(CASE WHEN cf.arrest_status = true THEN cf.incident_count ELSE 0 END) 
                      / NULLIF(SUM(cf.incident_count), 0), 2) AS arrest_rate_percentage
        FROM crime_facts cf
        JOIN dim_crime c ON cf.id_crime = c.id_crime
        JOIN dim_crime_category cc ON cc.id_crime_category = c.id_crime_category
        GROUP BY cc.crime_category
        ORDER BY arrest_rate_percentage DESC;
        """
        df = pd.read_sql_query(query, engine)
        df = df.rename(columns={'crime_category': 'Crime Type', 'arrest_rate_percentage': 'Arrest Rate'})
        return df
    except Exception as e:
        st.error(f"Error fetching arrest rates by category: {e}")
        return pd.DataFrame()

def get_cases_by_category():
    """Get total cases for each crime category"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dim_crime_category.crime_category,
            SUM(crime_facts.incident_count) AS total_cases
        FROM crime_facts
        JOIN dim_crime ON crime_facts.id_crime = dim_crime.id_crime
        JOIN dim_crime_category ON dim_crime_category.id_crime_category = dim_crime.id_crime_category
        GROUP BY dim_crime_category.id_crime_category, dim_crime_category.crime_category
        ORDER BY total_cases DESC;
        """
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        st.error(f"Error fetching cases by category: {e}")
        return pd.DataFrame()

def get_domestic_status_by_category():
    """Get domestic status comparison per crime category"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            cc.crime_category,
            SUM(CASE WHEN cf.domestic_status = true THEN cf.incident_count ELSE 0 END) AS domestic_cases,
            SUM(CASE WHEN cf.domestic_status = false THEN cf.incident_count ELSE 0 END) AS non_domestic_cases,
            SUM(cf.incident_count) AS total_cases
        FROM crime_facts cf
        JOIN dim_crime c ON cf.id_crime = c.id_crime
        JOIN dim_crime_category cc ON cc.id_crime_category = c.id_crime_category
        GROUP BY cc.crime_category
        ORDER BY total_cases DESC;
        """
        df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        st.error(f"Error fetching domestic status by category: {e}")
        return pd.DataFrame()