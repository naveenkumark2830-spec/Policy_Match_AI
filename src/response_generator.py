import logging
from groq import Groq
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResponseGenerator:
    """Generate responses using Groq"""
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
        logger.info("ResponseGenerator initialized")
    
    def generate(
        self,
        query: str,
        profile: Dict,
        schemes: List[Dict],
        conversation_history: List[Dict] = None
    ) -> str:
        """Generate response"""
        
        logger.info("Generating response")
        
        schemes_text = "\n".join([
            f"{i+1}. {s['full_scheme'][:200]}"
            for i, s in enumerate(schemes[:3])
        ])
        
        history_context = ""
        if conversation_history and len(conversation_history) > 2:
            history_context = "\nPrevious context:\n"
            for msg in conversation_history[-2:]:
                if msg['role'] == 'user':
                    history_context += f"User asked: {msg['content']}\n"
                else:
                    history_context += f"You explained: {msg['content'][:150]}\n"
        
        prompt = f"""You are a helpful government schemes advisor. Provide clear, simple explanations.

User Profile: Age {profile.get('age', '?')}, {profile.get('occupation', 'unknown')}, {profile.get('state', 'unknown')}, Category: {profile.get('category', 'General')}
Current Query: {query}{history_context}

Top Relevant Schemes:
{schemes_text}

Provide:
1. Which schemes best answer their question (2-3 sentences)
2. Key details and benefits
3. Step-by-step how to apply
4. Important eligibility criteria

Keep response clear, practical, and action-oriented."""

        try:
            msg = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=600,
            )
            
            response = msg.choices[0].message.content
            logger.info("Response generated successfully")
            return response
        
        except Exception as e:
            logger.error(f"Generation error: {e}")
            return "Unable to generate response. Please try again."
    
    def answer_followup(
        self,
        question: str,
        previous_response: str,
        schemes: List[Dict]
    ) -> str:
        """Answer follow-up questions"""
        
        logger.info("Answering follow-up question")
        
        schemes_text = "\n".join([s['full_scheme'][:150] for s in schemes[:3]])
        
        prompt = f"""You previously explained: {previous_response[:300]}

User's follow-up question: {question}

Schemes mentioned: {schemes_text}

Provide a focused answer to their follow-up question, building on what was already explained."""

        try:
            msg = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500,
            )
            
            response = msg.choices[0].message.content
            logger.info("Follow-up answer generated")
            return response
        
        except Exception as e:
            logger.error(f"Follow-up generation error: {e}")
            return "Unable to answer. Please ask your question again."