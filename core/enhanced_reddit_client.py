"""
Enhanced Reddit Client with Direct Posting and Policy Compliance
"""
import os
import time
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass

try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    praw = None

@dataclass
class PostResult:
    success: bool = False
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error_message: Optional[str] = None
    submission_object: Optional[object] = None

@dataclass
class SubredditInfo:
    name: str
    display_name: str
    subscribers: int
    description: str
    rules: List[str]
    available_flairs: List[str]
    submission_requirements: Dict
    posting_allowed: bool
    over18: bool

class EnhancedRedditClient:
    def __init__(self):
        if not PRAW_AVAILABLE:
            raise ImportError("PRAW library not installed")
        
        # Try to initialize Reddit client with error handling
        try:
            self.reddit = praw.Reddit(
                client_id=os.getenv("REDDIT_CLIENT_ID"),
                client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                username=os.getenv("REDDIT_USERNAME"),
                password=os.getenv("REDDIT_PASSWORD"),
                user_agent=os.getenv("REDDIT_USER_AGENT", "reddit_automation_bot_1.0")
            )
            self.client = self.reddit  # Add alias for compatibility
            self.username = os.getenv("REDDIT_USERNAME")
            
            # Test connection
            try:
                self.reddit.user.me()
            except Exception as e:
                print(f"Warning: Reddit connection test failed: {e}")
                
        except Exception as e:
            print(f"Warning: Could not initialize Reddit client: {e}")
            self.reddit = None
            self.client = None
            self.username = None
    
    def test_connection(self) -> bool:
        """Test Reddit API connection"""
        try:
            user = self.reddit.user.me()
            return user is not None
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def get_detailed_subreddit_info(self, subreddit_name: str) -> SubredditInfo:
        """Get detailed information about a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Get available flairs
            available_flairs = []
            try:
                for flair in subreddit.flair.link_templates:
                    available_flairs.append(flair['text'])
            except:
                available_flairs = []
            
            # Get rules
            rules = []
            try:
                for rule in subreddit.rules:
                    rules.append(rule.short_name)
            except:
                rules = []
            
            # Check submission requirements
            submission_requirements = {
                "text_posts_allowed": True,
                "link_posts_allowed": True,
                "requires_flair": len(available_flairs) > 0,
                "min_account_age": 0,
                "min_karma": 0
            }
            
            return SubredditInfo(
                name=subreddit_name,
                display_name=subreddit.display_name,
                subscribers=subreddit.subscribers or 0,
                description=subreddit.description[:200] if subreddit.description else "",
                rules=rules,
                available_flairs=available_flairs,
                submission_requirements=submission_requirements,
                posting_allowed=True,
                over18=subreddit.over18 or False
            )
            
        except Exception as e:
            return SubredditInfo(
                name=subreddit_name,
                display_name=subreddit_name,
                subscribers=0,
                description=f"Error getting info: {e}",
                rules=[],
                available_flairs=[],
                submission_requirements={},
                posting_allowed=False,
                over18=False
            )
    
    def validate_post_before_submission(self, subreddit_name: str, title: str, body: str, flair: str = None) -> Dict:
        """Validate post before submission to check for potential issues"""
        validation_result = {
            "can_post": True,
            "warnings": [],
            "errors": [],
            "suggestions": []
        }
        
        try:
            subreddit_info = self.get_detailed_subreddit_info(subreddit_name)
            
            # Check if posting is allowed
            if not subreddit_info.posting_allowed:
                validation_result["can_post"] = False
                validation_result["errors"].append("Posting not allowed in this subreddit")
            
            # Check title length
            if len(title) > 300:
                validation_result["warnings"].append("Title is very long (>300 chars)")
            elif len(title) < 10:
                validation_result["warnings"].append("Title might be too short")
            
            # Check body length
            if len(body) > 40000:
                validation_result["warnings"].append("Post body is very long")
            
            # Check flair requirements
            if subreddit_info.submission_requirements.get("requires_flair", False):
                if not flair and subreddit_info.available_flairs:
                    validation_result["warnings"].append(f"Consider adding flair. Available: {', '.join(subreddit_info.available_flairs[:3])}")
            
            # Content quality checks
            if title.count('!') > 3:
                validation_result["suggestions"].append("Reduce exclamation marks in title")
            
            if title.isupper():
                validation_result["suggestions"].append("Avoid all caps in title")
            
            # Self-promotion detection
            if any(word in body.lower() for word in ['my blog', 'my website', 'check out my', 'subscribe to']):
                validation_result["warnings"].append("Content might be seen as self-promotion")
            
            return validation_result
            
        except Exception as e:
            validation_result["errors"].append(f"Validation error: {e}")
            return validation_result
    
    def submit_post_with_validation(self, subreddit_name: str, title: str, body: str, flair: str = None, validate_first: bool = True) -> PostResult:
        """Submit post with optional validation"""
        
        if validate_first:
            validation = self.validate_post_before_submission(subreddit_name, title, body, flair)
            
            if not validation["can_post"]:
                return PostResult(
                    success=False,
                    error_message=f"Validation failed: {'; '.join(validation['errors'])}"
                )
            
            # Log warnings
            if validation["warnings"]:
                print(f"⚠️ Warnings: {'; '.join(validation['warnings'])}")
            
            if validation["suggestions"]:
                print(f"💡 Suggestions: {'; '.join(validation['suggestions'])}")
        
        return self.submit_post(subreddit_name, title, body, flair)
    
    def submit_post(self, subreddit_name: str, title: str, body: str, flair: str = None) -> PostResult:
        """Submit a post to Reddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            # Submit the post
            submission = subreddit.submit(
                title=title,
                selftext=body,
                flair_id=None,  # We'll set flair separately if needed
                send_replies=True
            )
            
            # Set flair if provided
            if flair:
                try:
                    # Try to set flair
                    submission.flair.select(flair)
                except Exception as flair_error:
                    print(f"Warning: Could not set flair '{flair}': {flair_error}")
            
            return PostResult(
                success=True,
                post_id=submission.id,
                post_url=f"https://reddit.com{submission.permalink}",
                submission_object=submission
            )
            
        except Exception as e:
            error_msg = str(e)
            
            # Parse common Reddit errors
            if "SUBMIT_VALIDATION_FLAIR_REQUIRED" in error_msg:
                error_msg = "This subreddit requires post flair. Please add appropriate flair."
            elif "NO_SELFS" in error_msg:
                error_msg = "This subreddit doesn't allow text posts."
            elif "SUBMIT_VALIDATION_BODY_NOT_ALLOWED" in error_msg:
                error_msg = "This subreddit doesn't allow body text in posts."
            elif "RATELIMIT" in error_msg:
                error_msg = "Rate limited. Please wait before posting again."
            elif "SUBREDDIT_NOTALLOWED" in error_msg:
                error_msg = "You don't have permission to post in this subreddit."
            
            return PostResult(
                success=False,
                error_message=error_msg
            )
    
    def get_post_performance(self, post_id: str) -> Dict:
        """Get performance metrics for a posted submission"""
        try:
            submission = self.reddit.submission(id=post_id)
            
            return {
                "upvotes": submission.score,
                "upvote_ratio": submission.upvote_ratio,
                "num_comments": submission.num_comments,
                "created_utc": submission.created_utc,
                "permalink": submission.permalink,
                "is_removed": submission.removed_by_category is not None,
                "flair": submission.link_flair_text
            }
            
        except Exception as e:
            return {"error": f"Could not get performance data: {e}"}
    
    def check_user_permissions(self, subreddit_name: str) -> Dict:
        """Check user's permissions in a subreddit"""
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            
            permissions = {
                "can_submit": True,
                "is_banned": False,
                "is_moderator": False,
                "is_contributor": False,
                "account_age_ok": True,
                "karma_sufficient": True
            }
            
            # Check if user is banned (this might raise an exception)
            try:
                # Try to get user's flair (will fail if banned)
                subreddit.flair(self.username)
            except Exception:
                permissions["is_banned"] = True
                permissions["can_submit"] = False
            
            # Check if user is moderator
            try:
                moderators = list(subreddit.moderator())
                permissions["is_moderator"] = any(mod.name == self.username for mod in moderators)
            except:
                pass
            
            return permissions
            
        except Exception as e:
            return {"error": f"Could not check permissions: {e}"}
    
    def get_user_post_history(self, limit: int = 10) -> List[Dict]:
        """Get user's recent post history"""
        try:
            user = self.reddit.user.me()
            submissions = list(user.submissions.new(limit=limit))
            
            history = []
            for submission in submissions:
                history.append({
                    "id": submission.id,
                    "title": submission.title,
                    "subreddit": submission.subreddit.display_name,
                    "score": submission.score,
                    "num_comments": submission.num_comments,
                    "created_utc": submission.created_utc,
                    "url": f"https://reddit.com{submission.permalink}"
                })
            
            return history
            
        except Exception as e:
            return [{"error": f"Could not get post history: {e}"}]
    
    def get_subreddit_info(self, subreddit_name: str) -> Dict:
        """Get basic subreddit information (compatible interface)"""
        if not self.reddit:
            return {"error": "Reddit client not initialized"}
            
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return {
                "name": subreddit_name,
                "display_name": subreddit.display_name,
                "subscribers": subreddit.subscribers,
                "description": subreddit.public_description or "No description",
                "over18": subreddit.over18,
                "can_assign_link_flair": subreddit.can_assign_link_flair,
                "submission_type": subreddit.submission_type
            }
        except Exception as e:
            return {"error": str(e)}
    
    def can_post_to_subreddit(self, subreddit_name: str) -> bool:
        """Check if we can post to a subreddit"""
        if not self.reddit:
            return False
            
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            # Basic checks
            return (subreddit.submission_type in ["any", "self"] and 
                   not subreddit.subreddit_type == "private")
        except Exception:
            return False
    
    def validate_post_content(self, content: str, title: str, subreddit_name: str) -> Tuple[bool, List[str]]:
        """Validate post content against subreddit rules"""
        issues = []
        
        # Basic validation
        if len(title) > 300:
            issues.append("Title too long (max 300 characters)")
        if len(content) > 40000:
            issues.append("Content too long (max 40,000 characters)")
        if not title.strip():
            issues.append("Title cannot be empty")
        
        # Content quality checks
        if content.count("http") > 5:
            issues.append("Too many links in content")
        
        # Spam-like patterns
        spam_indicators = ["click here", "buy now", "limited time", "act fast"]
        spam_count = sum(1 for indicator in spam_indicators if indicator.lower() in content.lower())
        if spam_count > 2:
            issues.append("Content appears promotional")
        
        return len(issues) == 0, issues
    
    def create_post(self, subreddit: str, title: str, content: str) -> Dict:
        """Create a post on Reddit (compatible interface)"""
        if not self.reddit:
            return {"success": False, "error": "Reddit client not initialized"}
            
        try:
            subreddit_obj = self.reddit.subreddit(subreddit)
            submission = subreddit_obj.submit(title=title, selftext=content)
            
            return {
                "success": True,
                "post_id": submission.id,
                "url": f"https://reddit.com{submission.permalink}",
                "title": submission.title,
                "subreddit": submission.subreddit.display_name
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global instance
_enhanced_reddit_client = None

def get_enhanced_reddit_client():
    """Get the enhanced Reddit client instance"""
    global _enhanced_reddit_client
    if _enhanced_reddit_client is None:
        _enhanced_reddit_client = EnhancedRedditClient()
    return _enhanced_reddit_client
