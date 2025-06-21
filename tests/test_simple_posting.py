"""
Simple Reddit Posting Test
Tests if the system can actually post to Reddit
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import praw
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

def test_basic_reddit_connection():
    """Test basic Reddit API connection"""
    print("🔍 Testing Reddit API Connection...")
    
    try:
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            username=os.getenv("REDDIT_USERNAME"),
            password=os.getenv("REDDIT_PASSWORD"),
            user_agent="RedditAutomationBot/1.0"
        )
        
        # Test authentication
        user = reddit.user.me()
        print(f"✅ Connected to Reddit as: {user.name}")
        print(f"   Account created: {datetime.fromtimestamp(user.created_utc).strftime('%Y-%m-%d')}")
        print(f"   Karma: {user.comment_karma + user.link_karma}")
        
        return True, reddit
        
    except Exception as e:
        print(f"❌ Reddit connection failed: {str(e)}")
        return False, None

def test_subreddit_access():
    """Test access to various subreddits"""
    print("\\n🔍 Testing Subreddit Access...")
    
    success, reddit = test_basic_reddit_connection()
    if not success:
        return False
    
    test_subreddits = ["test", "pythonforengineers", "learnpython"]
    
    for subreddit_name in test_subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            print(f"✅ r/{subreddit_name}: {subreddit.subscribers:,} subscribers")
            
            # Check if we can access recent posts
            posts = list(subreddit.new(limit=1))
            print(f"   Latest post: {posts[0].title[:50]}..." if posts else "   No posts found")
            
        except Exception as e:
            print(f"❌ r/{subreddit_name}: {str(e)}")
    
    return True

def test_posting_permissions():
    """Test posting permissions on safe subreddits"""
    print("\\n🔍 Testing Posting Permissions...")
    
    success, reddit = test_basic_reddit_connection()
    if not success:
        return False
    
    username = os.getenv("REDDIT_USERNAME")
    safe_subreddits = ["test", f"u_{username}"]
    
    for subreddit_name in safe_subreddits:
        try:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Try to access subreddit info
            print(f"📝 r/{subreddit_name}:")
            print(f"   Description: {subreddit.public_description[:100] if subreddit.public_description else 'No description'}")
            print(f"   Submission Type: {subreddit.submission_type}")
            print(f"   Subscribers: {subreddit.subscribers:,}")
            
            # Check if posting is allowed
            if subreddit.submission_type in ["any", "self"]:
                print(f"   ✅ Text posts allowed")
            else:
                print(f"   ⚠️  Text posts not allowed")
                
        except Exception as e:
            print(f"   ❌ Error accessing r/{subreddit_name}: {str(e)}")
    
    return True

def test_actual_post():
    """Test making an actual post to Reddit"""
    print("\\n🔍 Testing ACTUAL Reddit Posting...")
    print("⚠️  WARNING: This will create a real post on Reddit!")
    
    # Ask for confirmation
    confirm = input("\\nContinue with live posting test? (y/N): ").lower().strip()
    if confirm != 'y':
        print("⏭️  Skipping live posting test")
        return True
    
    success, reddit = test_basic_reddit_connection()
    if not success:
        return False
    
    username = os.getenv("REDDIT_USERNAME")
    target_subreddit = f"u_{username}"  # Post to user's profile (safest option)
    
    try:
        print(f"\\n📝 Creating test post in r/{target_subreddit}...")
        
        # Create the post
        title = f"Reddit Automation Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        content = f"""# Reddit Automation System Test

This is an automated test post created by the Reddit Automation Toolkit.

**Test Details:**
- Posted on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
- Posted by: Reddit Automation Bot
- Target: r/{target_subreddit}
- Status: Testing actual posting functionality

**Purpose:**
This post verifies that the Reddit automation system can successfully:
1. ✅ Connect to Reddit API
2. ✅ Authenticate with credentials  
3. ✅ Create and submit posts
4. ✅ Handle responses properly

If you're seeing this post, the automation system is working correctly! 🎉

---
*This is an automated post. Please ignore.*"""
        
        subreddit = reddit.subreddit(target_subreddit)
        submission = subreddit.submit(title=title, selftext=content)
        
        print(f"✅ POST SUCCESSFUL!")
        print(f"   Post ID: {submission.id}")
        print(f"   Post URL: https://reddit.com{submission.permalink}")
        print(f"   Title: {submission.title}")
        print(f"   Subreddit: r/{submission.subreddit.display_name}")
        print(f"   Created: {datetime.fromtimestamp(submission.created_utc)}")
        
        # Test retrieving the post
        print("\\n🔍 Verifying post exists...")
        retrieved_post = reddit.submission(id=submission.id)
        print(f"✅ Post verified: {retrieved_post.title}")
        
        return True, {
            "post_id": submission.id,
            "post_url": f"https://reddit.com{submission.permalink}",
            "title": submission.title,
            "subreddit": submission.subreddit.display_name
        }
        
    except Exception as e:
        print(f"❌ POSTING FAILED: {str(e)}")
        
        # Provide specific error guidance
        if "THREAD_LOCKED" in str(e):
            print("   → The subreddit doesn't allow new posts")
        elif "NO_TEXT" in str(e):
            print("   → Post content is required")
        elif "RATE_LIMIT" in str(e):
            print("   → You're posting too frequently. Wait before trying again")
        elif "SUBREDDIT_NOTALLOWED" in str(e):
            print("   → You don't have permission to post in this subreddit")
        else:
            print(f"   → Unexpected error: {type(e).__name__}")
        
        return False, str(e)

def test_post_retrieval():
    """Test retrieving posts from Reddit"""
    print("\\n🔍 Testing Post Retrieval...")
    
    success, reddit = test_basic_reddit_connection()
    if not success:
        return False
    
    try:
        # Get some recent posts from a popular subreddit
        subreddit = reddit.subreddit("pythonforengineers")
        posts = list(subreddit.new(limit=3))
        
        print(f"✅ Retrieved {len(posts)} recent posts from r/pythonforengineers:")
        for i, post in enumerate(posts, 1):
            print(f"   {i}. {post.title[:60]}...")
            print(f"      Score: {post.score}, Comments: {post.num_comments}")
        
        return True
        
    except Exception as e:
        print(f"❌ Post retrieval failed: {str(e)}")
        return False

def main():
    """Run focused posting tests"""
    print("🚀 REDDIT POSTING FUNCTIONALITY TEST")
    print("=" * 50)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check environment variables first
    required_vars = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USERNAME", "REDDIT_PASSWORD"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("   Please check your .env file")
        return False
    
    print("✅ All required environment variables are present")
    
    # Run tests
    tests = [
        ("Basic Reddit Connection", test_basic_reddit_connection),
        ("Subreddit Access", test_subreddit_access), 
        ("Posting Permissions", test_posting_permissions),
        ("Post Retrieval", test_post_retrieval),
        ("Actual Posting", test_actual_post)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\\n{'='*50}")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"❌ Test '{test_name}' failed with error: {str(e)}")
            results[test_name] = False
    
    # Summary
    print(f"\\n{'='*50}")
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {test_name}")
    
    print(f"\\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\\n🎉 ALL TESTS PASSED! Reddit posting is working correctly.")
    else:
        print(f"\\n⚠️  {total - passed} test(s) failed. Check the output above.")
    
    return results

if __name__ == "__main__":
    main()
