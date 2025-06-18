import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Koneksi DB
@st.cache_resource
def init_connection():
    try:
        DB_CONFIG = {
            'host': st.secrets["postgres"]["host"],
            'port': st.secrets["postgres"]["port"],
            'database': st.secrets["postgres"]["database"],
            'user': st.secrets["postgres"]["user"],
            'password': st.secrets["postgres"]["password"]
        }
        
        connection_string = f"postgresql://{DB_CONFIG['user']}:{quote_plus(DB_CONFIG['password'])}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        engine = create_engine(connection_string)
        return engine
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

# Query
@st.cache_data(ttl=600) 
def run_query(query, params=None):
    """Menjalankan query SQL dan mengembalikan DataFrame"""
    try:
        engine = init_connection()
        if engine is None:
            return None
        
        if params:
            df = pd.read_sql_query(query, engine, params=params)
        else:
            df = pd.read_sql_query(query, engine)
        return df
    except Exception as e:
        st.error(f"Error executing query: {e}")
        return None

# Tabel
@st.cache_data(ttl=3600)  
def get_table_info():
    """Mendapatkan informasi tentang tabel-tabel dalam database"""
    query = """
    SELECT table_name, column_name, data_type 
    FROM information_schema.columns 
    WHERE table_schema = 'public' 
    ORDER BY table_name, ordinal_position;
    """
    return run_query(query)

# Daftar tabel
@st.cache_data(ttl=3600)
def get_tables():
    """Mendapatkan daftar nama tabel"""
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name;
    """
    return run_query(query)

# Test koneksi db
def test_database_connection():
    """Test koneksi database dan tampilkan status"""
    engine = init_connection()
    if engine:
        try:
            # Test query
            test_query = "SELECT 1 as test"
            result = run_query(test_query)
            if result is not None:
                st.success("✅ Database connected successfully!")

                tables = get_tables()
                if tables is not None and not tables.empty:
                    st.info(f"📊 Found {len(tables)} tables: {', '.join(tables['table_name'].tolist())}")
                return True
            else:
                st.error("❌ Failed to execute test query")
                return False
        except Exception as e:
            st.error(f"❌ Database connection test failed: {e}")
            return False
    else:
        st.error("❌ Could not establish database connection")
        return False