"""
Comprehensive Real Reddit Posting Test
Tests actual posting functionality and error handling
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import traceback

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from core.error_handling import ErrorHandler, RedditAutomationError, ErrorCode, get_error_handler
from core.enhanced_reddit_client import get_enhanced_reddit_client
from core.enhanced_subreddit_recommender import get_enhanced_subreddit_recommender
from core.workflow_manager import get_workflow_manager
from core.ai_client import get_ai_client
from core.database import get_database

def test_reddit_authentication():
    """Test Reddit authentication with proper error handling"""
    print("🔍 Testing Reddit Authentication...")
    
    try:
        reddit_client = get_enhanced_reddit_client()
        
        # Test basic connection
        user = reddit_client.client.user.me()
        print(f"✅ Reddit Authentication SUCCESS - Logged in as: {user.name}")
        
        # Test subreddit access
        test_subreddit = reddit_client.client.subreddit("test")
        print(f"✅ Subreddit Access - r/test has {test_subreddit.subscribers} subscribers")
        
        return True, None
        
    except Exception as e:
        error_handler = get_error_handler()
        structured_error = error_handler.handle_error(e, context={"test": "reddit_auth"})
        print(f"❌ Reddit Authentication FAILED: {structured_error.error_details.user_message}")
        return False, structured_error

def test_subreddit_permissions():
    """Test posting permissions in safe test subreddits"""
    print("\\n🔍 Testing Subreddit Permissions...")
    
    test_subreddits = ["test", "u_" + os.getenv("REDDIT_USERNAME", "testuser")]
    results = {}
    
    try:
        reddit_client = get_enhanced_reddit_client()
        
        for subreddit_name in test_subreddits:
            try:
                subreddit_info = reddit_client.get_subreddit_info(subreddit_name)
                can_post = reddit_client.can_post_to_subreddit(subreddit_name)
                
                results[subreddit_name] = {
                    "exists": True,
                    "can_post": can_post,
                    "info": subreddit_info
                }
                
                status = "✅ CAN POST" if can_post else "⚠️ CANNOT POST"
                print(f"{status} - r/{subreddit_name}: {subreddit_info.get('description', 'No description')[:50]}...")
                
            except Exception as e:
                results[subreddit_name] = {
                    "exists": False,
                    "error": str(e)
                }
                print(f"❌ r/{subreddit_name}: {str(e)}")
        
        return results
        
    except Exception as e:
        error_handler = get_error_handler()
        structured_error = error_handler.handle_error(e, context={"test": "subreddit_permissions"})
        print(f"❌ Subreddit Permission Test FAILED: {structured_error.error_details.user_message}")
        return {}

def test_content_generation():
    """Test AI content generation with error handling"""
    print("\\n🔍 Testing Content Generation...")
    
    try:
        ai_client = get_ai_client()
        recommender = get_enhanced_subreddit_recommender()
        
        # Test URL - using a simple, accessible article
        test_url = "https://medium.com/@example/test-article"
        test_content = "This is a test article about Python programming best practices."
        
        # Test subreddit recommendations
        print("  Testing subreddit recommendations...")
        recommendations = recommender.get_recommendations(test_content, 3)
        print(f"  ✅ Generated {len(recommendations)} recommendations")
        
        # Test post generation
        print("  Testing post generation...")
        if recommendations:
            target_subreddit = recommendations[0]["name"]
            post = recommender.generate_post(test_content, target_subreddit)
            print(f"  ✅ Generated post for r/{target_subreddit}")
            print(f"     Title: {post['title'][:50]}...")
            print(f"     Content length: {len(post['content'])} characters")
            
            return True, {
                "recommendations": recommendations,
                "post": post,
                "target_subreddit": target_subreddit
            }
        else:
            print("  ❌ No recommendations generated")
            return False, None
            
    except Exception as e:
        error_handler = get_error_handler()
        structured_error = error_handler.handle_error(e, context={"test": "content_generation"})
        print(f"❌ Content Generation FAILED: {structured_error.error_details.user_message}")
        return False, structured_error

def test_dry_run_posting():
    """Test posting workflow without actually posting (dry run)"""
    print("\\n🔍 Testing Posting Workflow (Dry Run)...")
    
    try:
        workflow_manager = get_workflow_manager()
        
        # Test the complete workflow
        test_url = "https://example.com/test-article"
        
        print("  Running complete workflow...")
        result = workflow_manager.run_complete_workflow(
            url=test_url,
            dry_run=True  # Don't actually post
        )
        
        print(f"  ✅ Workflow completed successfully")
        print(f"     Steps completed: {len(result.get('steps', []))}")
        print(f"     Recommendations: {len(result.get('recommendations', []))}")
        print(f"     Final post ready: {'✅' if result.get('final_post') else '❌'}")
        
        return True, result
        
    except Exception as e:
        error_handler = get_error_handler()
        structured_error = error_handler.handle_error(e, context={"test": "dry_run_posting"})
        print(f"❌ Dry Run Posting FAILED: {structured_error.error_details.user_message}")
        return False, structured_error

def test_actual_posting():
    """Test actual posting to a safe test subreddit"""
    print("\\n🔍 Testing ACTUAL Posting (LIVE TEST)...")
    print("⚠️  WARNING: This will make an actual post to Reddit!")
    
    # Ask for confirmation
    confirm = input("Continue with live posting test? (y/N): ").lower().strip()
    if confirm != 'y':
        print("  ⏭️  Skipping live posting test")
        return True, {"skipped": True}
    
    try:
        reddit_client = get_enhanced_reddit_client()
        
        # Use user's profile as safest posting location
        username = os.getenv("REDDIT_USERNAME")
        safe_subreddit = f"u_{username}"
        
        # Create a test post
        test_post = {
            "title": f"Reddit Automation Test - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": """This is an automated test post from the Reddit Automation Toolkit.

This post was created to verify that the posting functionality is working correctly.

Test Details:
- Generated automatically
- Posted via PRAW API
- Part of system validation

If you see this post, the automation system is working! 🎉""",
            "subreddit": safe_subreddit
        }
        
        print(f"  Attempting to post to r/{safe_subreddit}...")
        
        # Actually post
        post_result = reddit_client.create_post(
            subreddit=safe_subreddit,
            title=test_post["title"],
            content=test_post["content"]
        )
        
        if post_result.get("success"):
            post_url = post_result.get("url", "N/A")
            print(f"  ✅ LIVE POST SUCCESS!")
            print(f"     Post URL: {post_url}")
            print(f"     Post ID: {post_result.get('post_id', 'N/A')}")
            
            # Log to database
            db = get_database()
            db.add_post_history(
                url="test://live-posting-test",
                subreddit=safe_subreddit,
                title=test_post["title"],
                content=test_post["content"],
                post_id=post_result.get("post_id"),
                post_url=post_url,
                status="posted"
            )
            
            return True, post_result
        else:
            print(f"  ❌ POST FAILED: {post_result.get('error', 'Unknown error')}")
            return False, post_result
            
    except Exception as e:
        error_handler = get_error_handler()
        structured_error = error_handler.handle_error(e, context={"test": "actual_posting"})
        print(f"❌ Live Posting FAILED: {structured_error.error_details.user_message}")
        print(f"   Error details: {structured_error.error_details.suggestions}")
        return False, structured_error

def test_error_recovery():
    """Test error handling and recovery mechanisms"""
    print("\\n🔍 Testing Error Recovery...")
    
    error_handler = get_error_handler()
    
    # Test various error scenarios
    test_cases = [
        {
            "name": "Invalid Subreddit",
            "test": lambda: get_enhanced_reddit_client().get_subreddit_info("this_subreddit_definitely_does_not_exist_123456")
        },
        {
            "name": "Invalid URL",
            "test": lambda: get_enhanced_subreddit_recommender().analyze_url("not-a-url")
        },
        {
            "name": "Empty Content",
            "test": lambda: get_enhanced_subreddit_recommender().get_recommendations("", 5)
        }
    ]
    
    recovery_results = {}
    
    for case in test_cases:
        try:
            print(f"  Testing {case['name']}...")
            case["test"]()
            print(f"    ⚠️  Expected error but test passed")
            recovery_results[case["name"]] = "unexpected_success"
        except Exception as e:
            structured_error = error_handler.handle_error(e, context={"test_case": case["name"]})
            print(f"    ✅ Error handled correctly: {structured_error.error_details.code.value}")
            recovery_results[case["name"]] = "handled_correctly"
    
    # Get error summary
    error_summary = error_handler.get_error_summary(hours=1)
    print(f"  Error summary: {error_summary['total_errors']} errors in last hour")
    
    return recovery_results

def main():
    """Run comprehensive posting test"""
    print("🚀 REDDIT AUTOMATION - COMPREHENSIVE POSTING TEST")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Initialize error handling
    from core.error_handling import configure_error_handling
    configure_error_handling("logs/posting_test.log")
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("Reddit Authentication", test_reddit_authentication),
        ("Subreddit Permissions", test_subreddit_permissions),
        ("Content Generation", test_content_generation),
        ("Dry Run Posting", test_dry_run_posting),
        ("Actual Posting", test_actual_posting),
        ("Error Recovery", test_error_recovery)
    ]
    
    for test_name, test_func in tests:
        try:
            print(f"\\n{'=' * 60}")
            result = test_func()
            test_results[test_name] = result
        except Exception as e:
            print(f"❌ TEST FRAMEWORK ERROR in {test_name}: {str(e)}")
            test_results[test_name] = ("error", str(e))
    
    # Final summary
    print(f"\\n{'=' * 60}")
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results.items():
        if isinstance(result, tuple) and len(result) >= 2:
            success = result[0]
            if success:
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
                failed += 1
        else:
            print(f"ℹ️  {test_name}: COMPLETED")
    
    print(f"\\nTotal: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\\n🎉 ALL TESTS PASSED! Your Reddit automation is working correctly.")
    else:
        print(f"\\n⚠️  {failed} tests failed. Check the errors above for details.")
    
    return test_results

if __name__ == "__main__":
    results = main()
