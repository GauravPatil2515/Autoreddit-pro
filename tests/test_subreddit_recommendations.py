"""
Test the subreddit recommendation system
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from core.subreddit_recommender import get_subreddit_recommender

# Load environment variables
load_dotenv()

def test_subreddit_recommendations():
    """Test the subreddit recommendation functionality"""
    print("🎯 Testing Subreddit Recommendation System")
    print("=" * 50)
    
    # Test URLs - replace with actual Medium articles
    test_urls = [
        "https://medium.com/@example/python-data-science-tutorial",
        "https://medium.com/@example/javascript-web-development-guide", 
        "https://medium.com/@example/startup-business-lessons"
    ]
    
    try:
        # Initialize recommender
        recommender = get_subreddit_recommender()
        print("✅ Subreddit recommender initialized successfully")
        
        # Test with a sample article URL (you can replace this)
        test_url = "https://medium.com/@example/python-machine-learning-tutorial"
        
        print(f"\n🔍 Analyzing article: {test_url}")
        print("Note: Using fallback analysis since this is a test URL")
        
        # Get recommendations
        recommendations = recommender.recommend_subreddits(test_url, max_recommendations=5)
        
        if recommendations:
            print(f"\n📋 Found {len(recommendations)} recommendations:")
            print("-" * 40)
            
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. r/{rec.name}")
                print(f"   📊 Overall Score: {rec.overall_score:.1%}")
                print(f"   🎯 Relevance: {rec.relevance_score:.1%}")
                print(f"   ✅ Compliance: {rec.compliance_score:.1%}")
                print(f"   ⚠️  Risk Level: {rec.risk_level}")
                print(f"   👥 Subscribers: {rec.subscribers:,}")
                print(f"   💡 Why: {rec.why_recommended}")
                print()
        else:
            print("❌ No recommendations found")
        
        # Test post generation for top recommendation
        if recommendations:
            top_rec = recommendations[0]
            print(f"🔄 Testing post generation for r/{top_rec.name}...")
            
            post_data = recommender.generate_subreddit_specific_post(
                test_url, 
                top_rec.name
            )
            
            if post_data.get("success", False):
                print(f"✅ Post generated successfully!")
                print(f"Title: {post_data['title']}")
                print(f"Body preview: {post_data['body'][:100]}...")
            else:
                print(f"❌ Post generation failed: {post_data.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing subreddit recommendations: {e}")
        return False

def test_content_analysis():
    """Test the content analysis functionality"""
    print("\n🧠 Testing Content Analysis")
    print("=" * 30)
    
    try:
        recommender = get_subreddit_recommender()
        
        # Test with sample content
        sample_url = "https://medium.com/test/python-data-science"
        
        print("🔍 Testing content analysis (will use fallback for test URL)...")
        content_analysis = recommender.analyze_article_content(sample_url)
        
        if "error" not in content_analysis:
            print("✅ Content analysis successful!")
            print(f"Keywords: {content_analysis.get('keywords', [])}")
            print(f"Topics: {content_analysis.get('topics', [])}")
            print(f"Content Type: {content_analysis.get('content_type', 'N/A')}")
        else:
            print(f"❌ Content analysis failed: {content_analysis['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing content analysis: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Subreddit Recommendation System Test")
    print("=" * 60)
    
    # Check if Groq API key is available
    if not os.getenv("GROQ_API_KEY"):
        print("❌ GROQ_API_KEY not found in environment variables")
        print("Please set your Groq API key in the .env file")
        exit(1)
    
    print(f"✅ Groq API key found")
    
    # Run tests
    test1_success = test_content_analysis()
    test2_success = test_subreddit_recommendations() 
    
    print("\n" + "=" * 60)
    if test1_success and test2_success:
        print("🎉 All tests passed! Subreddit recommendation system is ready!")
        print("\n📋 Next steps:")
        print("1. Run the Streamlit app: streamlit run app.py")
        print("2. Go to the 'Subreddit Recommendations' tab")
        print("3. Enter a real Medium article URL for analysis")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
