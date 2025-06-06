import openai
import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMHandler:
    def __init__(self):
        """Initialize the LLM handler with OpenRouter API key."""
        self.client = openai.OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv('OPENROUTER_API_KEY')
        )
        
    def parse_query(self, user_query: str) -> Dict[str, Any]:
        """
        Parse a natural language query into structured criteria.
        
        Args:
            user_query: Natural language query from user
            
        Returns:
            Dictionary with parsed criteria
        """
        
        system_prompt = """
You are a helpful assistant that parses shopping queries into structured data.

Extract the following information from the user's query and return it as a JSON object:
- category: type of product (dress, jeans, shirt, shoes, jacket, etc.)
- color: color preference 
- price_max: maximum price (extract numbers like $200, under 100, etc.)
- price_min: minimum price
- rating_min: minimum rating (if mentioned)

Rules:
1. Only include fields that are explicitly mentioned or clearly implied
2. For colors, use simple color names (red, blue, green, etc.)
3. For categories, use singular form (dress not dresses, shoe not shoes)
4. For prices, extract just the numeric value
5. If no specific criteria are mentioned, return an empty object {}

Examples:
- "Show me red dresses under $200" → {"category": "dress", "color": "red", "price_max": 200}
- "I want blue jeans" → {"category": "jeans", "color": "blue"}
- "Find shoes with good ratings" → {"category": "shoes", "rating_min": 4.0}
- "Something cheap" → {"price_max": 50}

Return only the JSON object, no other text.
"""

        try:
            response = self.client.chat.completions.create(
                model="openai/gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to parse the JSON response
            try:
                criteria = json.loads(result_text)
                return criteria if isinstance(criteria, dict) else {}
            except json.JSONDecodeError:
                # Fallback: try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
                return {}
                
        except Exception as e:
            print(f"Error calling OpenRouter API: {e}")
            # Fallback to simple keyword parsing
            return self._fallback_parse(user_query)
    
    def _fallback_parse(self, query: str) -> Dict[str, Any]:
        """
        Fallback parsing method using simple keyword matching.
        
        Args:
            query: User query string
            
        Returns:
            Dictionary with basic parsed criteria
        """
        query_lower = query.lower()
        criteria = {}
        
        # Simple color detection
        colors = ['red', 'blue', 'green', 'black', 'white', 'pink', 'yellow', 'purple', 'orange', 'brown', 'grey', 'gray', 'navy']
        for color in colors:
            if color in query_lower:
                criteria['color'] = color
                break
        
        # Simple category detection
        categories = {
            'dress': ['dress', 'gown'],
            'jeans': ['jeans', 'denim'],
            'shirt': ['shirt', 'blouse', 'top'],
            'shoes': ['shoes', 'sneakers', 'boots'],
            'jacket': ['jacket', 'blazer', 'coat']
        }
        
        for category, keywords in categories.items():
            if any(keyword in query_lower for keyword in keywords):
                criteria['category'] = category
                break
        
        # Simple price detection
        import re
        price_match = re.search(r'\$?(\d+)', query)
        if price_match:
            price = float(price_match.group(1))
            if 'under' in query_lower or 'below' in query_lower or 'less than' in query_lower:
                criteria['price_max'] = price
            elif 'over' in query_lower or 'above' in query_lower or 'more than' in query_lower:
                criteria['price_min'] = price
            else:
                criteria['price_max'] = price  # Default to max price
        
        return criteria
    
    def generate_search_summary(self, criteria: Dict[str, Any], query: str) -> str:
        """
        Generate a summary of what the system understood from the query.
        
        Args:
            criteria: Parsed criteria dictionary
            query: Original user query
            
        Returns:
            Summary string
        """
        if not criteria:
            return f"Searching for: '{query}' (showing all products)"
        
        parts = []
        if criteria.get('category'):
            parts.append(f"Category: {criteria['category']}")
        if criteria.get('color'):
            parts.append(f"Color: {criteria['color']}")
        if criteria.get('price_max'):
            parts.append(f"Max price: ${criteria['price_max']}")
        if criteria.get('price_min'):
            parts.append(f"Min price: ${criteria['price_min']}")
        if criteria.get('rating_min'):
            parts.append(f"Min rating: {criteria['rating_min']}")
        
        return "Searching for: " + " | ".join(parts) 