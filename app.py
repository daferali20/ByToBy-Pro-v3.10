"""
ByToBy-Pro-v3 - Main Application Entry Point
A comprehensive financial analysis and trading platform with AI-powered features
"""

import streamlit as st
import os
import sys
from datetime import datetime
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Import configurations
from backend.utils.logging import setup_logging
from backend.services import initialize_services
from backend.database import init_database

# Page configuration
st.set_page_config(
    page_title="ByToBy-Pro-v3 - Trading Analytics Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ByToBy-Pro-v3',
        'Report a bug': 'https://github.com/yourusername/ByToBy-Pro-v3/issues',
        'About': "# ByToBy-Pro-v3\n\nAdvanced Trading Analytics Platform with AI Integration"
    }
)

# Custom CSS
def load_custom_css():
    """Load custom CSS styling"""
    css = """
    <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: 700;
            color: #00ff00;
            background: linear-gradient(90deg, #1a1a2e, #16213e);
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1rem;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
        }
        .sidebar-content {
            padding: 1rem;
        }
        .stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            color: white;
            font-weight: bold;
        }
        .stButton > button:hover {
            transform: scale(1.02);
            transition: all 0.3s ease;
        }
        .success-message {
            background-color: #d4edda;
            color: #155724;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #28a745;
        }
        .warning-message {
            background-color: #fff3cd;
            color: #856404;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #ffc107;
        }
        .info-message {
            background-color: #d1ecf1;
            color: #0c5460;
            padding: 1rem;
            border-radius: 5px;
            border-left: 5px solid #17a2b8;
        }
        .custom-footer {
            text-align: center;
            padding: 2rem;
            margin-top: 2rem;
            border-top: 1px solid #e0e0e0;
            color: #666;
        }
        /* Dark theme overrides */
        .stApp {
            background-color: #0e1117;
        }
        .stSidebar {
            background-color: #1a1a2e;
        }
        .stMarkdown {
            color: #ffffff;
        }
        /* Responsive design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 1.5rem;
            }
        }
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .fade-in {
            animation: fadeIn 0.5s ease-in;
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    defaults = {
        'authenticated': False,
        'user_id': None,
        'username': None,
        'selected_symbols': ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'AMZN'],
        'portfolio_data': {},
        'watchlist': [],
        'alerts': [],
        'theme': 'dark',
        'last_update': datetime.now(),
        'data_refresh_rate': 30,  # seconds
        'risk_tolerance': 'medium',
        'preferred_timeframe': '1D',
        'notification_preferences': {
            'email': True,
            'push': True,
            'sound': False
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Sidebar navigation
def render_sidebar():
    """Render the sidebar navigation"""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h1 style="color: #00ff00; font-size: 2rem;">📈 ByToBy</h1>
            <p style="color: #888;">Professional v3.0</p>
            <hr style="border: 1px solid #333;">
        </div>
        """, unsafe_allow_html=True)
        
        # User authentication status
        if st.session_state.authenticated:
            st.success(f"👤 Welcome, {st.session_state.username}!")
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user_id = None
                st.session_state.username = None
                st.rerun()
        else:
            st.info("🔒 Please login to access all features")
            if st.button("🔑 Login / Register"):
                st.session_state.show_login = True
        
        st.markdown("---")
        
        # Main navigation
        st.markdown("### 🧭 Navigation")
        pages = {
            "📊 Dashboard": "dashboard",
            "🤖 AI Scanner": "ai_scanner",
            "💥 Explosion Scanner": "explosion_scanner",
            "💰 Smart Money": "smart_money",
            "📈 Stock Analysis": "stock_analysis",
            "🌍 Market Overview": "market_overview",
            "🔥 Heatmap": "heatmap",
            "📰 News AI": "news_ai",
            "🔔 Alerts": "alerts",
            "⚙️ Settings": "settings"
        }
        
        # Create navigation buttons
        for label, page_name in pages.items():
            if st.button(label, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.current_page = page_name
                st.rerun()
        
        st.markdown("---")
        
        # Quick actions
        st.markdown("### ⚡ Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.session_state.last_update = datetime.now()
                st.success("Data refreshed!")
        with col2:
            if st.button("📤 Export", use_container_width=True):
                st.info("Exporting data...")
        
        st.markdown("---")
        
        # System status
        st.markdown("### 📡 System Status")
        st.markdown(f"""
        - **Status:** 🟢 Online
        - **Last Update:** {st.session_state.last_update.strftime('%H:%M:%S')}
        - **Symbols Tracked:** {len(st.session_state.selected_symbols)}
        - **Alerts Active:** {len(st.session_state.alerts)}
        """)
        
        st.markdown("---")
        st.caption("© 2026 ByToBy-Pro-v3 | All Rights Reserved")

# Main page router
def render_page(page_name):
    """Render the selected page"""
    try:
        if page_name == "dashboard":
            from pages.dashboard import show
            show()
        elif page_name == "ai_scanner":
            from pages.ai_scanner import show
            show()
        elif page_name == "explosion_scanner":
            from pages.explosion_scanner import show
            show()
        elif page_name == "smart_money":
            from pages.smart_money import show
            show()
        elif page_name == "stock_analysis":
            from pages.stock_analysis import show
            show()
        elif page_name == "market_overview":
            from pages.market_overview import show
            show()
        elif page_name == "heatmap":
            from pages.heatmap import show
            show()
        elif page_name == "news_ai":
            from pages.news_ai import show
            show()
        elif page_name == "alerts":
            from pages.alerts import show
            show()
        elif page_name == "settings":
            from pages.settings import show
            show()
        else:
            st.error(f"Page '{page_name}' not found")
    except ImportError as e:
        st.error(f"Error loading page: {str(e)}")
        st.info("Please ensure all page modules are properly installed")

# Main application
def main():
    """Main application entry point"""
    # Initialize
    load_custom_css()
    initialize_session_state()
    
    # Set default page if not set
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    # Render header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.markdown("### 📈")
    with col2:
        st.markdown("""
        <div class="main-header fade-in" style="text-align: center;">
            ByToBy-Pro-v3 🚀
            <span style="font-size: 1rem; display: block; color: #aaa;">
                Advanced AI-Powered Trading Analytics
            </span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        current_time = datetime.now().strftime("%I:%M %p")
        st.markdown(f"""
        <div style="text-align: right; padding: 1rem;">
            <span style="color: #888;">🕐 {current_time}</span><br>
            <span style="color: #666; font-size: 0.8rem;">{datetime.now().strftime('%B %d, %Y')}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Render sidebar and content
    render_sidebar()
    
    # Main content area
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    render_page(st.session_state.current_page)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="custom-footer">
        <p>⚠️ <strong>Disclaimer:</strong> This platform is for educational and informational purposes only. 
        Not financial advice. Always do your own research before making investment decisions.</p>
        <p style="font-size: 0.8rem;">🚀 Powered by AI | 📊 Real-time Market Data | 💡 Intelligent Insights</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")
