import os

# API Configuration
API_BASE_URL = os.getenv("BACKEND_URL", "https://ai-interview-assistant-rjve.onrender.com")

# Page Configuration
PAGE_CONFIG = {
    "page_title": "AI Interview Assistant",
    "page_icon": "🧠",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        transition: width 0.3s ease;
    }
</style>
"""

# Topic Categories
TOPIC_CATEGORIES = ["general", "dsa", "ml", "system_design", "behavioral"]

# Study Plan Configuration
STUDY_PLAN_DAYS = 45
DEFAULT_STUDY_HOURS = 4
