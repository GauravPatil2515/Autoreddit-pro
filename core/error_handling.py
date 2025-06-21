"""
Enhanced Error Handling and Logging for Reddit Automation Toolkit
Provides structured error handling, logging, and user-friendly error messages
"""
import logging
import sys
import traceback
import json
from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

class ErrorCode(Enum):
    """Structured error codes for different types of failures"""
    # Configuration Errors
    CONFIG_ERROR = "CONFIG_ERROR"
    MISSING_ENV_VARS = "MISSING_ENV_VARS"
    INVALID_CONFIG = "INVALID_CONFIG"
    
    # Network/API Errors
    NETWORK_ERROR = "NETWORK_ERROR"
    API_ERROR = "API_ERROR"
    AUTH_ERROR = "AUTH_ERROR"
    RATE_LIMIT = "RATE_LIMIT"
    
    # Reddit-specific Errors
    REDDIT_AUTH_FAILED = "REDDIT_AUTH_FAILED"
    REDDIT_API_ERROR = "REDDIT_API_ERROR"
    SUBREDDIT_NOT_FOUND = "SUBREDDIT_NOT_FOUND"
    POSTING_DENIED = "POSTING_DENIED"
    CONTENT_VIOLATION = "CONTENT_VIOLATION"
    
    # AI/Content Errors
    AI_API_ERROR = "AI_API_ERROR"
    CONTENT_GENERATION_FAILED = "CONTENT_GENERATION_FAILED"
    CONTENT_ANALYSIS_FAILED = "CONTENT_ANALYSIS_FAILED"
    
    # Validation Errors
    VALIDATION_ERROR = "VALIDATION_ERROR"
    URL_INVALID = "URL_INVALID"
    CONTENT_TOO_LONG = "CONTENT_TOO_LONG"
    SPAM_DETECTED = "SPAM_DETECTED"
    
    # System Errors
    DATABASE_ERROR = "DATABASE_ERROR"
    FILE_ERROR = "FILE_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    
    # Workflow Errors
    WORKFLOW_ERROR = "WORKFLOW_ERROR"
    STEP_FAILED = "STEP_FAILED"

@dataclass
class ErrorDetails:
    """Detailed error information"""
    code: ErrorCode
    message: str
    user_message: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    suggestions: Optional[List[str]] = None
    help_url: Optional[str] = None
    retry_after: Optional[int] = None
    timestamp: Optional[datetime] = None

class RedditAutomationError(Exception):
    """Base exception class for Reddit automation errors"""
    
    def __init__(self, 
                 code: ErrorCode, 
                 message: str, 
                 user_message: Optional[str] = None,
                 details: Optional[Dict[str, Any]] = None,
                 suggestions: Optional[List[str]] = None,
                 help_url: Optional[str] = None,
                 retry_after: Optional[int] = None):
        
        # Store individual attributes for backward compatibility
        self.code = code
        self.message = message
        self.user_message = user_message or self._generate_user_message(code, message)
        self.details = details or {}
        self.suggestions = suggestions or self._generate_suggestions(code)
        self.help_url = help_url or self._get_help_url(code)
        self.retry_after = retry_after
        self.timestamp = datetime.now()
        
        # Also store as ErrorDetails object for compatibility
        self.error_details = ErrorDetails(
            code=code,
            message=message,
            user_message=self.user_message,
            details=self.details,
            suggestions=self.suggestions,
            help_url=self.help_url,
            retry_after=retry_after,
            timestamp=self.timestamp
        )
        
        super().__init__(message)
    
    def _generate_user_message(self, code: ErrorCode, message: str) -> str:
        """Generate user-friendly error message"""
        user_messages = {
            ErrorCode.MISSING_ENV_VARS: "Your Reddit automation system isn't configured yet. Please run the setup wizard to get started.",
            ErrorCode.REDDIT_AUTH_FAILED: "Could not connect to Reddit. Please check your Reddit API credentials.",
            ErrorCode.AI_API_ERROR: "The AI service is currently unavailable. Please try again in a few minutes.",
            ErrorCode.RATE_LIMIT: "You're making requests too quickly. Please wait a moment before trying again.",
            ErrorCode.SUBREDDIT_NOT_FOUND: "The subreddit you specified doesn't exist or is private.",
            ErrorCode.POSTING_DENIED: "You don't have permission to post in this subreddit.",
            ErrorCode.CONTENT_VIOLATION: "Your content may violate subreddit rules. Please review and modify.",
            ErrorCode.URL_INVALID: "The article URL you provided is not valid or accessible.",
            ErrorCode.SPAM_DETECTED: "Your content appears promotional. Consider making it more informative.",
        }
        return user_messages.get(code, f"An error occurred: {message}")
    
    def _generate_suggestions(self, code: ErrorCode) -> List[str]:
        """Generate helpful suggestions based on error code"""
        suggestions = {
            ErrorCode.MISSING_ENV_VARS: [
                "Run: python scripts/setup_environment.py",
                "Check the README.md for setup instructions",
                "Ensure all required API keys are obtained"
            ],
            ErrorCode.REDDIT_AUTH_FAILED: [
                "Verify your Reddit username and password",
                "Check that your Reddit app credentials are correct",
                "Ensure you created a 'script' type app, not 'web app'"
            ],
            ErrorCode.AI_API_ERROR: [
                "Check your Groq API key is valid",
                "Verify you have API credits remaining",
                "Try again in a few minutes"
            ]
        }
        return suggestions.get(code, ["Check the logs for more details"])
    
    def _get_help_url(self, code: ErrorCode) -> Optional[str]:
        """Get help URL for specific error types"""
        help_urls = {
            ErrorCode.MISSING_ENV_VARS: "https://github.com/your-repo/setup-guide",
            ErrorCode.REDDIT_AUTH_FAILED: "https://www.reddit.com/prefs/apps",
            ErrorCode.AI_API_ERROR: "https://console.groq.com/keys",
        }
        return help_urls.get(code)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for JSON serialization"""
        return {
            "error_code": self.code.value,
            "message": self.message,
            "user_message": self.user_message,
            "details": self.details,
            "suggestions": self.suggestions,
            "help_url": self.help_url,
            "retry_after": self.retry_after,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }

class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self, log_file: Optional[str] = None):
        self.setup_logging(log_file)
        self.error_history = []
    
    def setup_logging(self, log_file: Optional[str] = None):
        """Setup logging configuration"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Create logs directory if it doesn't exist
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(log_file or 'logs/reddit_automation.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('RedditAutomation')
    
    def handle_error(self, 
                    error: Exception, 
                    context: Optional[Dict[str, Any]] = None,
                    user_facing: bool = True) -> RedditAutomationError:
        """Handle and log an error, converting it to RedditAutomationError if needed"""
        
        # Convert to structured error if needed
        if isinstance(error, RedditAutomationError):
            structured_error = error
        else:
            structured_error = self._convert_to_structured_error(error, context)
        
        # Log the error
        self._log_error(structured_error, context)
        
        # Add to error history
        self.error_history.append({
            "error": structured_error.to_dict(),
            "context": context,
            "timestamp": datetime.now()
        })
        
        return structured_error
    
    def _convert_to_structured_error(self, 
                                   error: Exception, 
                                   context: Optional[Dict[str, Any]] = None) -> RedditAutomationError:
        """Convert generic exception to structured error"""
        
        error_str = str(error).lower()
        error_type = type(error).__name__
        
        # Default system error
        return RedditAutomationError(
            ErrorCode.SYSTEM_ERROR,
            f"Unexpected error: {str(error)}",
            details={
                "error_type": error_type,
                "traceback": traceback.format_exc()
            }
        )
    
    def _log_error(self, error: RedditAutomationError, context: Optional[Dict[str, Any]] = None):
        """Log error with appropriate level"""
        log_message = f"[{error.code.value}] {error.message}"
        
        if context:
            log_message += f" | Context: {json.dumps(context, default=str)}"
        
        self.logger.error(log_message)

# Global error handler instance
_error_handler = None

def get_error_handler() -> ErrorHandler:
    """Get global error handler instance"""
    global _error_handler
    if _error_handler is None:
        _error_handler = ErrorHandler()
    return _error_handler

def configure_error_handling(log_file: Optional[str] = None):
    """Configure global error handling"""
    global _error_handler
    _error_handler = ErrorHandler(log_file)

# User-friendly error display functions
def display_error_to_user(error: RedditAutomationError) -> str:
    """Format error for user display"""
    output = []
    output.append(f"ERROR: {error.user_message}")
    
    if error.suggestions:
        output.append("\\nSuggestions:")
        for suggestion in error.suggestions:
            output.append(f"   • {suggestion}")
    
    if error.help_url:
        output.append(f"\\nHelp: {error.help_url}")
    
    if error.retry_after:
        output.append(f"\\nPlease wait {error.retry_after} seconds before retrying")
    
    return "\\n".join(output)

def get_error_recovery_steps(error: RedditAutomationError) -> List[str]:
    """Get recovery steps for an error"""
    recovery_steps = {
        ErrorCode.MISSING_ENV_VARS: [
            "Run the environment setup wizard: python scripts/setup_environment.py",
            "Follow the setup instructions carefully",
            "Test the configuration with: python scripts/setup_environment.py --check"
        ],
        ErrorCode.REDDIT_AUTH_FAILED: [
            "Double-check your Reddit username and password",
            "Verify your Reddit API credentials at https://www.reddit.com/prefs/apps",
            "Make sure you created a 'script' type application",
            "Re-run the setup wizard if needed"
        ]
    }
    
    return recovery_steps.get(error.code, [
        "Check the error logs for more details",
        "Try the operation again",
        "Contact support if the problem persists"
    ])
