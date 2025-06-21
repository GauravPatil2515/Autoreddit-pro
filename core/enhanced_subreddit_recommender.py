"""
Enhanced Subreddit Recommender with Policy Compliance
"""
import os
import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False

@dataclass
class SubredditRecommendation:
    name: str
    relevance_score: float
    compliance_score: float
    overall_score: float
    why_recommended: str
    risk_level: str
    subscribers: int = 100000
    posting_rules: List[str] = None
    required_flair: str = ""
    title_requirements: str = ""
    content_guidelines: str = ""

class EnhancedSubredditRecommender:
    def __init__(self):
        self.groq_client = None
        if GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
            try:
                self.groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            except:
                pass
        
        # Enhanced subreddit database with detailed rules
        self.subreddit_database = {
            "programming": {
                "focus": ["programming", "coding", "development", "software"],
                "rules": [
                    "No self-promotion unless it's educational",
                    "Include code examples when relevant", 
                    "Be specific in titles",
                    "No blog spam"
                ],
                "required_flair": "",
                "title_format": "Clear, descriptive titles",
                "content_type": "technical discussion",
                "subscribers": 6778000,
                "activity_level": "high",
                "posting_guidelines": "Focus on programming concepts, avoid direct promotion"
            },
            "Python": {
                "focus": ["python", "programming", "data science", "machine learning"],
                "rules": [
                    "Python-specific content only",
                    "Include code snippets when helpful",
                    "Mark beginner vs advanced content",
                    "No duplicate posts"
                ],
                "required_flair": "",
                "title_format": "Descriptive with [Topic] tags when relevant",
                "content_type": "python discussion",
                "subscribers": 1200000,
                "activity_level": "very high",
                "posting_guidelines": "Python-focused, educational content preferred"
            },
            "MachineLearning": {
                "focus": ["machine learning", "AI", "data science", "research"],
                "rules": [
                    "Research-focused content",
                    "Include methodology when discussing projects",
                    "Academic tone preferred",
                    "Cite sources"
                ],
                "required_flair": "Discussion",
                "title_format": "Academic style with clear topic",
                "content_type": "research discussion",
                "subscribers": 2800000,
                "activity_level": "high",
                "posting_guidelines": "Academic approach, research-backed content"
            },
            "webdev": {
                "focus": ["web development", "javascript", "react", "frontend", "backend"],
                "rules": [
                    "Web development focused",
                    "Include live demos when possible",
                    "Mention tech stack used",
                    "Be helpful to community"
                ],
                "required_flair": "",
                "title_format": "Clear about technology used",
                "content_type": "web development",
                "subscribers": 850000,
                "activity_level": "high",
                "posting_guidelines": "Practical web development content"
            },
            "entrepreneur": {
                "focus": ["business", "startup", "entrepreneurship", "marketing"],
                "rules": [
                    "Business-focused content",
                    "Share actionable insights",
                    "No direct sales pitches",
                    "Community value first"
                ],
                "required_flair": "",
                "title_format": "Value-focused titles",
                "content_type": "business discussion",
                "subscribers": 1100000,
                "activity_level": "medium",
                "posting_guidelines": "Business insights, avoid promotional content"
            },
            "datascience": {
                "focus": ["data science", "analytics", "statistics", "visualization"],
                "rules": [
                    "Data science content only",
                    "Include methodology",
                    "Show your work/code",
                    "Educational focus"
                ],
                "required_flair": "",
                "title_format": "Clear about data/methods used",
                "content_type": "data science",
                "subscribers": 650000,
                "activity_level": "medium",
                "posting_guidelines": "Technical data science content with examples"
            }
        }
    
    def analyze_article_content(self, article_url: str) -> Dict:
        """Analyze article content to understand topics and themes"""
        # Extract basic info from URL
        url_keywords = self._extract_keywords_from_url(article_url)
        
        if self.groq_client:
            try:
                # Use AI to analyze content
                return self._ai_analyze_content(article_url, url_keywords)
            except:
                pass
        
        # Fallback analysis
        return self._fallback_content_analysis(url_keywords)
    
    def _extract_keywords_from_url(self, url: str) -> List[str]:
        """Extract keywords from URL"""
        # Remove common URL parts and extract meaningful words
        cleaned = re.sub(r'https?://|www\.|\.com|\.org|/@|\-|_', ' ', url.lower())
        words = re.findall(r'\b[a-z]{3,}\b', cleaned)
        
        # Filter out common words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'had', 'but', 'article', 'post', 'blog', 'medium'}
        keywords = [word for word in words if word not in stop_words]
        
        return keywords[:10]  # Return top 10 keywords
    
    def _ai_analyze_content(self, article_url: str, url_keywords: List[str]) -> Dict:
        """Use AI to analyze article content"""
        prompt = f"""
        Analyze this article URL and keywords to determine the main topics and themes:
        
        URL: {article_url}
        Keywords: {', '.join(url_keywords)}
        
        Determine:
        1. Primary topic (programming, business, data science, etc.)
        2. Technical level (beginner, intermediate, advanced)
        3. Content type (tutorial, discussion, case study, etc.)
        4. Target audience
        5. Key themes (3-5 main themes)
        
        Respond in JSON format:
        {{
            "primary_topic": "...",
            "technical_level": "...",
            "content_type": "...",
            "target_audience": "...",
            "themes": ["theme1", "theme2", "theme3"],
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }}
        """
        
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
            temperature=0.3
        )
        
        try:
            import json
            return json.loads(response.choices[0].message.content)
        except:
            return self._fallback_content_analysis(url_keywords)
    
    def _fallback_content_analysis(self, keywords: List[str]) -> Dict:
        """Fallback content analysis based on keywords"""
        # Determine primary topic based on keywords
        tech_words = ['python', 'javascript', 'programming', 'code', 'development', 'software', 'tech']
        business_words = ['business', 'startup', 'entrepreneur', 'marketing', 'sales', 'growth']
        data_words = ['data', 'science', 'machine', 'learning', 'ai', 'analytics', 'statistics']
        
        tech_score = sum(1 for word in keywords if word in tech_words)
        business_score = sum(1 for word in keywords if word in business_words)
        data_score = sum(1 for word in keywords if word in data_words)
        
        if tech_score >= business_score and tech_score >= data_score:
            primary_topic = "programming"
        elif business_score >= data_score:
            primary_topic = "business"
        else:
            primary_topic = "data_science"
        
        return {
            "primary_topic": primary_topic,
            "technical_level": "intermediate",
            "content_type": "discussion",
            "target_audience": "developers",
            "themes": keywords[:3],
            "keywords": keywords
        }
    
    def get_recommendations(self, content: str, num_recommendations: int = 5) -> List[Dict]:
        """
        Get subreddit recommendations for content (compatible interface)
        """
        try:
            # Use the existing recommend_subreddits method
            recommendations = self.recommend_subreddits(
                article_url="",  # We'll analyze content directly
                max_recommendations=num_recommendations
            )
            
            # Convert to simpler format for compatibility
            result = []
            for rec in recommendations:
                result.append({
                    "name": rec.name,
                    "score": rec.overall_score,
                    "reason": rec.why_recommended,
                    "risk_level": rec.risk_level,
                    "subscribers": rec.subscribers
                })
            
            return result
            
        except Exception as e:
            # Fallback to simple recommendations
            return self._get_fallback_recommendations(content, num_recommendations)
    
    def _get_fallback_recommendations(self, content: str, num_recommendations: int) -> List[Dict]:
        """Fallback recommendations when AI is not available"""
        content_lower = content.lower()
        fallback_recs = []
        
        # Simple keyword-based matching
        if any(word in content_lower for word in ["python", "programming", "code", "developer"]):
            fallback_recs.extend([
                {"name": "learnpython", "score": 0.8, "reason": "Python programming content", "risk_level": "low", "subscribers": 900000},
                {"name": "Python", "score": 0.9, "reason": "Python-specific content", "risk_level": "low", "subscribers": 800000},
                {"name": "programming", "score": 0.7, "reason": "General programming content", "risk_level": "medium", "subscribers": 4000000}
            ])
        
        if any(word in content_lower for word in ["web", "javascript", "react", "frontend"]):
            fallback_recs.extend([
                {"name": "webdev", "score": 0.8, "reason": "Web development content", "risk_level": "low", "subscribers": 700000},
                {"name": "javascript", "score": 0.9, "reason": "JavaScript content", "risk_level": "medium", "subscribers": 500000}
            ])
        
        if any(word in content_lower for word in ["data", "science", "machine learning", "ai"]):
            fallback_recs.extend([
                {"name": "MachineLearning", "score": 0.9, "reason": "AI/ML content", "risk_level": "low", "subscribers": 600000},
                {"name": "datascience", "score": 0.8, "reason": "Data science content", "risk_level": "low", "subscribers": 400000}
            ])
        
        # Default fallbacks
        if not fallback_recs:
            fallback_recs = [
                {"name": "programming", "score": 0.6, "reason": "General programming community", "risk_level": "medium", "subscribers": 4000000},
                {"name": "learnprogramming", "score": 0.7, "reason": "Learning-focused community", "risk_level": "low", "subscribers": 3000000}
            ]
        
        return fallback_recs[:num_recommendations]
    
    def recommend_subreddits(self, article_url: str, max_recommendations: int = 6) -> List[SubredditRecommendation]:
        """Original method for detailed recommendations"""
        content_analysis = self.analyze_article_content(article_url)
        recommendations = []
        
        for subreddit_name, subreddit_data in self.subreddit_database.items():
            relevance_score = self._calculate_relevance_score(content_analysis, subreddit_data)
            compliance_score = self._calculate_compliance_score(content_analysis, subreddit_data)
            overall_score = (relevance_score * 0.7) + (compliance_score * 0.3)
            
            recommendation = SubredditRecommendation(
                name=subreddit_name,
                relevance_score=relevance_score,
                compliance_score=compliance_score,
                overall_score=overall_score,
                why_recommended=self._generate_recommendation_reason(subreddit_name, content_analysis, relevance_score),
                risk_level=self._assess_risk_level(subreddit_data, compliance_score),
                subscribers=subreddit_data.get('subscribers', 100000),
                posting_rules=subreddit_data.get('rules', []),
                required_flair=subreddit_data.get('required_flair', ''),
                title_requirements=subreddit_data.get('title_format', ''),
                content_guidelines=subreddit_data.get('posting_guidelines', '')
            )
            
            if overall_score > 0.3:  # Only include relevant subreddits
                recommendations.append(recommendation)
        
        # Sort by overall score
        recommendations.sort(key=lambda x: x.overall_score, reverse=True)
        return recommendations[:max_recommendations]
    
    def _calculate_relevance_score(self, content_analysis: Dict, subreddit_data: Dict) -> float:
        """Calculate how relevant the content is to the subreddit"""
        score = 0.0
        content_keywords = content_analysis.get('keywords', []) + content_analysis.get('themes', [])
        subreddit_focus = subreddit_data.get('focus', [])
        
        # Check keyword overlap
        for keyword in content_keywords:
            for focus_area in subreddit_focus:
                if keyword.lower() in focus_area.lower() or focus_area.lower() in keyword.lower():
                    score += 0.2
        
        # Topic alignment
        primary_topic = content_analysis.get('primary_topic', '')
        if primary_topic in subreddit_focus:
            score += 0.4
        
        return min(score, 1.0)
    
    def _calculate_compliance_score(self, content_analysis: Dict, subreddit_data: Dict) -> float:
        """Calculate compliance with subreddit rules"""
        # Base compliance score
        score = 0.7
        
        # Check if content type matches subreddit expectations
        content_type = content_analysis.get('content_type', '')
        if content_type == 'tutorial' and 'educational' in subreddit_data.get('posting_guidelines', ''):
            score += 0.2
        
        # Technical level appropriateness
        tech_level = content_analysis.get('technical_level', '')
        if tech_level in ['intermediate', 'advanced'] and 'research' in subreddit_data.get('content_type', ''):
            score += 0.1
        
        return min(score, 1.0)
    
    def _assess_risk_level(self, subreddit_data: Dict, compliance_score: float) -> str:
        """Assess posting risk level"""
        if compliance_score >= 0.8:
            return "LOW"
        elif compliance_score >= 0.6:
            return "MEDIUM"
        else:
            return "HIGH"
    
    def _generate_recommendation_reason(self, subreddit_name: str, content_analysis: Dict, relevance_score: float) -> str:
        """Generate explanation for why this subreddit was recommended"""
        primary_topic = content_analysis.get('primary_topic', 'general')
        
        if relevance_score >= 0.8:
            return f"Excellent match for {primary_topic} content with high community engagement"
        elif relevance_score >= 0.6:
            return f"Good fit for {primary_topic} discussions in r/{subreddit_name}"
        else:
            return f"Moderate relevance for {primary_topic} topics"
    
    def generate_policy_compliant_post(self, article_url: str, subreddit_name: str, content_analysis: Dict = None) -> Dict:
        """Generate a post that complies with specific subreddit policies"""
        if not content_analysis:
            content_analysis = self.analyze_article_content(article_url)
        
        subreddit_data = self.subreddit_database.get(subreddit_name, {})
        
        if self.groq_client:
            try:
                return self._ai_generate_compliant_post(article_url, subreddit_name, subreddit_data, content_analysis)
            except:
                pass
        
        # Fallback generation
        return self._fallback_post_generation(article_url, subreddit_name, subreddit_data)
    
    def _ai_generate_compliant_post(self, article_url: str, subreddit_name: str, subreddit_data: Dict, content_analysis: Dict) -> Dict:
        """Use AI to generate policy-compliant post"""
        rules = "\n".join(subreddit_data.get('rules', []))
        guidelines = subreddit_data.get('posting_guidelines', '')
        title_format = subreddit_data.get('title_format', '')
        
        prompt = f"""
        Create a Reddit post for r/{subreddit_name} about this article: {article_url}
        
        Article Analysis:
        - Primary Topic: {content_analysis.get('primary_topic', 'general')}
        - Technical Level: {content_analysis.get('technical_level', 'intermediate')}
        - Content Type: {content_analysis.get('content_type', 'discussion')}
        - Key Themes: {', '.join(content_analysis.get('themes', []))}
        
        Subreddit Rules:
        {rules}
        
        Posting Guidelines:
        {guidelines}
        
        Title Requirements:
        {title_format}
        
        IMPORTANT: Follow ALL rules strictly. Make the post:
        1. Valuable to the community
        2. Discussion-focused, not promotional
        3. Compliant with all listed rules
        4. Engaging and authentic
        
        Generate:
        TITLE: [engaging, rule-compliant title under 300 chars]
        BODY: [valuable discussion post that follows guidelines]
        
        Make it feel natural and community-focused.
        """
        
        response = self.groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.7
        )
        
        result_text = response.choices[0].message.content
        title, body = self._parse_ai_response(result_text)
        
        return {
            "title": title,
            "body": body,
            "success": True,
            "compliance_notes": self._generate_compliance_notes(subreddit_data),
            "required_flair": subreddit_data.get('required_flair', ''),
            "posting_tips": self._generate_posting_tips(subreddit_name)
        }
    
    def _parse_ai_response(self, text: str) -> Tuple[str, str]:
        """Parse AI response to extract title and body"""
        import re
        title_match = re.search(r'TITLE:\s*(.+)', text)
        body_match = re.search(r'BODY:\s*(.+)', text, re.DOTALL)
        
        title = title_match.group(1).strip() if title_match else "Interesting Article Discussion"
        body = body_match.group(1).strip() if body_match else text
        
        return title, body
    
    def _fallback_post_generation(self, article_url: str, subreddit_name: str, subreddit_data: Dict) -> Dict:
        """Fallback post generation"""
        guidelines = subreddit_data.get('posting_guidelines', 'Share valuable content')
        
        title = f"Thought-provoking article worth discussing in r/{subreddit_name}"
        body = f"""Found this interesting article that I thought would spark good discussion here:

{article_url}

The article covers some important points that align with our community's interests. I'm curious about your thoughts and experiences with this topic.

What's your take on the main points discussed? Have you encountered similar situations or concepts?

Looking forward to hearing different perspectives!"""
        
        return {
            "title": title,
            "body": body,
            "success": True,
            "compliance_notes": self._generate_compliance_notes(subreddit_data),
            "required_flair": subreddit_data.get('required_flair', ''),
            "posting_tips": self._generate_posting_tips(subreddit_name)
        }
    
    def _generate_compliance_notes(self, subreddit_data: Dict) -> List[str]:
        """Generate compliance notes for the user"""
        notes = []
        
        if subreddit_data.get('required_flair'):
            notes.append(f"⚠️ Required flair: {subreddit_data['required_flair']}")
        
        if 'no self-promotion' in str(subreddit_data.get('rules', [])).lower():
            notes.append("📝 Focus on discussion value, not promotion")
        
        if 'code' in str(subreddit_data.get('rules', [])).lower():
            notes.append("💻 Include code examples if relevant")
        
        return notes
    
    def _generate_posting_tips(self, subreddit_name: str) -> List[str]:
        """Generate posting tips for the subreddit"""
        tips = [
            "Engage with comments promptly",
            "Follow up with additional insights",
            "Be open to feedback and discussion"
        ]
        
        if subreddit_name.lower() in ['programming', 'python']:
            tips.append("Include technical details in discussions")
        elif subreddit_name.lower() in ['entrepreneur', 'business']:
            tips.append("Focus on actionable insights")
        
        return tips
    
    def generate_post(self, content: str, subreddit: str) -> Dict:
        """Generate a post for specific subreddit (compatible interface)"""
        try:
            if self.groq_client:
                # Use AI to generate post
                prompt = f"""
Create a Reddit post for r/{subreddit} based on this content:

{content}

Requirements:
- Write a clear, engaging title (max 300 characters)
- Create informative post content 
- Follow r/{subreddit} community guidelines
- Make it educational and valuable
- Avoid promotional language

Format your response as:
TITLE: [your title here]
CONTENT: [your post content here]
"""
                
                try:
                    response = self.groq_client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1000,
                        temperature=0.7
                    )
                    
                    generated_text = response.choices[0].message.content
                    
                    # Parse the response
                    if "TITLE:" in generated_text and "CONTENT:" in generated_text:
                        title_part = generated_text.split("TITLE:")[1].split("CONTENT:")[0].strip()
                        content_part = generated_text.split("CONTENT:")[1].strip()
                        
                        return {
                            "title": title_part,
                            "content": content_part,
                            "subreddit": subreddit
                        }
                except Exception as e:
                    print(f"AI generation failed: {e}")
                    
            # Fallback to template-based generation
            return self._generate_fallback_post(content, subreddit)
            
        except Exception as e:
            return self._generate_fallback_post(content, subreddit)
    
    def _generate_fallback_post(self, content: str, subreddit: str) -> Dict:
        """Generate a basic post using templates"""
        # Extract key information
        content_lower = content.lower()
        
        # Generate title based on content
        if "python" in content_lower:
            title = "Useful Python Tips and Best Practices"
        elif "programming" in content_lower:
            title = "Programming Best Practices Worth Knowing"
        elif "tutorial" in content_lower:
            title = "Step-by-Step Tutorial Guide"
        else:
            title = "Interesting Article Discussion"
        
        # Generate content
        post_content = f"""I wanted to share some insights from a recent article I read.

## Key Points:

{content[:500]}{"..." if len(content) > 500 else ""}

## Discussion:

What are your thoughts on this approach? Have you encountered similar situations in your projects?

Looking forward to hearing your experiences and insights!

---
*Let me know if you'd like me to elaborate on any specific points.*"""

        return {
            "title": title,
            "content": post_content,
            "subreddit": subreddit
        }

# Global instance
_enhanced_recommender = None

def get_enhanced_subreddit_recommender():
    """Get the enhanced subreddit recommender instance"""
    global _enhanced_recommender
    if _enhanced_recommender is None:
        _enhanced_recommender = EnhancedSubredditRecommender()
    return _enhanced_recommender
