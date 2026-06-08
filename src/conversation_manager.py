from typing import Dict, List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ConversationManager:
    """Manages multi-turn conversations with history"""
    
    def __init__(self, max_history: int = 10):
        """Initialize conversation manager"""
        self.max_history = max_history
        self.history = []
        self.user_profile = None
        self.conversation_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.context = {}
        
        logger.info("Conversation manager initialized")
    
    def add_user_message(self, message: str) -> None:
        """Add user message to history"""
        self.history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now().isoformat()
        })
        
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-self.max_history:]
        
        logger.info(f"User message added. History size: {len(self.history)}")
    
    def add_assistant_message(self, message: str, metadata: Dict = None) -> None:
        """Add assistant response to history"""
        entry = {
            'role': 'assistant',
            'content': message,
            'timestamp': datetime.now().isoformat()
        }
        
        if metadata:
            entry['metadata'] = metadata
        
        self.history.append(entry)
        logger.info(f"Assistant message added")
    
    def update_profile(self, profile: Dict) -> None:
        """Update user profile"""
        self.user_profile = profile
        logger.info(f"Profile updated: {profile}")
    
    def update_context(self, schemes: List[Dict]) -> None:
        """Update context with retrieved schemes"""
        self.context['schemes'] = schemes
        self.context['last_search'] = datetime.now().isoformat()
        logger.info(f"Context updated with {len(schemes)} schemes")
    
    def get_history_for_llm(self) -> List[Dict]:
        """Get formatted history for LLM context"""
        formatted = []
        
        for msg in self.history[-6:]:
            formatted.append({
                'role': msg['role'],
                'content': msg['content']
            })
        
        return formatted
    
    def get_last_user_message(self) -> str:
        """Get last user message"""
        for msg in reversed(self.history):
            if msg['role'] == 'user':
                return msg['content']
        return ""
    
    def get_conversation_summary(self) -> Dict:
        """Get summary of current conversation"""
        user_messages = [m for m in self.history if m['role'] == 'user']
        assistant_messages = [m for m in self.history if m['role'] == 'assistant']
        
        return {
            'conversation_id': self.conversation_id,
            'total_turns': len(user_messages),
            'profile': self.user_profile,
            'schemes_discussed': self.context.get('schemes', []),
            'message_count': {
                'user': len(user_messages),
                'assistant': len(assistant_messages)
            }
        }
    
    def clear(self) -> None:
        """Clear conversation history"""
        self.history = []
        self.context = {}
        logger.info("Conversation cleared")