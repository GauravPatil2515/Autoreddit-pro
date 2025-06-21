"""
Utility functions
"""
import re
from typing import Dict, Optional, List

def validate_medium_url(url: str) -> bool:
    if not url:
        return False
    # Accept specific tech/blog domains only
    valid_domains = [
        "medium.com", "towardsdatascience.com", "hackernoon.com", 
        "dev.to", "substack.com"
    ]
    url_lower = url.lower()
    # Check if URL contains valid domains and has proper structure
    has_valid_domain = any(domain in url_lower for domain in valid_domains)
    has_blog_pattern = "blog." in url_lower and (".com" in url_lower or ".org" in url_lower)
    
    return has_valid_domain or has_blog_pattern

def extract_article_info(url: str) -> Optional[Dict]:
    return {
        "title": "Sample Article",
        "description": "This is a sample article description",
        "url": url
    }

def validate_subreddit_list(subreddits: str) -> List[str]:
    if not subreddits:
        return []
    return [s.strip() for s in subreddits.split(",") if s.strip()]

def get_optimal_posting_time() -> str:
    return "Now"

def calculate_random_delay(min_minutes: int = 30, max_minutes: int = 180) -> int:
    import random
    return random.randint(min_minutes, max_minutes)
