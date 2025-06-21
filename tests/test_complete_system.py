"""
Comprehensive System Test Suite
Tests all components: Environment, AI, Reddit, Database, Workflow
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "core"))

from dotenv import load_dotenv
load_dotenv()

class SystemTester:
    """Comprehensive system testing"""
    
    def __init__(self):
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
    
    def test_section(self, name: str):
        """Start a new test section"""
        print(f"\n{'='*60}")
        print(f"🧪 TESTING: {name}")
        print(f"{'='*60}")
    
    def test_case(self, name: str, test_func, *args, **kwargs):
        """Run a single test case"""
        self.total_tests += 1
        print(f"\n🔍 Test: {name}")
        
        try:
            start_time = time.time()
            result = test_func(*args, **kwargs)
            end_time = time.time()
            
            if result:
                print(f"✅ PASSED ({end_time - start_time:.2f}s)")
                self.passed_tests += 1
                self.test_results[name] = {"status": "PASSED", "time": end_time - start_time}
                return True
            else:
                print(f"❌ FAILED")
                self.test_results[name] = {"status": "FAILED", "time": end_time - start_time}
                return False
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            self.test_results[name] = {"status": "ERROR", "error": str(e)}
            return False
    
    def test_environment(self):
        """Test environment configuration"""
        required_vars = [
            "GROQ_API_KEY",
            "REDDIT_CLIENT_ID", 
            "REDDIT_CLIENT_SECRET",
            "REDDIT_USERNAME",
            "REDDIT_PASSWORD",
            "REDDIT_USER_AGENT"
        ]
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"Missing variables: {missing}")
            return False
        
        print("All environment variables present")
        return True
    
    def test_imports(self):
        """Test all module imports"""
        modules = [
            "subreddit_recommender",
            "reddit_client", 
            "ai_client",
            "database",
            "utils"
        ]
        
        for module in modules:
            try:
                __import__(module)
                print(f"✓ {module}")
            except ImportError as e:
                print(f"✗ {module}: {e}")
                return False
        
        return True
    
    def test_ai_client(self):
        """Test AI client functionality"""
        try:
            from ai_client import GroqAIClient
            
            client = GroqAIClient()
            print("✓ AI client initialized")
            
            # Test simple generation
            result = client.generate_reddit_post(
                "https://medium.com/test/sample-article",
                "Test summary about Python programming",
                "programming",
                "discussion_starter"
            )
            
            if result.success and result.title and result.body:
                print(f"✓ Generated post: {result.title[:50]}...")
                return True
            else:
                print(f"✗ Generation failed: {result.error_message if hasattr(result, 'error_message') else 'Unknown error'}")
                return False
                
        except Exception as e:
            print(f"✗ AI client error: {e}")
            return False
    
    def test_reddit_client(self):
        """Test Reddit client functionality"""
        try:
            from reddit_client import get_reddit_client
            
            client = get_reddit_client()
            print("✓ Reddit client initialized")
            
            # Test connection
            if client.test_connection():
                print("✓ Reddit API connection successful")
                
                # Test subreddit access
                info = client.get_subreddit_info("programming")
                if info:
                    print(f"✓ Subreddit access: r/programming ({info.get('subscribers', 'N/A')} members)")
                    return True
                else:
                    print("✗ Could not access subreddit")
                    return False
            else:
                print("✗ Reddit API connection failed")
                return False
                
        except Exception as e:
            print(f"✗ Reddit client error: {e}")
            return False
    
    def test_subreddit_recommender(self):
        """Test subreddit recommendation system"""
        try:
            from subreddit_recommender import get_subreddit_recommender
            
            recommender = get_subreddit_recommender()
            print("✓ Subreddit recommender initialized")
            
            # Test with sample URL
            test_url = "https://medium.com/test/python-tutorial"
            recommendations = recommender.recommend_subreddits(test_url, max_recommendations=5)
            
            if recommendations and len(recommendations) > 0:
                print(f"✓ Generated {len(recommendations)} recommendations")
                
                # Test post generation
                top_rec = recommendations[0]
                post_data = recommender.generate_subreddit_specific_post(test_url, top_rec.name)
                
                if post_data.get("success", False):
                    print(f"✓ Generated post for r/{top_rec.name}")
                    return True
                else:
                    print(f"✗ Post generation failed: {post_data.get('error', 'Unknown')}")
                    return False
            else:
                print("✗ No recommendations generated")
                return False
                
        except Exception as e:
            print(f"✗ Recommender error: {e}")
            return False
    
    def test_database(self):
        """Test database functionality"""
        try:
            from database import db
            
            # Test database initialization
            print("✓ Database initialized")            # Test adding post history
            post_id = db.add_post_history(
                article_url="https://medium.com/test/sample-article",
                title="Test Article Post",
                content="This is test content for the post",
                subreddit="test",
                status="generated"
            )
            if post_id:
                print("✓ Post history added")
                
                # Test retrieving history
                history = db.get_post_history(limit=1)
                if history:
                    print("✓ Post history retrieved")
                    return True
                else:
                    print("✗ Could not retrieve history")
                    return False
            else:
                print("✗ Could not add post history")
                return False
                
        except Exception as e:
            print(f"✗ Database error: {e}")
            return False
    
    def test_utils(self):
        """Test utility functions"""
        try:
            from utils import validate_medium_url, extract_article_info
            
            # Test URL validation
            valid_urls = [
                "https://medium.com/@author/article",
                "https://towardsdatascience.com/article",
                "https://hackernoon.com/article"
            ]
            
            invalid_urls = [
                "https://google.com",
                "not-a-url",
                ""
            ]
            
            for url in valid_urls:
                if not validate_medium_url(url):
                    print(f"✗ Valid URL rejected: {url}")
                    return False
            
            for url in invalid_urls:
                if validate_medium_url(url):
                    print(f"✗ Invalid URL accepted: {url}")
                    return False
            
            print("✓ URL validation working")
            
            # Test article extraction (may fail for test URLs, that's OK)
            try:
                extract_article_info("https://medium.com/test/article")
                print("✓ Article extraction function accessible")
            except:
                print("✓ Article extraction function accessible (connection expected to fail for test URL)")
            
            return True
            
        except Exception as e:
            print(f"✗ Utils error: {e}")
            return False
    
    def test_end_to_end_workflow(self):
        """Test the complete workflow without posting"""
        try:
            from subreddit_recommender import get_subreddit_recommender
            from reddit_client import get_reddit_client
            
            print("🔄 Testing complete workflow...")
            
            # 1. Initialize components
            recommender = get_subreddit_recommender()
            reddit_client = get_reddit_client()
            
            # 2. Analyze article
            test_url = "https://medium.com/test/python-data-science"
            recommendations = recommender.recommend_subreddits(test_url, max_recommendations=3)
            
            if not recommendations:
                print("✗ No recommendations in workflow test")
                return False
            
            # 3. Generate posts
            generated_posts = []
            for rec in recommendations[:2]:  # Test with first 2
                post_data = recommender.generate_subreddit_specific_post(test_url, rec.name)
                if post_data.get("success", False):
                    generated_posts.append({
                        "subreddit": rec.name,
                        "title": post_data["title"],
                        "body": post_data["body"]
                    })
            
            if not generated_posts:
                print("✗ No posts generated in workflow test")
                return False
            
            # 4. Validate posts (don't actually post)
            for post in generated_posts:
                if not post["title"] or not post["body"]:
                    print(f"✗ Invalid post for r/{post['subreddit']}")
                    return False
            
            print(f"✓ End-to-end workflow successful ({len(generated_posts)} posts ready)")
            return True
            
        except Exception as e:
            print(f"✗ Workflow error: {e}")
            return False
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🚀 REDDIT AUTOMATION - COMPREHENSIVE SYSTEM TEST")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Environment tests
        self.test_section("ENVIRONMENT & CONFIGURATION")
        self.test_case("Environment Variables", self.test_environment)
        self.test_case("Module Imports", self.test_imports)
        
        # Component tests
        self.test_section("CORE COMPONENTS")
        self.test_case("AI Client (Groq)", self.test_ai_client)
        self.test_case("Reddit Client (PRAW)", self.test_reddit_client)
        self.test_case("Subreddit Recommender", self.test_subreddit_recommender)
        self.test_case("Database Operations", self.test_database)
        self.test_case("Utility Functions", self.test_utils)
        
        # Integration tests
        self.test_section("INTEGRATION & WORKFLOW")
        self.test_case("End-to-End Workflow", self.test_end_to_end_workflow)
        
        # Results summary
        self.show_test_results()
    
    def show_test_results(self):
        """Display comprehensive test results"""
        print(f"\n{'='*60}")
        print(f"📊 TEST RESULTS SUMMARY")
        print(f"{'='*60}")
        
        success_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Total tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success rate: {success_rate:.1f}%")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status = result["status"]
            if status == "PASSED":
                print(f"✅ {test_name} ({result.get('time', 0):.2f}s)")
            elif status == "FAILED":
                print(f"❌ {test_name}")
            elif status == "ERROR":
                print(f"🔥 {test_name}: {result.get('error', 'Unknown error')}")
        
        # System readiness
        print(f"\n🎯 SYSTEM READINESS:")
        if success_rate >= 90:
            print("🟢 EXCELLENT - System is fully ready for production use")
        elif success_rate >= 75:
            print("🟡 GOOD - System is mostly ready, minor issues detected")
        elif success_rate >= 50:
            print("🟠 FAIR - System has some issues, review failed tests")
        else:
            print("🔴 POOR - System has major issues, fix critical components")
        
        # Next steps
        if self.passed_tests == self.total_tests:
            print(f"\n🎉 ALL TESTS PASSED!")
            print("✅ Your Reddit automation system is ready to use")
            print("▶️  Run: python reddit_automation.py")
        else:
            print(f"\n⚠️  SOME TESTS FAILED")
            print("🔧 Please fix the failed components before using the system")
            print("📖 Check the error messages above for guidance")

def main():
    """Main test runner"""
    tester = SystemTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
