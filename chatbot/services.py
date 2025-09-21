import os
import json
import requests
from typing import Dict, Any, Optional
from django.conf import settings

class ChatbotService:
    """Service class for handling chatbot API requests to Hugging Face and OpenAI"""
    
    def __init__(self):
        # Use environment variables - don't hardcode API keys
        self.huggingface_api_key = os.getenv('HUGGINGFACE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.huggingface_api_url = "https://api-inference.huggingface.co/models/"
        self.default_model = "microsoft/DialoGPT-medium"
        
    def get_career_focused_response(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """
        Generate career-focused chatbot response using available APIs
        Falls back to rule-based responses if APIs are unavailable
        """
        # Try Hugging Face first
        if self.huggingface_api_key:
            try:
                response = self._query_huggingface(message, user_context)
                if response:
                    return self._enhance_career_context(response, message)
            except Exception as e:
                print(f"Hugging Face API error: {e}")
        
        # Try OpenAI as fallback
        if self.openai_api_key:
            try:
                response = self._query_openai(message, user_context)
                if response:
                    return response
            except Exception as e:
                print(f"OpenAI API error: {e}")
        
        # Fallback to enhanced rule-based responses
        return self._rule_based_career_response(message, user_context)
    
    def _query_huggingface(self, message: str, user_context: Dict[str, Any] = None) -> Optional[str]:
        """Query Hugging Face Inference API"""
        if not self.huggingface_api_key:
            return None
            
        headers = {"Authorization": f"Bearer {self.huggingface_api_key}"}
        
        # Enhance message with career context
        enhanced_message = self._add_career_context(message, user_context)
        
        data = {
            "inputs": enhanced_message,
            "parameters": {
                "max_length": 100,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(
                f"{self.huggingface_api_url}{self.default_model}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Extract the response part (after the input)
                    if enhanced_message in generated_text:
                        return generated_text.replace(enhanced_message, '').strip()
                    return generated_text.strip()
            
        except requests.RequestException as e:
            print(f"Request error: {e}")
            
        return None
    
    def _query_openai(self, message: str, user_context: Dict[str, Any] = None) -> Optional[str]:
        """Query OpenAI API (if available)"""
        if not self.openai_api_key:
            return None
            
        try:
            # Note: This requires the openai package to be installed
            import openai
            openai.api_key = self.openai_api_key
            
            system_prompt = self._get_career_system_prompt(user_context)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except ImportError:
            print("OpenAI package not installed")
        except Exception as e:
            print(f"OpenAI API error: {e}")
            
        return None
    
    def _add_career_context(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """Add career context to the message for better responses"""
        context_prefix = "As a career advisor, please help with this question: "
        
        if user_context:
            role = user_context.get('current_role', '')
            industry = user_context.get('industry_interest', '')
            if role or industry:
                context_prefix += f"(User is a {role} interested in {industry}) "
        
        return context_prefix + message
    
    def _get_career_system_prompt(self, user_context: Dict[str, Any] = None) -> str:
        """Get system prompt for career-focused responses"""
        base_prompt = """You are a helpful career advisor and mentor. Provide practical, 
        actionable advice about careers, job searching, resume writing, interview preparation, 
        skill development, and professional growth. Keep responses concise and supportive."""
        
        if user_context:
            role = user_context.get('current_role', '')
            industry = user_context.get('industry_interest', '')
            experience = user_context.get('experience_years', 0)
            
            if any([role, industry, experience]):
                base_prompt += f" The user is a {role} with {experience} years of experience, interested in {industry}."
        
        return base_prompt
    
    def _enhance_career_context(self, response: str, original_message: str) -> str:
        """Enhance AI response with career-specific context"""
        # Add career-specific suggestions based on the original message
        message_lower = original_message.lower()
        
        enhancements = []
        
        if 'resume' in message_lower:
            enhancements.append("💡 Pro tip: Quantify your achievements with specific numbers and metrics.")
        elif 'interview' in message_lower:
            enhancements.append("💡 Pro tip: Use the STAR method (Situation, Task, Action, Result) for behavioral questions.")
        elif 'skill' in message_lower:
            enhancements.append("💡 Pro tip: Focus on skills that are in high demand in your target industry.")
        elif 'salary' in message_lower or 'negotiate' in message_lower:
            enhancements.append("💡 Pro tip: Research market rates using sites like Glassdoor, PayScale, or Levels.fyi.")
        
        if enhancements:
            return response + "\n\n" + "\n".join(enhancements)
        
        return response
    
    def _rule_based_career_response(self, message: str, user_context: Dict[str, Any] = None) -> str:
        """Enhanced rule-based career responses as fallback"""
        text = message.lower()
        
        # Resume-related queries
        if any(word in text for word in ['resume', 'cv', 'curriculum']):
            return self._get_resume_advice(text, user_context)
        
        # Interview-related queries
        if any(word in text for word in ['interview', 'preparation', 'questions']):
            return self._get_interview_advice(text, user_context)
        
        # Skills-related queries
        if any(word in text for word in ['skill', 'learn', 'technology', 'programming']):
            return self._get_skills_advice(text, user_context)
        
        # Career change queries
        if any(word in text for word in ['career change', 'transition', 'switch']):
            return self._get_career_change_advice(text, user_context)
        
        # Salary/negotiation queries
        if any(word in text for word in ['salary', 'negotiate', 'pay', 'compensation']):
            return self._get_salary_advice(text, user_context)
        
        # Networking queries
        if any(word in text for word in ['network', 'linkedin', 'connections']):
            return self._get_networking_advice(text, user_context)
        
        # Job search queries
        if any(word in text for word in ['job search', 'job hunt', 'apply', 'application']):
            return self._get_job_search_advice(text, user_context)
        
        # Default response
        return self._get_default_response(user_context)
    
    def _get_resume_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        advice = [
            "📄 **Resume Tips:**",
            "• Use a clean, professional format with consistent styling",
            "• Quantify achievements with specific numbers and metrics",
            "• Tailor your resume for each job application",
            "• Include relevant keywords from the job description",
            "• Keep it to 1-2 pages maximum",
            "• Start bullet points with strong action verbs"
        ]
        
        if user_context and user_context.get('experience_years', 0) == 0:
            advice.append("• For entry-level: Highlight projects, internships, and relevant coursework")
        
        return "\n".join(advice)
    
    def _get_interview_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        return """🎯 **Interview Preparation:**
• Research the company thoroughly (mission, values, recent news)
• Practice STAR method responses for behavioral questions
• Prepare thoughtful questions to ask the interviewer
• Review your resume and be ready to discuss each experience
• Practice common technical questions for your field
• Plan your outfit and route to the interview location
• Bring multiple copies of your resume and a notepad"""
    
    def _get_skills_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        advice = """🚀 **Skill Development Tips:**
• Focus on in-demand skills in your target industry
• Build a portfolio to showcase your abilities
• Consider online courses (Coursera, Udemy, edX)
• Practice with real projects and challenges
• Stay updated with industry trends"""
        
        if 'programming' in text or 'coding' in text:
            advice += "\n\n**High-demand Programming Skills:**\n• Python, JavaScript, SQL\n• Cloud platforms (AWS, Azure, GCP)\n• Data analysis and visualization\n• Machine learning basics"
        
        return advice
    
    def _get_career_change_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        return """🔄 **Career Transition Strategy:**
• Identify transferable skills from your current role
• Network with professionals in your target field
• Consider informational interviews to learn about the industry
• Build relevant skills through courses or side projects
• Look for bridge roles that combine old and new skills
• Update your LinkedIn to reflect your career interests
• Consider temporary or contract work to gain experience"""
    
    def _get_salary_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        return """💰 **Salary Negotiation Tips:**
• Research market rates using Glassdoor, PayScale, or Levels.fyi
• Consider total compensation, not just base salary
• Practice your negotiation conversation beforehand
• Focus on your value and achievements
• Be prepared to discuss benefits, PTO, and growth opportunities
• Know your walk-away point before negotiations begin
• Wait for the right moment (usually after receiving an offer)"""
    
    def _get_networking_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        return """🤝 **Networking Strategies:**
• Optimize your LinkedIn profile with a professional photo
• Engage with industry content and thought leaders
• Attend virtual and in-person industry events
• Join professional associations in your field
• Offer help and value before asking for favors
• Follow up with new connections within 24-48 hours
• Build genuine relationships, not just transactional ones"""
    
    def _get_job_search_advice(self, text: str, user_context: Dict[str, Any] = None) -> str:
        return """🔍 **Job Search Strategy:**
• Use multiple job boards (LinkedIn, Indeed, company websites)
• Set up job alerts for relevant positions
• Apply within 1-2 days of job posting when possible
• Customize your application for each role
• Track your applications in a spreadsheet
• Follow up on applications after 1-2 weeks
• Consider working with recruiters in your industry
• Leverage your network for referrals"""
    
    def _get_default_response(self, user_context: Dict[str, Any] = None) -> str:
        response = """👋 I'm your career advisor! I can help you with:

📄 **Resume & CV writing**
🎯 **Interview preparation** 
🚀 **Skill development**
🔄 **Career transitions**
💰 **Salary negotiations**
🤝 **Professional networking**
🔍 **Job search strategies**

What career topic would you like to explore today?"""

        if user_context and user_context.get('current_role'):
            role = user_context.get('current_role')
            response += f"\n\nI see you're working as a {role}. Feel free to ask me anything specific to your role!"
        
        return response