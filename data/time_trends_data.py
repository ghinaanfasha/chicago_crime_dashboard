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

def get_risky_time_by_date_range(start_date, end_date):
    """Get risky time within date range"""
    engine = init_connection()
    if engine is None:
        return {"daytime": "N/A", "total_incidents": 0}
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            dim_date.daytime, 
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_date.daytime
        ORDER BY total_incidents DESC
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
            return {
                "daytime": df['daytime'].iloc[0],
                "total_incidents": int(df['total_incidents'].iloc[0])
            }
        return {"daytime": "N/A", "total_incidents": 0}
    except Exception as e:
        st.error(f"Error fetching risky time: {e}")
        return {"daytime": "N/A", "total_incidents": 0}

def get_risky_day_by_date_range(start_date, end_date):
    """Get risky day within date range"""
    engine = init_connection()
    if engine is None:
        return {"weekday": "N/A", "total_incidents": 0}
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            dim_date.weekday, 
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_date.weekday
        ORDER BY total_incidents DESC
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
            return {
                "weekday": df['weekday'].iloc[0],
                "total_incidents": int(df['total_incidents'].iloc[0])
            }
        return {"weekday": "N/A", "total_incidents": 0}
    except Exception as e:
        st.error(f"Error fetching risky day: {e}")
        return {"weekday": "N/A", "total_incidents": 0}

def get_risky_month_by_date_range(start_date, end_date):
    """Get risky month within date range"""
    engine = init_connection()
    if engine is None:
        return {"month_name": "N/A", "total_incidents": 0}
    
    try:
        start_year = start_date.year
        start_month = start_date.month
        start_day = start_date.day
        end_year = end_date.year
        end_month = end_date.month
        end_day = end_date.day
        
        query = """
        SELECT 
            CASE dim_date.month
                WHEN 1 THEN 'Januari'
                WHEN 2 THEN 'Februari'
                WHEN 3 THEN 'Maret'
                WHEN 4 THEN 'April'
                WHEN 5 THEN 'Mei'
                WHEN 6 THEN 'Juni'
                WHEN 7 THEN 'Juli'
                WHEN 8 THEN 'Agustus'
                WHEN 9 THEN 'September'
                WHEN 10 THEN 'Oktober'
                WHEN 11 THEN 'November'
                WHEN 12 THEN 'Desember'
            END AS month_name,
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_date.month
        ORDER BY total_incidents DESC
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
            return {
                "month_name": df['month_name'].iloc[0],
                "total_incidents": int(df['total_incidents'].iloc[0])
            }
        return {"month_name": "N/A", "total_incidents": 0}
    except Exception as e:
        st.error(f"Error fetching risky month: {e}")
        return {"month_name": "N/A", "total_incidents": 0}
    
def get_crime_by_time_of_day(start_date, end_date):
    """Get crime distribution by time of day within date range"""
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
            dim_date.daytime,
            SUM(crime_facts.incident_count) AS total_cases
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE (dim_date.year > %(start_year)s OR 
               (dim_date.year = %(start_year)s AND dim_date.month > %(start_month)s) OR
               (dim_date.year = %(start_year)s AND dim_date.month = %(start_month)s AND dim_date.day >= %(start_day)s))
        AND (dim_date.year < %(end_year)s OR 
             (dim_date.year = %(end_year)s AND dim_date.month < %(end_month)s) OR
             (dim_date.year = %(end_year)s AND dim_date.month = %(end_month)s AND dim_date.day <= %(end_day)s))
        GROUP BY dim_date.daytime
        ORDER BY 
            CASE dim_date.daytime 
                WHEN 'Dini hari' THEN 1
                WHEN 'Pagi' THEN 2
                WHEN 'Siang' THEN 3
                WHEN 'Sore' THEN 4
                WHEN 'Malam' THEN 5
            END
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
        st.error(f"Error fetching crime by time of day: {e}")
        return pd.DataFrame()

def get_crime_by_day_of_week(start_date, end_date):
    """Get crime distribution by day of week within date range"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dim_date.weekday,
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE MAKE_DATE(dim_date.year, dim_date.month, dim_date.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY dim_date.weekday
        ORDER BY 
            CASE dim_date.weekday 
                WHEN 'Senin' THEN 1
                WHEN 'Selasa' THEN 2
                WHEN 'Rabu' THEN 3
                WHEN 'Kamis' THEN 4
                WHEN 'Jumat' THEN 5
                WHEN 'Sabtu' THEN 6
                WHEN 'Minggu' THEN 7
            END
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime by day of week: {e}")
        return pd.DataFrame()

def get_crime_by_month(start_date, end_date):
    """Get crime distribution by month within date range (aggregated across years)"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            CASE dim_date.month
                WHEN 1 THEN 'Januari'
                WHEN 2 THEN 'Februari'
                WHEN 3 THEN 'Maret'
                WHEN 4 THEN 'April'
                WHEN 5 THEN 'Mei'
                WHEN 6 THEN 'Juni'
                WHEN 7 THEN 'Juli'
                WHEN 8 THEN 'Agustus'
                WHEN 9 THEN 'September'
                WHEN 10 THEN 'Oktober'
                WHEN 11 THEN 'November'
                WHEN 12 THEN 'Desember'
            END AS month_name,
            dim_date.month AS month_number,
            SUM(crime_facts.incident_count) AS total_incidents
        FROM crime_facts
        JOIN dim_date ON crime_facts.id_date = dim_date.id_date
        WHERE MAKE_DATE(dim_date.year, dim_date.month, dim_date.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY dim_date.month
        ORDER BY dim_date.month
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime by month: {e}")
        return pd.DataFrame()

def get_crime_category_by_daytime(start_date, end_date):
    """Get crime distribution by category and daytime within date range"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dcc.crime_category,
            dd.daytime,
            SUM(cf.incident_count) AS total_incidents
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE MAKE_DATE(dd.year, dd.month, dd.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY dcc.crime_category, dd.daytime
        ORDER BY 
            CASE dd.daytime 
                WHEN 'Dini hari' THEN 1
                WHEN 'Pagi' THEN 2
                WHEN 'Siang' THEN 3
                WHEN 'Sore' THEN 4
                WHEN 'Malam' THEN 5
            END,
            dcc.crime_category
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime category by daytime: {e}")
        return pd.DataFrame()

def get_crime_category_by_weekday(start_date, end_date):
    """Get crime distribution by category and weekday within date range"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dcc.crime_category,
            dd.weekday,
            SUM(cf.incident_count) AS total_incidents
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE MAKE_DATE(dd.year, dd.month, dd.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY dcc.crime_category, dd.weekday
        ORDER BY 
            CASE dd.weekday 
                WHEN 'Senin' THEN 1
                WHEN 'Selasa' THEN 2
                WHEN 'Rabu' THEN 3
                WHEN 'Kamis' THEN 4
                WHEN 'Jumat' THEN 5
                WHEN 'Sabtu' THEN 6
                WHEN 'Minggu' THEN 7
            END,
            dcc.crime_category
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime category by weekday: {e}")
        return pd.DataFrame()

def get_crime_category_by_month(start_date, end_date):
    """Get crime distribution by category and month within date range"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dcc.crime_category,
            CASE dd.month
                WHEN 1 THEN 'Januari'
                WHEN 2 THEN 'Februari'
                WHEN 3 THEN 'Maret'
                WHEN 4 THEN 'April'
                WHEN 5 THEN 'Mei'
                WHEN 6 THEN 'Juni'
                WHEN 7 THEN 'Juli'
                WHEN 8 THEN 'Agustus'
                WHEN 9 THEN 'September'
                WHEN 10 THEN 'Oktober'
                WHEN 11 THEN 'November'
                WHEN 12 THEN 'Desember'
            END AS month_name,
            dd.month AS month_number,
            SUM(cf.incident_count) AS total_incidents
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE MAKE_DATE(dd.year, dd.month, dd.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        GROUP BY dcc.crime_category, dd.month
        ORDER BY dd.month, dcc.crime_category
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime category by month: {e}")
        return pd.DataFrame()

def get_crime_detail_table(start_date, end_date, month_filter=None, weekday_filter=None, daytime_filter=None, crime_category_filter=None):
    """Get detailed crime data with filters"""
    engine = init_connection()
    if engine is None:
        return pd.DataFrame()
    
    try:
        query = """
        SELECT 
            dlc.location_category,
            dl.location_description,
            dc.primary_type,
            dc.description,
            cf.arrest_status,
            dd.day,
            dd.month,
            dd.year,
            dd.weekday,
            dd.daytime,
            dcc.crime_category
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_location dl ON cf.id_location = dl.id_location
        JOIN dim_location_category dlc ON dl.id_location_category = dlc.id_location_category
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE MAKE_DATE(dd.year, dd.month, dd.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
        
        if month_filter:
            if month_filter.isdigit():
                query += " AND dd.month = %(month_filter)s"
                params['month_filter'] = int(month_filter)
            else:
                month_mapping = {
                    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
                    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8, 
                    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
                }
                if month_filter in month_mapping:
                    query += " AND dd.month = %(month_filter)s"
                    params['month_filter'] = month_mapping[month_filter]
        
        if weekday_filter:
            query += " AND dd.weekday = %(weekday_filter)s"
            params['weekday_filter'] = weekday_filter
        
        if daytime_filter:
            query += " AND dd.daytime = %(daytime_filter)s"
            params['daytime_filter'] = daytime_filter
        
        if crime_category_filter:
            query += " AND dcc.crime_category = %(crime_category_filter)s"
            params['crime_category_filter'] = crime_category_filter
        
        query += " ORDER BY dd.year DESC, dd.month DESC, dd.day DESC LIMIT 1000"
        
        df = pd.read_sql_query(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Error fetching crime detail table: {e}")
        return pd.DataFrame()

def get_months_list():
    """Get list of available months"""
    return ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 
            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

def get_weekdays_list():
    """Get list of available weekdays"""
    return ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']

def get_daytime_list():
    """Get list of available daytime periods"""
    return ['Dini hari', 'Pagi', 'Siang', 'Sore', 'Malam']

def get_crime_categories_list():
    """Get list of available crime categories"""
    engine = init_connection()
    if engine is None:
        return ["Street and Narcotics Crimes", "Battery Crimes", "Burglary", "Theft Crimes", "Property Crimes"]
    
    try:
        query = """
        SELECT DISTINCT crime_category 
        FROM dim_crime_category 
        ORDER BY crime_category
        """
        
        df = pd.read_sql_query(query, engine)
        return df['crime_category'].tolist()
    except Exception as e:
        st.error(f"Error fetching crime categories: {e}")
        return ["Street and Narcotics Crimes", "Battery Crimes", "Burglary", "Theft Crimes", "Property Crimes"]

def get_filtered_total_incidents(start_date, end_date, month_filter=None, weekday_filter=None, daytime_filter=None, crime_category_filter=None):
    """Get total incidents with filters applied (aggregated by incident_count, not row count)"""
    engine = init_connection()
    if engine is None:
        return 0
    
    try:
        query = """
        SELECT 
            SUM(cf.incident_count) AS total_incidents
        FROM crime_facts cf
        JOIN dim_date dd ON cf.id_date = dd.id_date
        JOIN dim_location dl ON cf.id_location = dl.id_location
        JOIN dim_location_category dlc ON dl.id_location_category = dlc.id_location_category
        JOIN dim_crime dc ON cf.id_crime = dc.id_crime
        JOIN dim_crime_category dcc ON dc.id_crime_category = dcc.id_crime_category
        WHERE MAKE_DATE(dd.year, dd.month, dd.day) 
              BETWEEN %(start_date)s AND %(end_date)s
        """
        
        params = {
            'start_date': start_date,
            'end_date': end_date
        }

        if month_filter:
            if month_filter.isdigit():
                query += " AND dd.month = %(month_filter)s"
                params['month_filter'] = int(month_filter)
            else:
                month_mapping = {
                    'Januari': 1, 'Februari': 2, 'Maret': 3, 'April': 4,
                    'Mei': 5, 'Juni': 6, 'Juli': 7, 'Agustus': 8, 
                    'September': 9, 'Oktober': 10, 'November': 11, 'Desember': 12
                }
                if month_filter in month_mapping:
                    query += " AND dd.month = %(month_filter)s"
                    params['month_filter'] = month_mapping[month_filter]
        
        if weekday_filter:
            query += " AND dd.weekday = %(weekday_filter)s"
            params['weekday_filter'] = weekday_filter
        
        if daytime_filter:
            query += " AND dd.daytime = %(daytime_filter)s"
            params['daytime_filter'] = daytime_filter
        
        if crime_category_filter:
            query += " AND dcc.crime_category = %(crime_category_filter)s"
            params['crime_category_filter'] = crime_category_filter
        
        df = pd.read_sql_query(query, engine, params=params)
        return int(df['total_incidents'].iloc[0]) if not df.empty and df['total_incidents'].iloc[0] is not None else 0
    except Exception as e:
        st.error(f"Error fetching filtered total incidents: {e}")
        return 0