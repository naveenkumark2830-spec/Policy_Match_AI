import os
import logging
from dotenv import load_dotenv
from .conversation_manager import ConversationManager
from .profile_extractor import ProfileExtractor
from .rag_engine import OptimizedRAGEngine
from .response_generator import ResponseGenerator
from .utils import is_followup_question

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

class GovernmentSchemeAssistant:
    """Production assistant with multi-turn conversation"""
    
    def __init__(self):
        logger.info("Initializing Government Scheme Assistant")
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not set in .env")
        
        self.extractor = ProfileExtractor(groq_api_key=groq_key)
        
        base_path = r"D:\GovSchemeAI"
        self.rag = OptimizedRAGEngine(base_path)
        
        self.generator = ResponseGenerator(groq_api_key=groq_key)
        self.conversation = ConversationManager()
        
        logger.info("Assistant initialization complete")
    
    def process_message(self, user_message: str) -> str:
        logger.info(f"Processing: {user_message[:50]}")
        self.conversation.add_user_message(user_message)
        
        if is_followup_question(user_message, self.conversation.history):
            logger.info("Detected follow-up question")
            return self._handle_followup(user_message)
        else:
            logger.info("New question")
            return self._handle_new_question(user_message)
    
    def _handle_new_question(self, user_message: str) -> str:
        logger.info("Handling new question")
        
        profile = self.extractor.extract(user_message)
        self.conversation.update_profile(profile)
        
        schemes = self.rag.search_by_profile(profile, top_k=5)
        self.conversation.update_context(schemes)
        
        response = self.generator.generate(
            user_message,
            profile,
            schemes,
            self.conversation.get_history_for_llm()
        )
        
        self.conversation.add_assistant_message(
            response,
            metadata={'schemes': [s['rank'] for s in schemes]}
        )
        
        return response
    
    def _handle_followup(self, user_message: str) -> str:
        logger.info("Handling follow-up question")
        
        last_response = self._get_last_assistant_message()
        schemes = self.conversation.context.get('schemes', [])
        
        if schemes:
            response = self.generator.answer_followup(
                user_message,
                last_response,
                schemes
            )
        else:
            profile = self.conversation.user_profile or self.extractor.extract(user_message)
            schemes = self.rag.search_by_profile(profile, top_k=5)
            self.conversation.update_context(schemes)
            
            response = self.generator.generate(
                user_message,
                profile,
                schemes,
                self.conversation.get_history_for_llm()
            )
        
        self.conversation.add_assistant_message(response)
        return response
    
    def _get_last_assistant_message(self) -> str:
        for msg in reversed(self.conversation.history):
            if msg['role'] == 'assistant':
                return msg['content']
        return ""
    
    def get_conversation_summary(self) -> dict:
        return self.conversation.get_conversation_summary()


def main():
    print("\n" + "=" * 80)
    print("GOVERNMENT SCHEMES ADVISOR - MULTI-TURN CONVERSATION")
    print("=" * 80)
    print("\nAsk about government schemes. Type 'quit' to exit.")
    print("You can ask follow-up questions anytime.\n")
    
    try:
        assistant = GovernmentSchemeAssistant()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                summary = assistant.get_conversation_summary()
                print(f"\nConversation Summary:")
                print(f"Total questions asked: {summary['total_turns']}")
                print(f"Schemes discussed: {len(summary['schemes_discussed'])}")
                print("\nThank you for using Government Schemes Advisor!")
                break
            
            if user_input.lower() == 'summary':
                summary = assistant.get_conversation_summary()
                print(f"\nCurrent Profile: {summary['profile']}")
                print(f"Messages exchanged: {summary['message_count']}")
                continue
            
            if not user_input:
                continue
            
            response = assistant.process_message(user_input)
            print(f"\nAdvisor: {response}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"\nError occurred: {e}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()