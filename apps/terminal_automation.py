#!/usr/bin/env python3
"""
Terminal-based Reddit Automation Tool
"""
import sys
import os
import argparse
from typing import List, Dict

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from core.ai_client import get_ai_client
from core.reddit_client import get_reddit_client
from core.subreddit_recommender import get_subreddit_recommender
from core.database import get_database
from core.utils import validate_medium_url, extract_article_info

def print_banner():
    print("🚀 Reddit Automation - Terminal Mode")
    print("=" * 50)
    print()

def generate_post(article_url: str, subreddit: str = None) -> None:
    """Generate a post for the given article"""
    try:
        print(f"🔗 Analyzing article: {article_url}")
        
        if not validate_medium_url(article_url):
            print("❌ Invalid article URL. Please provide a valid Medium/tech blog URL.")
            return
        
        # Get AI client and generate post
        ai_client = get_ai_client()
        if not ai_client:
            print("❌ AI client not available")
            return
        
        # Extract article info
        article_info = extract_article_info(article_url)
        
        # Generate post content
        print("🤖 Generating post content...")
        post_content = ai_client.generate_post(
            article_url=article_url,
            article_title=article_info.get('title', 'Article'),
            article_summary=article_info.get('description', 'Interesting article')
        )
        
        print("\n📝 Generated Post:")
        print("-" * 30)
        print(f"Title: {post_content.get('title', 'No title')}")
        print(f"Content: {post_content.get('content', 'No content')}")
        print("-" * 30)
        
        # Save to database
        db = get_database()
        db.add_post_history(
            article_url=article_url,
            subreddit=subreddit or "test",
            title=post_content.get('title', ''),
            content=post_content.get('content', ''),
            status="generated"
        )
        
        print("✅ Post generated and saved to database")
        
    except Exception as e:
        print(f"❌ Error generating post: {e}")

def recommend_subreddits(article_url: str) -> None:
    """Get subreddit recommendations for the article"""
    try:
        print(f"🎯 Finding subreddit recommendations for: {article_url}")
        
        if not validate_medium_url(article_url):
            print("❌ Invalid article URL. Please provide a valid Medium/tech blog URL.")
            return
        
        recommender = get_subreddit_recommender()
        recommendations = recommender.recommend_subreddits(article_url)
        
        print(f"\n📋 Found {len(recommendations)} recommendations:")
        print("-" * 50)
        
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. r/{rec.name}")
            print(f"   📊 Score: {rec.overall_score*100:.1f}%")
            print(f"   ⚠️  Risk: {rec.risk_level}")
            print(f"   💡 Why: {rec.why_recommended}")
            print()
        
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")

def show_history() -> None:
    """Show post history from database"""
    try:
        db = get_database()
        history = db.get_post_history(limit=10)
        
        if not history:
            print("📭 No post history found")
            return
        
        print("📋 Recent Post History:")
        print("-" * 60)
        
        for post in history:
            print(f"🔗 {post.get('article_url', 'N/A')}")
            print(f"📍 r/{post.get('subreddit', 'N/A')}")
            print(f"📝 {post.get('title', 'N/A')[:60]}...")
            print(f"📅 {post.get('created_at', 'N/A')}")
            print(f"✅ Status: {post.get('status', 'N/A')}")
            print("-" * 40)
        
    except Exception as e:
        print(f"❌ Error fetching history: {e}")

def main():
    parser = argparse.ArgumentParser(description="Reddit Automation Terminal Tool")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate post command
    gen_parser = subparsers.add_parser('generate', help='Generate a post for an article')
    gen_parser.add_argument('url', help='Article URL to analyze')
    gen_parser.add_argument('--subreddit', help='Target subreddit (optional)')
    
    # Recommend subreddits command
    rec_parser = subparsers.add_parser('recommend', help='Get subreddit recommendations')
    rec_parser.add_argument('url', help='Article URL to analyze')
    
    # History command
    hist_parser = subparsers.add_parser('history', help='Show post generation history')
    
    args = parser.parse_args()
    
    print_banner()
    
    if args.command == 'generate':
        generate_post(args.url, args.subreddit)
    elif args.command == 'recommend':
        recommend_subreddits(args.url)
    elif args.command == 'history':
        show_history()
    else:
        print("Usage examples:")
        print("  python apps/terminal_automation.py generate https://medium.com/@example/article")
        print("  python apps/terminal_automation.py recommend https://medium.com/@example/article")
        print("  python apps/terminal_automation.py history")
        print("\nFor detailed help: python apps/terminal_automation.py --help")

if __name__ == "__main__":
    main()
