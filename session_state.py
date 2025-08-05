import streamlit as st
from typing import List, Dict, Any


class SessionStateManager:
    """Manage Streamlit session state"""
    
    @staticmethod
    def initialize():
        """Initialize session state variables"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        if "current_day" not in st.session_state:
            st.session_state.current_day = 1
        
        if "user_preferences" not in st.session_state:
            st.session_state.user_preferences = {
                "study_hours": 4,
                "difficulty": "Medium",
                "notifications": True
            }
    
    @staticmethod
    def get_chat_history() -> List[Dict[str, Any]]:
        """Get chat history"""
        return st.session_state.get("chat_history", [])
    
    @staticmethod
    def add_chat_message(role: str, content: str):
        """Add message to chat history"""
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.append({
            "role": role,
            "content": content
        })
    
    @staticmethod
    def clear_chat_history():
        """Clear chat history"""
        st.session_state.chat_history = []
    
    @staticmethod
    def get_current_day() -> int:
        """Get current study day"""
        return st.session_state.get("current_day", 1)
    
    @staticmethod
    def set_current_day(day: int):
        """Set current study day"""
        st.session_state.current_day = day
    
    @staticmethod
    def increment_current_day():
        """Increment current study day"""
        current = st.session_state.get("current_day", 1)
        st.session_state.current_day = current + 1
    
    @staticmethod
    def get_user_preferences() -> Dict[str, Any]:
        """Get user preferences"""
        return st.session_state.get("user_preferences", {})
    
    @staticmethod
    def update_user_preferences(preferences: Dict[str, Any]):
        """Update user preferences"""
        st.session_state.user_preferences.update(preferences)
