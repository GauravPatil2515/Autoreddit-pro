"""
Enhanced Reddit Automation Dashboard - Complete Workflow
AI-Powered Reddit posting with policy compliance and direct posting
"""

import streamlit as st
import pandas as pd
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
from pathlib import Path
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables
load_dotenv()

# Import our enhanced modules
try:
    from core.workflow_manager import get_workflow_manager
    from core.enhanced_subreddit_recommender import get_enhanced_subreddit_recommender
    from core.enhanced_reddit_client import get_enhanced_reddit_client
    from core.database import get_database
    from core.utils import validate_medium_url
except ImportError as e:
    st.error(f"Failed to import modules: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Reddit Automation - Enhanced Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize session state variables"""
    if 'workflow_manager' not in st.session_state:
        try:
            st.session_state.workflow_manager = get_workflow_manager()
        except Exception as e:
            st.session_state.workflow_manager = None
            st.error(f"Failed to initialize workflow manager: {e}")
    
    if 'current_workflow_result' not in st.session_state:
        st.session_state.current_workflow_result = None
    
    if 'posting_history' not in st.session_state:
        st.session_state.posting_history = []

def render_header():
    """Render the main header"""
    st.title("🚀 Reddit Automation - Enhanced Dashboard")
    st.markdown("**Complete Workflow: URL → Analysis → Recommendations → Policy-Compliant Posts → Direct Posting**")
    
    # Status indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.session_state.workflow_manager:
            st.success("✅ Workflow Manager Ready")
        else:
            st.error("❌ Workflow Manager Failed")
    
    with col2:
        try:
            reddit_client = get_enhanced_reddit_client()
            if reddit_client.test_connection():
                st.success("✅ Reddit Connected")
            else:
                st.warning("⚠️ Reddit Connection Issues")
        except:
            st.error("❌ Reddit Client Failed")
    
    with col3:
        if os.getenv("GROQ_API_KEY"):
            st.success("✅ AI Ready")
        else:
            st.error("❌ AI Not Configured")
    
    with col4:
        try:
            db = get_database()
            st.success("✅ Database Ready")
        except:
            st.error("❌ Database Issues")

def render_main_workflow():
    """Render the main workflow interface"""
    st.header("🔄 Complete Reddit Automation Workflow")
    
    # Step 1: Article URL Input
    with st.container():
        st.subheader("📝 Step 1: Enter Article URL")
        article_url = st.text_input(
            "Medium Article URL",
            placeholder="https://medium.com/@yourname/your-article-title",
            help="Enter the URL of your Medium article or blog post"
        )
        
        if article_url and not validate_medium_url(article_url):
            st.error("❌ Please enter a valid article URL (Medium, Dev.to, personal blog, etc.)")
            return
    
    if not article_url:
        st.info("👆 Enter an article URL to start the workflow")
        return
    
    # Workflow configuration
    with st.expander("⚙️ Workflow Configuration", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            max_subreddits = st.slider("Max Subreddit Recommendations", 3, 10, 6)
            auto_analyze = st.checkbox("Auto-analyze content", value=True)
        
        with col2:
            show_compliance_details = st.checkbox("Show policy compliance details", value=True)
            enable_direct_posting = st.checkbox("Enable direct posting", value=True)
    
    # Execute workflow button
    if st.button("🚀 Start Complete Workflow", type="primary", use_container_width=True):
        execute_complete_workflow(article_url, max_subreddits, show_compliance_details, enable_direct_posting)

def execute_complete_workflow(article_url: str, max_subreddits: int, show_compliance_details: bool, enable_direct_posting: bool):
    """Execute the complete workflow"""
    
    if not st.session_state.workflow_manager:
        st.error("Workflow manager not available")
        return
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Execute workflow
    status_text.text("🔄 Executing complete workflow...")
    
    try:
        workflow_result = st.session_state.workflow_manager.execute_complete_workflow(
            article_url=article_url,
            max_subreddits=max_subreddits,
            auto_post=False  # We'll handle posting separately
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Workflow completed!")
        
        # Store result
        st.session_state.current_workflow_result = workflow_result
        
        if workflow_result.success:
            display_workflow_results(workflow_result, show_compliance_details, enable_direct_posting)
        else:
            st.error(f"❌ Workflow failed: {workflow_result.error_message}")
            display_workflow_steps(workflow_result.steps)
            
    except Exception as e:
        progress_bar.progress(0)
        status_text.text(f"❌ Error: {e}")
        st.error(f"Workflow execution failed: {e}")

def display_workflow_results(workflow_result, show_compliance_details: bool, enable_direct_posting: bool):
    """Display the complete workflow results"""
    
    if not workflow_result.final_result:
        st.error("No workflow results available")
        return
    
    final_result = workflow_result.final_result
    
    # Step progress
    display_workflow_steps(workflow_result.steps)
    
    # Content Analysis Results
    st.subheader("📊 Content Analysis")
    content_analysis = final_result.get("content_analysis", {})
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Primary Topic", content_analysis.get("primary_topic", "Unknown").title())
    with col2:
        st.metric("Technical Level", content_analysis.get("technical_level", "Unknown").title())
    with col3:
        st.metric("Content Type", content_analysis.get("content_type", "Unknown").title())
    
    if content_analysis.get("themes"):
        st.write(f"**Key Themes:** {', '.join(content_analysis['themes'])}")
    
    # Subreddit Recommendations
    st.subheader("🎯 Subreddit Recommendations")
    recommendations = final_result.get("recommendations", [])
    
    if recommendations:
        for i, rec in enumerate(recommendations):
            with st.expander(f"#{i+1} r/{rec['name']} - Score: {rec['score']*100:.1f}% ({rec['risk']} Risk)", expanded=i==0):
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Why recommended:** {rec['why']}")
                    st.write(f"**Subscribers:** {rec['subscribers']:,}")
                    
                    if show_compliance_details and rec.get('rules'):
                        st.write("**Posting Rules:**")
                        for rule in rec['rules'][:3]:
                            st.write(f"• {rule}")
                    
                    if rec.get('flair'):
                        st.info(f"📌 Required flair: {rec['flair']}")
                
                with col2:
                    risk_color = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}
                    st.metric("Risk Level", f"{risk_color.get(rec['risk'], '⚪')} {rec['risk']}")
                    
                    if enable_direct_posting:
                        if st.button(f"📝 Generate & Preview Post", key=f"preview_{rec['name']}"):
                            generate_and_preview_post(final_result["article_url"], rec['name'], workflow_result)
    
    # Generated Posts
    st.subheader("📝 Generated Posts")
    generated_posts = final_result.get("generated_posts", [])
    
    if generated_posts:
        for post in generated_posts:
            display_generated_post(post, enable_direct_posting, final_result["article_url"])
    else:
        st.warning("No posts were generated")

def display_workflow_steps(steps):
    """Display workflow execution steps"""
    with st.expander("🔍 Workflow Execution Details", expanded=False):
        for step in steps:
            status_icon = {
                "completed": "✅",
                "failed": "❌", 
                "running": "🔄",
                "pending": "⏳"
            }.get(step.status, "❓")
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                st.write(f"{status_icon} {step.status.title()}")
            
            with col2:
                st.write(f"**{step.step_name}**")
                if step.error_message:
                    st.error(f"Error: {step.error_message}")
            
            with col3:
                if step.timestamp:
                    st.write(step.timestamp.strftime("%H:%M:%S"))

def display_generated_post(post, enable_direct_posting: bool, article_url: str):
    """Display a generated post with posting options"""
    
    subreddit_name = post['subreddit']
    validation = post.get('validation', {})
    
    # Post container
    with st.container():
        st.markdown(f"### 📍 r/{subreddit_name}")
        
        # Validation status
        if validation.get('can_post', True):
            st.success("✅ Post ready for submission")
        else:
            st.error("❌ Post validation failed")
            for error in validation.get('errors', []):
                st.error(f"• {error}")
        
        # Warnings and suggestions
        if validation.get('warnings'):
            for warning in validation['warnings']:
                st.warning(f"⚠️ {warning}")
        
        if validation.get('suggestions'):
            for suggestion in validation['suggestions']:
                st.info(f"💡 {suggestion}")
        
        # Post content
        st.write(f"**Title:** {post['title']}")
        st.text_area(f"Content for r/{subreddit_name}", post['body'], height=150, disabled=True)
        
        # Compliance info
        if post.get('compliance_notes'):
            st.write("**Compliance Notes:**")
            for note in post['compliance_notes']:
                st.write(f"• {note}")
        
        if post.get('required_flair'):
            st.info(f"📌 Required flair: {post['required_flair']}")
        
        # Posting controls
        if enable_direct_posting and validation.get('can_post', True):
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button(f"🚀 Post to r/{subreddit_name}", key=f"post_{subreddit_name}", type="primary"):
                    post_to_reddit(article_url, subreddit_name, post)
            
            with col2:
                if st.button(f"📋 Copy Content", key=f"copy_{subreddit_name}"):
                    # This would copy to clipboard in a real implementation
                    st.success("Content copied!")
            
            with col3:
                st.write(f"Posting tips: {', '.join(post.get('posting_tips', [])[:2])}")
        
        st.markdown("---")

def post_to_reddit(article_url: str, subreddit_name: str, post_data: Dict):
    """Post content directly to Reddit"""
    
    if not st.session_state.workflow_manager:
        st.error("Workflow manager not available")
        return
    
    if not st.session_state.current_workflow_result:
        st.error("No workflow result available")
        return
    
    # Confirmation dialog
    if not st.session_state.get(f'confirm_post_{subreddit_name}', False):
        st.warning(f"⚠️ You are about to post to r/{subreddit_name}. This action cannot be undone.")
        if st.button(f"✅ Confirm Post to r/{subreddit_name}", key=f"confirm_{subreddit_name}"):
            st.session_state[f'confirm_post_{subreddit_name}'] = True
            st.rerun()
        return
    
    # Execute posting
    with st.spinner(f"Posting to r/{subreddit_name}..."):
        try:
            result = st.session_state.workflow_manager.post_to_selected_subreddit(
                st.session_state.current_workflow_result, 
                subreddit_name
            )
            
            if result['success']:
                st.success(f"🎉 Successfully posted to r/{subreddit_name}!")
                st.success(f"📱 Post URL: {result['post_url']}")
                
                # Add to posting history
                st.session_state.posting_history.append({
                    "subreddit": subreddit_name,
                    "url": result['post_url'],
                    "timestamp": datetime.now(),
                    "article_url": article_url
                })
                
                # Reset confirmation
                if f'confirm_post_{subreddit_name}' in st.session_state:
                    del st.session_state[f'confirm_post_{subreddit_name}']
                
            else:
                st.error(f"❌ Posting failed: {result['error']}")
                
        except Exception as e:
            st.error(f"❌ Posting error: {e}")

def generate_and_preview_post(article_url: str, subreddit_name: str, workflow_result):
    """Generate and preview a post for a specific subreddit"""
    
    if not st.session_state.workflow_manager:
        st.error("Workflow manager not available")
        return
    
    recommender = get_enhanced_subreddit_recommender()
    
    with st.spinner(f"Generating post for r/{subreddit_name}..."):
        try:
            content_analysis = workflow_result.final_result.get("content_analysis", {})
            post_data = recommender.generate_policy_compliant_post(
                article_url, subreddit_name, content_analysis
            )
            
            if post_data.get('success'):
                st.success(f"✅ Post generated for r/{subreddit_name}")
                
                # Display preview
                with st.expander(f"📝 Preview Post for r/{subreddit_name}", expanded=True):
                    st.write(f"**Title:** {post_data['title']}")
                    st.text_area("Content:", post_data['body'], height=200, disabled=True)
                    
                    if post_data.get('compliance_notes'):
                        st.write("**Compliance Notes:**")
                        for note in post_data['compliance_notes']:
                            st.write(f"• {note}")
            else:
                st.error("Failed to generate post")
                
        except Exception as e:
            st.error(f"Error generating post: {e}")

def render_posting_history():
    """Render posting history"""
    st.subheader("📋 Recent Posting History")
    
    if st.session_state.posting_history:
        for post in reversed(st.session_state.posting_history[-10:]):  # Show last 10
            with st.expander(f"r/{post['subreddit']} - {post['timestamp'].strftime('%Y-%m-%d %H:%M')}"):
                st.write(f"**Subreddit:** r/{post['subreddit']}")
                st.write(f"**Posted:** {post['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
                st.write(f"**Article:** {post['article_url']}")
                st.write(f"**Reddit Post:** [View Post]({post['url']})")
    else:
        st.info("No posting history yet")

def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    render_header()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["🔄 Complete Workflow", "📊 Analytics", "📋 History"])
    
    with tab1:
        render_main_workflow()
    
    with tab2:
        st.subheader("📊 Analytics Dashboard")
        try:
            db = get_database()
            history = db.get_post_history(limit=50)
            
            if history:
                df = pd.DataFrame(history)
                
                # Metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Posts", len(history))
                with col2:
                    successful = len([h for h in history if h.get('status') == 'posted_successfully'])
                    st.metric("Successfully Posted", successful)
                with col3:
                    if 'subreddit' in df.columns:
                        st.metric("Unique Subreddits", df['subreddit'].nunique())
                
                # Charts
                if 'subreddit' in df.columns and len(df) > 0:
                    st.subheader("Posts by Subreddit")
                    subreddit_counts = df['subreddit'].value_counts()
                    st.bar_chart(subreddit_counts)
                
                # Recent posts table
                st.subheader("Recent Posts")
                display_cols = ['title', 'subreddit', 'status', 'created_at']
                available_cols = [col for col in display_cols if col in df.columns]
                if available_cols:
                    st.dataframe(df[available_cols].head(20))
            else:
                st.info("No analytics data available yet")
                
        except Exception as e:
            st.error(f"Error loading analytics: {e}")
    
    with tab3:
        render_posting_history()

if __name__ == "__main__":
    main()
