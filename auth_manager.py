import streamlit as st
import requests
from typing import Optional, Dict, Any
from config import API_BASE_URL

class AuthManager:
    def __init__(self):
        self.api_base_url = API_BASE_URL
        
    def register_user(self, email: str, username: str, full_name: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        try:
            response = requests.post(
                f"{self.api_base_url}/auth/register",
                json={
                    "email": email,
                    "username": username,
                    "full_name": full_name,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Registration failed")}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user and get access token"""
        try:
            response = requests.post(
                f"{self.api_base_url}/auth/login",
                json={
                    "email": email,
                    "password": password
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                return {"success": True, "data": token_data}
            else:
                return {"success": False, "error": response.json().get("detail", "Login failed")}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_current_user(self, token: str) -> Dict[str, Any]:
        """Get current user information"""
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{self.api_base_url}/auth/me", headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to get user info"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return "token" in st.session_state and st.session_state.token is not None
    
    def get_token(self) -> Optional[str]:
        """Get current user token"""
        return st.session_state.get("token")
    
    def logout(self):
        """Logout user"""
        if "token" in st.session_state:
            del st.session_state.token
        if "user" in st.session_state:
            del st.session_state.user
        st.rerun() 