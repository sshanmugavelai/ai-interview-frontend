import streamlit as st
import requests
from typing import List, Dict, Any, Optional
from config import API_BASE_URL

class GoalsManager:
    def __init__(self):
        self.api_base_url = API_BASE_URL
        
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers"""
        token = st.session_state.get("token")
        if not token:
            raise Exception("User not authenticated")
        return {"Authorization": f"Bearer {token}"}
    
    def create_goal(self, title: str, description: str, category: str, target_days: int) -> Dict[str, Any]:
        """Create a new learning goal"""
        try:
            headers = self.get_auth_headers()
            response = requests.post(
                f"{self.api_base_url}/goals",
                headers=headers,
                json={
                    "title": title,
                    "description": description,
                    "category": category,
                    "target_days": target_days
                }
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.json().get("detail", "Failed to create goal")}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_user_goals(self) -> Dict[str, Any]:
        """Get all goals for the current user"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(f"{self.api_base_url}/goals", headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to fetch goals"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_goal(self, goal_id: int) -> Dict[str, Any]:
        """Get a specific goal"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(f"{self.api_base_url}/goals/{goal_id}", headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to fetch goal"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def update_goal(self, goal_id: int, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a goal"""
        try:
            headers = self.get_auth_headers()
            response = requests.put(
                f"{self.api_base_url}/goals/{goal_id}",
                headers=headers,
                json=updates
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to update goal"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_daily_plan(self, goal_id: int, day: int) -> Dict[str, Any]:
        """Get AI-generated daily plan"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(
                f"{self.api_base_url}/goals/{goal_id}/plan/{day}",
                headers=headers
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to generate plan"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def log_progress(self, goal_id: int, day: int, topics_covered: List[str], 
                    hours_studied: float, problems_solved: int, 
                    confidence_level: int, notes: str = "") -> Dict[str, Any]:
        """Log daily progress"""
        try:
            headers = self.get_auth_headers()
            response = requests.post(
                f"{self.api_base_url}/progress",
                headers=headers,
                json={
                    "goal_id": goal_id,
                    "day": day,
                    "topics_covered": topics_covered,
                    "hours_studied": hours_studied,
                    "problems_solved": problems_solved,
                    "confidence_level": confidence_level,
                    "notes": notes
                }
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to log progress"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_goal_progress(self, goal_id: int) -> Dict[str, Any]:
        """Get progress history for a goal"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(
                f"{self.api_base_url}/goals/{goal_id}/progress",
                headers=headers
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to fetch progress"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def chat_with_ai(self, goal_id: int, message: str) -> Dict[str, Any]:
        """Chat with AI learning coach"""
        try:
            headers = self.get_auth_headers()
            response = requests.post(
                f"{self.api_base_url}/chat",
                headers=headers,
                json={
                    "message": message,
                    "goal_id": goal_id
                }
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to get AI response"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"}
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get user analytics"""
        try:
            headers = self.get_auth_headers()
            response = requests.get(f"{self.api_base_url}/analytics", headers=headers)
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": "Failed to fetch analytics"}
        except Exception as e:
            return {"success": False, "error": f"Connection error: {str(e)}"} 