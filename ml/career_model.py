import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from collections import defaultdict
import json

# Import ML libraries with fallbacks
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

class CareerRecommendationModel:
    """
    Advanced career recommendation system using machine learning
    for better career path suggestions.
    """
    
    def __init__(self):
        self.career_data = self._load_career_data()
        self.tfidf_vectorizer = TfidfVectorizer() if SKLEARN_AVAILABLE else None
        self.career_embeddings = {}
        self._build_embeddings()
    
    def _load_career_data(self):
        """Load predefined career and skill data"""
        return {
            'Software Engineer': {
                'skills': ['Python', 'JavaScript', 'SQL', 'Git', 'Problem Solving'],
                'importance': [0.9, 0.8, 0.7, 0.8, 0.9],
                'description': 'Design, develop and maintain software applications',
                'category': 'Technology',
                'salary_range': '70000-180000'
            },
            'Data Scientist': {
                'skills': ['Python', 'Machine Learning', 'Statistics', 'SQL', 'Data Visualization'],
                'importance': [0.9, 0.95, 0.9, 0.8, 0.8],
                'description': 'Analyze complex data to help companies make decisions',
                'category': 'Technology',
                'salary_range': '80000-200000'
            },
            'Frontend Developer': {
                'skills': ['JavaScript', 'React', 'HTML', 'CSS', 'TypeScript'],
                'importance': [0.9, 0.9, 0.8, 0.8, 0.8],
                'description': 'Build user-facing web applications',
                'category': 'Technology',
                'salary_range': '65000-150000'
            },
            'Product Manager': {
                'skills': ['Product Strategy', 'Data Analysis', 'Communication', 'Leadership'],
                'importance': [0.9, 0.8, 0.95, 0.9],
                'description': 'Guide product success and lead cross-functional teams',
                'category': 'Business',
                'salary_range': '90000-220000'
            }
        }
    
    def _build_embeddings(self):
        """Build career embeddings using TF-IDF"""
        if not SKLEARN_AVAILABLE:
            return
            
        career_documents = []
        for career, info in self.career_data.items():
            skills_text = ' '.join(info['skills'])
            description_text = info['description']
            combined_text = f"{skills_text} {description_text}"
            career_documents.append(combined_text)
        
        try:
            career_tfidf_matrix = self.tfidf_vectorizer.fit_transform(career_documents)
            career_names = list(self.career_data.keys())
            
            for i, career in enumerate(career_names):
                self.career_embeddings[career] = career_tfidf_matrix[i].toarray().flatten()
        except Exception as e:
            print(f"Error building embeddings: {e}")
    
    def recommend_careers(self, user_skills: Dict[str, float], 
                         user_interests: List[str] = None) -> List[Dict[str, Any]]:
        """Recommend careers based on user skills and interests"""
        recommendations = []
        
        for career_name, career_info in self.career_data.items():
            score = self._calculate_career_score(user_skills, career_info, user_interests)
            
            if score > 0:
                recommendation = {
                    'career': career_name,
                    'score': round(score, 2),
                    'description': career_info['description'],
                    'category': career_info['category'],
                    'salary_range': career_info['salary_range'],
                    'matching_skills': self._get_matching_skills(user_skills, career_info),
                    'missing_skills': self._get_missing_skills(user_skills, career_info),
                    'recommendations': self._generate_career_advice(user_skills, career_info)
                }
                recommendations.append(recommendation)
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:10]
    
    def _calculate_career_score(self, user_skills: Dict[str, float], 
                              career_info: Dict, user_interests: List[str]) -> float:
        """Calculate compatibility score for a career"""
        skill_score = self._calculate_skill_match_score(user_skills, career_info)
        
        # Interest bonus (up to 20% boost)
        interest_bonus = 0
        if user_interests:
            career_text = f"{career_info['description']} {' '.join(career_info['skills'])}"
            for interest in user_interests:
                if interest.lower() in career_text.lower():
                    interest_bonus += 5
        
        return min(skill_score + interest_bonus, 100.0)
    
    def _calculate_skill_match_score(self, user_skills: Dict[str, float], 
                                   career_info: Dict) -> float:
        """Calculate skill matching score"""
        required_skills = career_info['skills']
        importance_weights = career_info['importance']
        
        total_weighted_score = 0.0
        total_weight = 0.0
        
        for i, skill in enumerate(required_skills):
            weight = importance_weights[i]
            user_level = user_skills.get(skill, 0)
            
            # Score based on proficiency
            if user_level >= 80:
                skill_score = 100
            elif user_level >= 60:
                skill_score = 80
            elif user_level >= 40:
                skill_score = 60
            else:
                skill_score = max(0, user_level)
            
            total_weighted_score += skill_score * weight
            total_weight += weight
        
        return (total_weighted_score / total_weight) if total_weight > 0 else 0
    
    def _get_matching_skills(self, user_skills: Dict[str, float], career_info: Dict) -> List[Dict]:
        """Get matching skills between user and career"""
        matching_skills = []
        for skill in career_info['skills']:
            user_level = user_skills.get(skill, 0)
            if user_level > 0:
                matching_skills.append({
                    'skill': skill,
                    'user_level': user_level,
                    'proficiency': 'Expert' if user_level >= 80 else 'Intermediate' if user_level >= 40 else 'Beginner'
                })
        return matching_skills
    
    def _get_missing_skills(self, user_skills: Dict[str, float], career_info: Dict) -> List[Dict]:
        """Get missing skills for career"""
        missing_skills = []
        for i, skill in enumerate(career_info['skills']):
            user_level = user_skills.get(skill, 0)
            if user_level < 60:
                importance = career_info['importance'][i]
                missing_skills.append({
                    'skill': skill,
                    'importance': importance,
                    'current_level': user_level,
                    'priority': 'High' if importance > 0.8 else 'Medium'
                })
        return sorted(missing_skills, key=lambda x: x['importance'], reverse=True)
    
    def _generate_career_advice(self, user_skills: Dict[str, float], career_info: Dict) -> List[str]:
        """Generate career advice"""
        advice = []
        missing_skills = self._get_missing_skills(user_skills, career_info)
        
        if missing_skills:
            top_skill = missing_skills[0]['skill']
            advice.append(f"Focus on developing {top_skill} skills")
        
        if len(missing_skills) > 3:
            advice.append("Consider taking a structured course to build multiple skills")
        
        return advice[:2]
    
    def generate_learning_roadmap(self, user_skills: Dict[str, float], 
                                target_career: str) -> Dict[str, Any]:
        """Generate learning roadmap for target career"""
        if target_career not in self.career_data:
            return {'error': 'Career not found'}
        
        career_info = self.career_data[target_career]
        missing_skills = self._get_missing_skills(user_skills, career_info)
        
        roadmap = {
            'target_career': target_career,
            'phases': {
                'Foundation (0-3 months)': [],
                'Intermediate (3-6 months)': [],
                'Advanced (6-12 months)': []
            },
            'projects': [
                {'title': f'{target_career} Portfolio Project', 'difficulty': 'Intermediate'},
                {'title': f'Advanced {target_career} Application', 'difficulty': 'Advanced'}
            ]
        }
        
        # Distribute skills across phases
        for skill_info in missing_skills[:6]:
            skill = skill_info['skill']
            importance = skill_info['importance']
            
            if importance > 0.8:
                roadmap['phases']['Foundation (0-3 months)'].append({
                    'skill': skill,
                    'target_level': 60,
                    'estimated_hours': 40
                })
            elif importance > 0.6:
                roadmap['phases']['Intermediate (3-6 months)'].append({
                    'skill': skill,
                    'target_level': 75,
                    'estimated_hours': 30
                })
            else:
                roadmap['phases']['Advanced (6-12 months)'].append({
                    'skill': skill,
                    'target_level': 80,
                    'estimated_hours': 25
                })
        
        return roadmap


# Legacy function for backward compatibility
def score_career_paths(user_skill_levels: Dict[int, int],
                      career_to_required_skills: Dict[int, List[int]]) -> List[Tuple[int, float]]:
    """Legacy function for backward compatibility"""
    scores: List[Tuple[int, float]] = []
    for career_id, required_ids in career_to_required_skills.items():
        if not required_ids:
            scores.append((career_id, 0.0))
            continue
        total_possible = len(required_ids) * 100
        achieved = 0
        for sid in required_ids:
            achieved += max(0, min(100, user_skill_levels.get(sid, 0)))
        score = round((achieved / total_possible) * 100.0, 2)
        scores.append((career_id, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)