"""
Complete Reddit Automation Workflow
Orchestrates the entire process from URL to posted content
"""
import os
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from core.enhanced_subreddit_recommender import get_enhanced_subreddit_recommender
from core.enhanced_reddit_client import get_enhanced_reddit_client
from core.database import get_database
from core.utils import validate_medium_url

@dataclass
class WorkflowStep:
    step_name: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    result: Optional[Dict] = None
    error_message: Optional[str] = None
    timestamp: Optional[datetime] = None

@dataclass
class WorkflowResult:
    success: bool
    workflow_id: str
    steps: List[WorkflowStep]
    final_result: Optional[Dict] = None
    error_message: Optional[str] = None

class RedditAutomationWorkflow:
    """Complete workflow manager for Reddit automation"""
    
    def __init__(self):
        self.recommender = get_enhanced_subreddit_recommender()
        self.reddit_client = get_enhanced_reddit_client()
        self.database = get_database()
        self.workflow_id = None
    
    def execute_complete_workflow(self, article_url: str, max_subreddits: int = 6, auto_post: bool = False, selected_subreddit: str = None) -> WorkflowResult:
        """Execute the complete workflow from URL to posted content"""
        
        self.workflow_id = f"workflow_{int(time.time())}"
        steps = []
        
        try:
            # Step 1: Validate URL
            step = WorkflowStep("URL Validation", "running", timestamp=datetime.now())
            steps.append(step)
            
            if not validate_medium_url(article_url):
                step.status = "failed"
                step.error_message = "Invalid article URL"
                return WorkflowResult(False, self.workflow_id, steps, error_message="Invalid URL")
            
            step.status = "completed"
            step.result = {"url": article_url, "valid": True}
            
            # Step 2: Analyze Content
            step = WorkflowStep("Content Analysis", "running", timestamp=datetime.now())
            steps.append(step)
            
            content_analysis = self.recommender.analyze_article_content(article_url)
            
            step.status = "completed"
            step.result = content_analysis
            
            # Step 3: Get Subreddit Recommendations
            step = WorkflowStep("Subreddit Recommendations", "running", timestamp=datetime.now())
            steps.append(step)
            
            recommendations = self.recommender.recommend_subreddits(article_url, max_subreddits)
            
            if not recommendations:
                step.status = "failed"
                step.error_message = "No suitable subreddits found"
                return WorkflowResult(False, self.workflow_id, steps, error_message="No subreddits found")
            
            step.status = "completed"
            step.result = {
                "recommendations": [
                    {
                        "name": rec.name,
                        "score": rec.overall_score,
                        "risk": rec.risk_level,
                        "why": rec.why_recommended,
                        "subscribers": rec.subscribers,
                        "rules": rec.posting_rules,
                        "flair": rec.required_flair
                    }
                    for rec in recommendations
                ]
            }
            
            # Step 4: Generate Policy-Compliant Posts
            step = WorkflowStep("Post Generation", "running", timestamp=datetime.now())
            steps.append(step)
            
            generated_posts = []
            target_subreddits = [selected_subreddit] if selected_subreddit else [rec.name for rec in recommendations[:3]]
            
            for subreddit_name in target_subreddits:
                try:
                    post_data = self.recommender.generate_policy_compliant_post(
                        article_url, subreddit_name, content_analysis
                    )
                    
                    if post_data.get('success'):
                        generated_posts.append({
                            "subreddit": subreddit_name,
                            "title": post_data['title'],
                            "body": post_data['body'],
                            "compliance_notes": post_data.get('compliance_notes', []),
                            "required_flair": post_data.get('required_flair', ''),
                            "posting_tips": post_data.get('posting_tips', [])
                        })
                    
                except Exception as e:
                    print(f"Failed to generate post for r/{subreddit_name}: {e}")
            
            if not generated_posts:
                step.status = "failed"
                step.error_message = "Failed to generate any posts"
                return WorkflowResult(False, self.workflow_id, steps, error_message="Post generation failed")
            
            step.status = "completed"
            step.result = {"generated_posts": generated_posts}
            
            # Step 5: Validate Posts (Pre-submission check)
            step = WorkflowStep("Post Validation", "running", timestamp=datetime.now())
            steps.append(step)
            
            validated_posts = []
            for post in generated_posts:
                validation = self.reddit_client.validate_post_before_submission(
                    post['subreddit'], 
                    post['title'], 
                    post['body'], 
                    post['required_flair']
                )
                
                post['validation'] = validation
                validated_posts.append(post)
            
            step.status = "completed"
            step.result = {"validated_posts": validated_posts}
            
            # Step 6: Auto-post if requested
            if auto_post and selected_subreddit:
                step = WorkflowStep("Reddit Posting", "running", timestamp=datetime.now())
                steps.append(step)
                
                # Find the post for the selected subreddit
                target_post = next((p for p in validated_posts if p['subreddit'] == selected_subreddit), None)
                
                if target_post and target_post['validation']['can_post']:
                    posting_result = self.reddit_client.submit_post_with_validation(
                        target_post['subreddit'],
                        target_post['title'],
                        target_post['body'],
                        target_post['required_flair']
                    )
                    
                    if posting_result.success:
                        step.status = "completed"
                        step.result = {
                            "posted": True,
                            "post_id": posting_result.post_id,
                            "post_url": posting_result.post_url,
                            "subreddit": selected_subreddit
                        }
                        
                        # Save to database
                        self.database.add_post_history(
                            article_url=article_url,
                            title=target_post['title'],
                            content=target_post['body'],
                            subreddit=selected_subreddit,
                            status="posted_successfully"
                        )
                        
                    else:
                        step.status = "failed"
                        step.error_message = posting_result.error_message
                        
                        # Save failed attempt to database
                        self.database.add_post_history(
                            article_url=article_url,
                            title=target_post['title'],
                            content=target_post['body'],
                            subreddit=selected_subreddit,
                            status="posting_failed"
                        )
                else:
                    step.status = "failed"
                    step.error_message = "Post validation failed or target post not found"
              # Final result compilation
            # Find the subreddit recommendations step
            recommendations_step = next((s for s in steps if s.step_name == "Subreddit Recommendations"), None)
            recommendations_data = recommendations_step.result.get("recommendations", []) if recommendations_step and recommendations_step.result else []
            
            final_result = {
                "workflow_id": self.workflow_id,
                "article_url": article_url,
                "content_analysis": content_analysis,
                "recommendations": recommendations_data,
                "generated_posts": validated_posts,
                "posting_result": steps[-1].result if auto_post and len(steps) > 5 else None,
                "timestamp": datetime.now().isoformat()
            }
            
            return WorkflowResult(True, self.workflow_id, steps, final_result)
            
        except Exception as e:
            # Mark current step as failed
            if steps and steps[-1].status == "running":
                steps[-1].status = "failed"
                steps[-1].error_message = str(e)
            
            return WorkflowResult(False, self.workflow_id, steps, error_message=str(e))
    
    def get_workflow_summary(self, workflow_result: WorkflowResult) -> Dict:
        """Get a summary of the workflow results"""
        if not workflow_result.success:
            return {
                "status": "failed",
                "error": workflow_result.error_message,
                "completed_steps": len([s for s in workflow_result.steps if s.status == "completed"])
            }
        
        final_result = workflow_result.final_result
        
        return {
            "status": "success",
            "workflow_id": workflow_result.workflow_id,
            "article_url": final_result["article_url"],
            "content_topic": final_result["content_analysis"].get("primary_topic", "general"),
            "recommendations_count": len(final_result["recommendations"]),
            "posts_generated": len(final_result["generated_posts"]),
            "top_recommendation": final_result["recommendations"][0]["name"] if final_result["recommendations"] else None,
            "posted": final_result["posting_result"] is not None,
            "post_url": final_result["posting_result"]["post_url"] if final_result.get("posting_result") else None
        }
    
    def get_best_recommendation(self, workflow_result: WorkflowResult) -> Optional[Dict]:
        """Get the best subreddit recommendation from workflow results"""
        if not workflow_result.success or not workflow_result.final_result:
            return None
        
        recommendations = workflow_result.final_result.get("recommendations", [])
        if not recommendations:
            return None
        
        return recommendations[0]  # Already sorted by score
    
    def post_to_selected_subreddit(self, workflow_result: WorkflowResult, subreddit_name: str) -> Dict:
        """Post to a specific subreddit from workflow results"""
        if not workflow_result.success:
            return {"success": False, "error": "Workflow was not successful"}
        
        # Find the generated post for this subreddit
        generated_posts = workflow_result.final_result.get("generated_posts", [])
        target_post = next((p for p in generated_posts if p['subreddit'] == subreddit_name), None)
        
        if not target_post:
            return {"success": False, "error": f"No generated post found for r/{subreddit_name}"}
        
        # Check validation
        if not target_post['validation']['can_post']:
            return {
                "success": False, 
                "error": f"Post validation failed: {'; '.join(target_post['validation']['errors'])}"
            }
        
        # Submit the post
        posting_result = self.reddit_client.submit_post_with_validation(
            target_post['subreddit'],
            target_post['title'],
            target_post['body'],
            target_post['required_flair']
        )
        
        if posting_result.success:
            # Save to database
            self.database.add_post_history(
                article_url=workflow_result.final_result["article_url"],
                title=target_post['title'],
                content=target_post['body'],
                subreddit=subreddit_name,
                status="posted_successfully"
            )
            
            return {
                "success": True,
                "post_id": posting_result.post_id,
                "post_url": posting_result.post_url,
                "subreddit": subreddit_name
            }
        else:
            # Save failed attempt
            self.database.add_post_history(
                article_url=workflow_result.final_result["article_url"],
                title=target_post['title'],
                content=target_post['body'],
                subreddit=subreddit_name,
                status="posting_failed"
            )
            
            return {
                "success": False,
                "error": posting_result.error_message
            }
    
    def run_complete_workflow(self, url: str, dry_run: bool = False, **kwargs) -> Dict:
        """Run complete workflow (compatible interface)"""
        try:
            # Use the existing execute_complete_workflow method
            result = self.execute_complete_workflow(
                article_url=url,
                auto_post=not dry_run,
                **kwargs
            )
            
            # Convert to compatible format
            if result.success:
                final_result = result.final_result or {}
                
                # Ensure recommendations are always present
                if 'recommendations' not in final_result:
                    # Try to get recommendations from steps
                    for step in result.steps:
                        if step.step_name == "Generate Recommendations" and step.result:
                            final_result['recommendations'] = step.result.get('recommendations', [])
                            break
                    
                    # If still no recommendations, add empty list
                    if 'recommendations' not in final_result:
                        final_result['recommendations'] = []
                
                return {
                    "success": True,
                    "steps": [{"name": s.step_name, "status": s.status, "result": s.result} for s in result.steps],
                    "recommendations": final_result.get('recommendations', []),
                    "final_post": final_result.get('generated_post'),
                    "workflow_id": result.workflow_id
                }
            else:
                return {
                    "success": False,
                    "error": result.error_message,
                    "steps": [{"name": s.step_name, "status": s.status, "error": s.error_message} for s in result.steps],
                    "recommendations": [],  # Always include recommendations key
                    "workflow_id": result.workflow_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "steps": [],
                "recommendations": [],  # Always include recommendations key
                "workflow_id": f"failed_{int(time.time())}"
            }

# Global instance
_workflow_manager = None

def get_workflow_manager():
    """Get the workflow manager instance"""
    global _workflow_manager
    if _workflow_manager is None:
        _workflow_manager = RedditAutomationWorkflow()
    return _workflow_manager
