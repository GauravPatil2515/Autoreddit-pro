"""
Groq AI Client for Reddit Post Generation
"""
import os
import time
import logging
from typing import Dict, Optional
from dataclasses import dataclass

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None

@dataclass
class PostGenerationResult:
    title: str = ""
    body: str = ""
    success: bool = False
    model_used: str = ""
    generation_time: float = 0.0
    token_count: int = 0
    error_message: Optional[str] = None

class GroqAIClient:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY required")
        if not GROQ_AVAILABLE:
            raise ImportError("Groq library not installed")
        self.client = Groq(api_key=self.api_key)
        self.default_model = os.getenv("DEFAULT_AI_MODEL", "llama-3.3-70b-versatile")
    
    def generate_reddit_post(self, medium_link: str, summary: str, subreddit: str, style: str = "discussion") -> PostGenerationResult:
        start_time = time.time()
        try:
            prompt = f"""Create a Reddit post for r/{subreddit} about this Medium article:

Article: {medium_link}
Summary: {summary}

Generate:
TITLE: [engaging title under 300 chars]
BODY: [discussion-focused post body]

Keep it natural and community-focused."""
            response = self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            result_text = response.choices[0].message.content
            title, body = self._parse_response(result_text)
            token_count = getattr(response.usage, 'total_tokens', 0) if hasattr(response, 'usage') else 0
            return PostGenerationResult(
                title=title,
                body=body,
                success=True,
                model_used=self.default_model,
                generation_time=time.time() - start_time,
                token_count=token_count
            )
        except Exception as e:
            return PostGenerationResult(
                success=False,
                error_message=str(e),
                generation_time=time.time() - start_time
            )
    
    def generate_post(self, article_url: str, article_title: str, article_summary: str, subreddit: str = "programming") -> Dict:
        """Generate a post for the given article - compatible with both old and new interfaces"""
        result = self.generate_reddit_post(article_url, article_summary, subreddit)
        
        return {
            "title": result.title,
            "content": result.body,
            "success": result.success,
            "error": result.error_message
        }
    
    def _parse_response(self, text: str) -> tuple:
        import re
        title_match = re.search(r'TITLE:\s*(.+)', text)
        body_match = re.search(r'BODY:\s*(.+)', text, re.DOTALL)
        title = title_match.group(1).strip() if title_match else "Article Discussion"
        body = body_match.group(1).strip() if body_match else text
        return title, body

# Global instance
_ai_client = None

def get_ai_client():
    """Get the global AI client instance"""
    global _ai_client
    if _ai_client is None:
        try:
            _ai_client = GroqAIClient()
        except Exception as e:
            print(f"Warning: Could not initialize AI client: {e}")
            return None
    return _ai_client
