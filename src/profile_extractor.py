import re
import json
import logging
from typing import Dict
from groq import Groq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProfileExtractor:
    """Extract user profile from natural language"""
    
    PROFILE_CACHE = {}
    
    PATTERNS = {
        'age': re.compile(r'(\d{1,2})\s*(?:year|yr|years old|age)', re.I),
        'income': re.compile(r'₹?\s*(\d+)\s*(?:lakh|lac|k|thousand|cr)', re.I),
        'state': re.compile(r'\b(' + '|'.join([
            'karnataka', 'tamil nadu', 'telangana', 'maharashtra', 'delhi',
            'uttar pradesh', 'west bengal', 'gujarat', 'rajasthan', 'punjab',
            'bihar', 'madhya pradesh', 'kerala', 'haryana', 'odisha'
        ]) + r')\b', re.I),
    }
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.model = "llama-3.3-70b-versatile"
        logger.info("ProfileExtractor initialized")
    
    def extract(self, query: str, use_cache: bool = True) -> Dict:
        """Extract profile with caching"""
        
        if use_cache and query in self.PROFILE_CACHE:
            logger.info("Cache hit for profile")
            return self.PROFILE_CACHE[query]
        
        logger.info("Extracting profile from query")
        
        profile = self._extract_with_groq(query)
        
        if not profile or not any(profile.values()):
            logger.warning("Groq extraction incomplete, using regex")
            profile = self._extract_with_regex(query)
        
        self.PROFILE_CACHE[query] = profile
        return profile
    
    def _extract_with_groq(self, query: str) -> Dict:
        """Extract profile using Groq"""
        
        system_msg = "Extract user information. Return only valid JSON."
        user_msg = f"""Extract from: "{query}"
Return JSON with: age, gender, occupation, state, income, category
Use null for missing values."""

        try:
            msg = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg}
                ],
                temperature=0.1,
                max_tokens=150,
            )
            
            response = msg.choices[0].message.content
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            
            if json_match:
                profile = json.loads(json_match.group())
                return self._validate_profile(profile)
        
        except Exception as e:
            logger.warning(f"Groq extraction error: {e}")
        
        return {}
    
    def _extract_with_regex(self, query: str) -> Dict:
        """Fallback regex extraction"""
        
        query_lower = query.lower()
        profile = {
            "age": None,
            "gender": None,
            "occupation": None,
            "state": None,
            "income": None,
            "category": None
        }
        
        match = self.PATTERNS['age'].search(query_lower)
        if match:
            profile["age"] = int(match.group(1))
        
        if re.search(r'\b(female|woman|girl)\b', query_lower):
            profile["gender"] = "female"
        elif re.search(r'\b(male|man|boy)\b', query_lower):
            profile["gender"] = "male"
        
        occupation_map = {
            r'student': 'student',
            r'employed|job|working': 'employed',
            r'self-employed|business': 'self-employed',
            r'retired': 'retired',
        }
        for pattern, label in occupation_map.items():
            if re.search(pattern, query_lower):
                profile["occupation"] = label
                break
        
        match = self.PATTERNS['state'].search(query_lower)
        if match:
            profile["state"] = match.group(1).lower()
        
        match = self.PATTERNS['income'].search(query_lower)
        if match:
            amount = int(match.group(1))
            if re.search(r'lakh|lac', query_lower):
                profile["income"] = amount * 100000
            elif re.search(r'crore', query_lower):
                profile["income"] = amount * 10000000
            else:
                profile["income"] = amount * 1000
        
        if re.search(r'\bsc\b', query_lower):
            profile["category"] = "SC"
        elif re.search(r'\bst\b', query_lower):
            profile["category"] = "ST"
        elif re.search(r'\bobc\b', query_lower):
            profile["category"] = "OBC"
        
        return profile
    
    def _validate_profile(self, profile: Dict) -> Dict:
        """Validate profile fields"""
        
        validated = {
            "age": None,
            "gender": None,
            "occupation": None,
            "state": None,
            "income": None,
            "category": None
        }
        
        if profile.get('age'):
            try:
                age = int(profile['age'])
                if 0 < age < 150:
                    validated['age'] = age
            except:
                pass
        
        if profile.get('gender'):
            g = str(profile['gender']).lower()
            if g in ['male', 'female']:
                validated['gender'] = g
        
        if profile.get('occupation'):
            o = str(profile['occupation']).lower()
            if o in ['student', 'employed', 'self-employed', 'retired']:
                validated['occupation'] = o
        
        if profile.get('state'):
            validated['state'] = str(profile['state']).lower()
        
        if profile.get('income'):
            try:
                income = int(profile['income'])
                if 0 < income < 100000000:
                    validated['income'] = income
            except:
                pass
        
        if profile.get('category'):
            c = str(profile['category']).upper()
            if c in ['SC', 'ST', 'OBC']:
                validated['category'] = c
        
        return validated