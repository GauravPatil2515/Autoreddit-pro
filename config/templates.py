"""
Post templates for Reddit automation.
Each template includes hooks, placeholders, and call-to-action variations.
Now enhanced with AI integration and fallback templates.
"""

import random
from typing import Dict, List, Optional

# Different opening hooks to make posts feel natural
OPENING_HOOKS = [
    "Just published a new article:",
    "Thoughts on this topic I just wrote about:",
    "I recently explored this interesting concept:",
    "Here's something I've been thinking about lately:",
    "Just shared my perspective on:",
    "Wrote about this fascinating topic:",
    "Been diving deep into this subject:",
    "Wanted to share some insights on:",
    "Recently published my thoughts on:",
    "Here's my take on an important topic:"
]

# Call-to-action variations (soft approach)
CALL_TO_ACTIONS = [
    "Would love to hear your thoughts!",
    "What's your experience with this?",
    "Curious about your perspective on this.",
    "Would appreciate any feedback or insights.",
    "What do you think about this approach?",
    "Anyone else encountered this?",
    "Open to discussion and different viewpoints.",
    "Happy to answer any questions!",
    "Looking forward to the discussion.",
    "What has been your experience?"
]

# Post templates with placeholders
POST_TEMPLATES = [
    {
        "name": "casual_share",
        "title": "{hook} {article_title}",
        "body": "{summary}\n\n{link}\n\n{cta}"
    },
    {
        "name": "discussion_starter",
        "title": "{article_title} - {hook}",
        "body": "I recently wrote about {topic_keyword}:\n\n{summary}\n\nFull article: {link}\n\n{cta}"
    },
    {
        "name": "insight_share",
        "title": "Insights on {topic_keyword}: {article_title}",
        "body": "{hook}\n\n{summary}\n\nRead more: {link}\n\n{cta}"
    },
    {
        "name": "question_based",
        "title": "{article_title}",
        "body": "{hook}\n\n{summary}\n\nI dive deeper into this in my latest article: {link}\n\n{cta}"
    }
]

# AI-Enhanced template styles that work with AI generation
AI_TEMPLATE_STYLES = {
    "discussion_starter": {
        "description": "Opens with engaging question, shares insights, asks for community input",
        "fallback_template": "question_based",
        "ai_prompt_focus": "discussion and engagement"
    },
    "value_first": {
        "description": "Leads with main takeaway, shares actionable points",
        "fallback_template": "insight_share", 
        "ai_prompt_focus": "practical value and actionability"
    },
    "question_based": {
        "description": "Starts with thought-provoking question related to article",
        "fallback_template": "question_based",
        "ai_prompt_focus": "curiosity and community wisdom"
    },
    "story_driven": {
        "description": "Opens with relatable scenario, connects to article theme",
        "fallback_template": "casual_share",
        "ai_prompt_focus": "storytelling and relatability"
    }
}

# Enhanced subreddit configurations for AI context
ENHANCED_SUBREDDIT_CONFIG = {
    "programming": {
        "preferred_hooks": [
            "Just wrote about a coding concept:",
            "Sharing some programming insights:",
            "Explored this development topic:"
        ],
        "topic_keywords": ["coding", "development", "programming", "software"],
        "ai_context": "Technical audience, appreciates code examples and practical solutions",
        "tone": "Professional but approachable, direct communication",
        "avoid": ["Overly promotional language", "Non-technical buzzwords"]
    },
    "webdev": {
        "preferred_hooks": [
            "Web development insights:",
            "Just published about web development:",
            "Sharing some frontend/backend knowledge:"
        ],
        "topic_keywords": ["web development", "frontend", "backend", "JavaScript"],
        "ai_context": "Mix of beginners and experts, show-don't-tell approach works well",
        "tone": "Casual but informative, practical examples appreciated",
        "avoid": ["Overly complex jargon without explanation"]
    },
    "entrepreneur": {
        "preferred_hooks": [
            "Entrepreneurial insights:",
            "Business lessons learned:",
            "Startup experience shared:"
        ],
        "topic_keywords": ["business", "entrepreneurship", "startup", "growth"],
        "ai_context": "Focus on actionable insights and real experiences",
        "tone": "Authentic, lesson-focused, avoid generic advice",
        "avoid": ["Get-rich-quick schemes", "Generic motivational content"]
    },
    "artificial": {
        "preferred_hooks": [
            "AI research insights:",
            "Machine learning findings:",
            "Exploring AI applications:"
        ],
        "topic_keywords": ["artificial intelligence", "machine learning", "AI", "ML"],
        "ai_context": "Technical accuracy crucial, cite sources and methodologies",
        "tone": "Scientific, evidence-based, cite credible sources",
        "avoid": ["Overhyped AI claims", "Non-technical speculation"]
    }
}

def get_random_template():
    """Get a random post template"""
    return random.choice(POST_TEMPLATES)

def get_random_hook(subreddit=None):
    """Get a random opening hook, optionally subreddit-specific"""
    import random
    
    if subreddit and subreddit.lower() in ENHANCED_SUBREDDIT_CONFIG:
        preferred_hooks = ENHANCED_SUBREDDIT_CONFIG[subreddit.lower()]["preferred_hooks"]
        return random.choice(preferred_hooks + OPENING_HOOKS)
    
    return random.choice(OPENING_HOOKS)

def get_random_cta():
    """Get a random call-to-action"""
    import random
    return random.choice(CALL_TO_ACTIONS)

def get_ai_fallback_template(style: str = "discussion_starter") -> Dict:
    """
    Get fallback template when AI generation fails
    
    Args:
        style: AI template style that failed
        
    Returns:
        Template dictionary with fallback content
    """
    style_config = AI_TEMPLATE_STYLES.get(style, AI_TEMPLATE_STYLES["discussion_starter"])
    fallback_name = style_config["fallback_template"]
    
    # Find matching template
    for template in POST_TEMPLATES:
        if template["name"] == fallback_name:
            return template
    
    # Ultimate fallback
    return POST_TEMPLATES[0]

def get_subreddit_ai_context(subreddit: str) -> Dict:
    """
    Get AI context information for specific subreddit
    
    Args:
        subreddit: Target subreddit name
        
    Returns:
        Dictionary with subreddit-specific AI guidance
    """
    subreddit_lower = subreddit.lower()
    
    if subreddit_lower in ENHANCED_SUBREDDIT_CONFIG:
        return ENHANCED_SUBREDDIT_CONFIG[subreddit_lower]
    
    # Default context for unknown subreddits
    return {
        "ai_context": "General Reddit audience, focus on providing value",
        "tone": "Friendly and engaging, avoid overly promotional content",
        "avoid": ["Spam-like behavior", "Excessive self-promotion"]
    }

def generate_fallback_post(
    article_title: str,
    summary: str,
    link: str,
    subreddit: str,
    style: str = "discussion_starter"
) -> Dict[str, str]:
    """
    Generate a post using traditional templates when AI fails
    
    Args:
        article_title: Title of the Medium article
        summary: Brief summary of the article
        link: URL to the article
        subreddit: Target subreddit
        style: Preferred style (used for fallback selection)
        
    Returns:
        Dictionary with title and body
    """
    template = get_ai_fallback_template(style)
    hook = get_random_hook(subreddit)
    cta = get_random_cta()
    
    # Extract topic keyword from summary or title
    subreddit_config = get_subreddit_ai_context(subreddit)
    topic_keywords = subreddit_config.get("topic_keywords", ["topic"])
    topic_keyword = topic_keywords[0]  # Use first as default
    
    # Fill template
    title = template["title"].format(
        hook=hook,
        article_title=article_title,
        topic_keyword=topic_keyword
    )
    
    body = template["body"].format(
        hook=hook,
        summary=summary,
        link=link,
        cta=cta,
        topic_keyword=topic_keyword,
        article_title=article_title
    )
    
    return {
        "title": title,
        "body": body,
        "template_used": template["name"],
        "generation_method": "fallback_template"
    }
