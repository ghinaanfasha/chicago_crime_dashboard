import streamlit as st
from database.connection import test_database_connection
from views import overview, time_trends, geographic
from styles.custom_css import apply_custom_styles

st.set_page_config(
    page_title="Chicago Crime Analytics", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Chicago Crime Analytics Dashboard\nThis is a responsive crime analytics dashboard."
    }
)

if "page" not in st.session_state:
    st.session_state.page = "Overview"

apply_custom_styles()

def create_mobile_menu():
    """Create a mobile-friendly menu"""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected = st.selectbox(
            "Navigate to:",
            ["Overview", "Time Trends", "Geographic"],
            index=["Overview", "Time Trends", "Geographic"].index(st.session_state.page),
            key="mobile_nav"
        )
        if selected != st.session_state.page:
            st.session_state.page = selected
            st.rerun()

def is_mobile():
    """Simple mobile detection based on sidebar state"""
    return st.session_state.get('mobile_mode', False)

# Sidebar menu 
with st.sidebar:
    st.markdown("### Navigation")

    nav_container = st.container()
    with nav_container:
        if st.button("Overview", key="overview", use_container_width=True):
            st.session_state.page = "Overview"
            st.rerun()
            
        if st.button("Time Trends", key="time", use_container_width=True):
            st.session_state.page = "Time Trends"
            st.rerun()
            
        if st.button("Geographic", key="geo", use_container_width=True):
            st.session_state.page = "Geographic"
            st.rerun()

    st.markdown("---")
    st.markdown("### Database")
    if st.button("🔗 Test Connection", key="test_db", use_container_width=True):
        with st.spinner("Testing connection..."):
            test_database_connection()

# Content
page = st.session_state.page

title_container = st.container()
with title_container:
    st.markdown("""
        <div class="main-title-container">
            <h1 class="main-title">
                Chicago Crime Analytics Dashboard
            </h1>
        </div>
    """, unsafe_allow_html=True)

def render_page_subtitle(subtitle):
    st.markdown(f"""
        <div class="page-subtitle-container">
            <h2 class="page-subtitle">
                {subtitle}
            </h2>
        </div>
    """, unsafe_allow_html=True)

# Route
try:
    if page == "Overview":
        render_page_subtitle("Overview")
        overview.show()
    elif page == "Time Trends":
        render_page_subtitle("Time Trends")
        time_trends.show()
    elif page == "Geographic":
        render_page_subtitle("Geographic Distribution")
        geographic.show()
    else:
        st.error("Page not found!")
        st.session_state.page = "Overview"
        st.rerun()
        
except Exception as e:
    st.error(f"An error occurred while loading the page: {str(e)}")
    st.info("Please try refreshing the page or contact support if the problem persists.")

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])
with footer_col2:
    st.markdown("""
        <div style="text-align: center; color: #666; font-size: clamp(0.7rem, 1.5vw, 0.9rem);">
            <p>© 2025 Chicago Crime Analytics Dashboard | Built with Streamlit</p>
        </div>
    """, unsafe_allow_html=True)