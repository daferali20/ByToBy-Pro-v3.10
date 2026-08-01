import streamlit as st
from backend.services import portfolio_service, watchlist_service
from backend.websocket import stream_manager

def main():
    st.set_page_config(
        page_title="ByToBy-Pro-v3",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Session state initialization
    initialize_session_state()
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", [
        "Dashboard", "AI Scanner", "Explosion Scanner", 
        "Smart Money", "Stock Analysis", "Market Overview",
        "Heatmap", "News AI", "Alerts", "Settings"
    ])
    
    # Page routing
    if page == "Dashboard":
        from pages.dashboard import show
    elif page == "AI Scanner":
        from pages.ai_scanner import show
    # ... etc
