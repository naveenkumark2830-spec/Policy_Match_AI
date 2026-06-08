import logging
import json
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def save_conversation(conversation_id: str, history: List[Dict], profile: Dict):
    """Save conversation history for reference"""
    data = {
        'conversation_id': conversation_id,
        'history': history,
        'profile': profile
    }
    
    with open(f'conversations/{conversation_id}.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Saved conversation: {conversation_id}")

def format_scheme_summary(schemes: List[Dict]) -> str:
    """Format schemes for context"""
    summary = []
    for scheme in schemes:
        summary.append(scheme['full_scheme'][:200])
    return "\n".join(summary)

def is_followup_question(current_query: str, history: List[Dict]) -> bool:
    """Detect if this is a follow-up question"""
    if not history:
        return False
    
    keywords = ['also', 'what about', 'how about', 'tell me more', 'more details', 
                'explain', 'can i', 'am i eligible', 'when', 'where', 'which one']
    
    return any(keyword in current_query.lower() for keyword in keywords)

def get_context_from_history(history: List[Dict], limit: int = 3) -> str:
    """Get relevant context from conversation history"""
    context = []
    for msg in history[-limit:]:
        if msg['role'] == 'assistant':
            context.append(f"Previous response: {msg['content'][:300]}")
    
    return "\n".join(context)