import requests
from typing import Dict, Any, Optional
from config import API_BASE_URL


class APIClient:
    """API client for backend communication"""
    
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Make HTTP request to API"""
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_health(self) -> Optional[Dict[str, Any]]:
        """Get health status"""
        return self._make_request("GET", "/health")
    
    def get_progress_status(self) -> Optional[Dict[str, Any]]:
        """Get progress status"""
        return self._make_request("GET", "/progress/status")
    
    def get_daily_plan(self, day: int) -> Optional[Dict[str, Any]]:
        """Get daily study plan"""
        return self._make_request("GET", f"/progress/plan/{day}")
    
    def get_analytics(self) -> Optional[Dict[str, Any]]:
        """Get progress analytics"""
        return self._make_request("GET", "/progress/analytics")
    
    def send_chat_message(self, message: str, topic_category: str) -> Optional[Dict[str, Any]]:
        """Send chat message to AI"""
        payload = {
            "message": message,
            "topic_category": topic_category
        }
        return self._make_request("POST", "/chat", json=payload)
    
    def log_progress(self, day: int, plan: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Log daily progress"""
        payload = {
            "day": day,
            "topics": plan["topics"],
            "notes": f"Completed day {day} study plan",
            "hours_studied": plan["estimated_hours"],
            "problems_solved": len(plan["practice_problems"]),
            "confidence_level": 8
        }
        return self._make_request("POST", "/progress/daily", json=payload)


# Global API client instance
api_client = APIClient()
