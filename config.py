import os

# API Configuration
API_BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page Configuration
PAGE_CONFIG = {
    "page_title": "AI Learning Assistant",
    "page_icon": "🎯",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Custom CSS Styles
CUSTOM_CSS = """
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .goal-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .progress-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .chat-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    .auth-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin: 0.5rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #5a6fd8 0%, #6a4190 100%);
    }
</style>
"""

# Learning Categories
LEARNING_CATEGORIES = {
    "interview_prep": {
        "name": "Interview Preparation",
        "description": "Prepare for technical and behavioral interviews",
        "icon": "💼",
        "subcategories": ["DSA", "System Design", "Machine Learning", "Behavioral"]
    },
    "language_learning": {
        "name": "Language Learning",
        "description": "Learn new languages and improve communication",
        "icon": "🌍",
        "subcategories": ["Grammar", "Vocabulary", "Conversation", "Writing"]
    },
    "coding": {
        "name": "Programming & Development",
        "description": "Master programming languages and development skills",
        "icon": "💻",
        "subcategories": ["Python", "Web Development", "Data Science", "Algorithms"]
    },
    "fitness": {
        "name": "Health & Fitness",
        "description": "Improve physical health and fitness",
        "icon": "💪",
        "subcategories": ["Strength Training", "Cardio", "Nutrition", "Flexibility"]
    },
    "academic": {
        "name": "Academic Studies",
        "description": "Excel in academic subjects and research",
        "icon": "📚",
        "subcategories": ["Mathematics", "Science", "Literature", "History"]
    }
}

# Default Study Plan Configuration
DEFAULT_STUDY_HOURS = 2
DEFAULT_TARGET_DAYS = 30

# UI Colors
COLORS = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8"
}
