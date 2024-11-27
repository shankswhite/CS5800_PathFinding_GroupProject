from datetime import datetime, timedelta
import asyncio
from typing import Dict, Optional

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.last_activity: Dict[str, datetime] = {}
        
    def add_session(self, session_id: str, data: dict):
        self.sessions[session_id] = data
        self.last_activity[session_id] = datetime.now()
        
    def get_session(self, session_id: str) -> Optional[dict]:
        if session_id in self.sessions:
            self.last_activity[session_id] = datetime.now()
            return self.sessions[session_id]
        return None
        
    def cleanup_sessions(self):
        current_time = datetime.now()
        expired_sessions = [
            sid for sid, last_active in self.last_activity.items()
            if (current_time - last_active) > timedelta(minutes=10)
        ]
        for sid in expired_sessions:
            del self.sessions[sid]
            del self.last_activity[sid] 