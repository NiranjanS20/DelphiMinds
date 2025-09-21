import re
import os
import json
import requests
from typing import List, Dict, Any, Tuple, Optional
from collections import Counter
import tempfile
from pathlib import Path

# Import packages with fallbacks for when they're not available
try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# Advanced text analysis libraries
try:
    import yake
    from keybert import KeyBERT
    import textstat
    from langdetect import detect
    from fuzzywuzzy import fuzz
    import pdfplumber
    import fitz  # PyMuPDF
    ADVANCED_LIBS_AVAILABLE = True
except ImportError:
    ADVANCED_LIBS_AVAILABLE = False


class ResumeNLPAnalyzer:
    """
    Advanced NLP utilities for resume analysis using spaCy, Hugging Face models,
    and traditional NLP techniques with fallbacks for missing dependencies.
    """
    
    def __init__(self):
        self.skills_database = self._load_skills_database()
        self.job_titles_database = self._load_job_titles_database()
        self.action_verbs = self._load_action_verbs()
        
        # Initialize NLP models if available
        self.nlp_model = None
        self.sentiment_analyzer = None
        self.ner_pipeline = None
        self.keyword_extractor = None
        self.yake_extractor = None
        
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize available NLP models"""
        # Initialize spaCy if available
        if SPACY_AVAILABLE:
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
            except OSError:
                try:
                    # Try to load a smaller model
                    self.nlp_model = spacy.load("en_core_web_md")
                except OSError:
                    print("spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
        
        # Initialize Hugging Face models if available
        if TRANSFORMERS_AVAILABLE:
            try:
                self.sentiment_analyzer = pipeline("sentiment-analysis", 
                                                 model="cardiffnlp/twitter-roberta-base-sentiment-latest")
                self.ner_pipeline = pipeline("ner", 
                                           model="dbmdz/bert-large-cased-finetuned-conll03-english")
            except Exception as e:
                print(f"Could not load Hugging Face models: {e}")
        
        # Initialize advanced text analysis tools
        if ADVANCED_LIBS_AVAILABLE:
            try:
                self.keyword_extractor = KeyBERT()
                self.yake_extractor = yake.KeywordExtractor(
                    lan="en",
                    n=3,
                    dedupLim=0.7,
                    top=20
                )
            except Exception as e:
                print(f"Could not load advanced analysis tools: {e}")
    
    def analyze_resume_text(self, text: str, job_description: str = "") -> Dict[str, Any]:
        """
        Comprehensive resume analysis returning structured data
        """
        analysis = {
            "skills_match": [],
            "job_fit_score": 0,
            "suggested_changes": [],
            "contact_info": {},
            "education": [],
            "experience": [],
            "skills": [],
            "certifications": [],
            "languages": [],
            "projects": [],
            "keywords": [],
            "ats_score": 0,
            "readability_score": 0,
            "sentiment_score": 0,
            "action_verbs_count": 0,
            "quantifiable_achievements": [],
            "improvement_suggestions": []
        }
        
        # Extract basic information
        analysis["contact_info"] = self._extract_contact_info(text)
        analysis["education"] = self._extract_education(text)
        analysis["experience"] = self._extract_experience(text)
        analysis["skills"] = self._extract_skills(text)
        analysis["certifications"] = self._extract_certifications(text)
        analysis["languages"] = self._extract_languages(text)
        analysis["projects"] = self._extract_projects(text)
        analysis["keywords"] = self._extract_keywords(text)
        
        # Advanced analysis
        analysis["quantifiable_achievements"] = self._find_quantifiable_achievements(text)
        analysis["action_verbs_count"] = self._count_action_verbs(text)
        analysis["ats_score"] = self._calculate_ats_score(text)
        analysis["readability_score"] = self._calculate_readability_score(text)
        analysis["sentiment_score"] = self._analyze_sentiment(text)
        
        # Job matching if job description provided
        if job_description:
            analysis["skills_match"], analysis["job_fit_score"] = self._match_job_requirements(text, job_description)
        
        # Generate suggestions
        analysis["suggested_changes"] = self._generate_suggestions(analysis, text)
        
        return analysis
    
    def _extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume text"""
        contact_info = {}
        
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        if emails:
            contact_info['email'] = emails[0]
        
        # Phone pattern
        phone_pattern = r'(\+?1?[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            contact_info['phone'] = ''.join(phones[0])
        
        # LinkedIn pattern
        linkedin_pattern = r'(linkedin\.com/in/[A-Za-z0-9-]+)'
        linkedin = re.findall(linkedin_pattern, text, re.IGNORECASE)
        if linkedin:
            contact_info['linkedin'] = f"https://{linkedin[0]}"
        
        # GitHub pattern
        github_pattern = r'(github\.com/[A-Za-z0-9-]+)'
        github = re.findall(github_pattern, text, re.IGNORECASE)
        if github:
            contact_info['github'] = f"https://{github[0]}"
        
        return contact_info
    
    def _extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information"""
        education = []
        
        # Common degree patterns
        degree_patterns = [
            r'(Bachelor|Master|PhD|Ph\.D|MBA|BS|BA|MS|MA)\s+(?:of\s+)?(?:Science\s+)?(?:Arts\s+)?(?:in\s+)?([^,\n.]+)',
            r'(B\.S\.|B\.A\.|M\.S\.|M\.A\.|Ph\.D\.)\s+(?:in\s+)?([^,\n.]+)',
        ]
        
        for pattern in degree_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                education.append({
                    'degree': match[0],
                    'field': match[1].strip()
                })
        
        return education
    
    def _extract_skills(self, text: str) -> List[Dict[str, float]]:
        """Extract and score skills from text"""
        skills_found = []
        text_lower = text.lower()
        
        for skill_category, skills_list in self.skills_database.items():
            for skill in skills_list:
                skill_lower = skill.lower()
                # Count occurrences and calculate confidence
                count = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', text_lower))
                if count > 0:
                    confidence = min(count / 3.0, 1.0)  # Max confidence at 3+ mentions
                    skills_found.append({
                        'skill': skill,
                        'category': skill_category,
                        'confidence': round(confidence, 2),
                        'mentions': count
                    })
        
        # Sort by confidence and return top skills
        return sorted(skills_found, key=lambda x: x['confidence'], reverse=True)[:20]
    
    def _match_job_requirements(self, resume_text: str, job_description: str) -> Tuple[List[Dict], float]:
        """Match resume skills with job requirements"""
        resume_skills = self._extract_skills(resume_text)
        job_skills = self._extract_skills(job_description)
        
        job_skill_names = {skill['skill'].lower() for skill in job_skills}
        matched_skills = []
        total_job_skills = len(job_skill_names)
        matched_count = 0
        
        for resume_skill in resume_skills:
            skill_name = resume_skill['skill'].lower()
            if skill_name in job_skill_names:
                matched_skills.append({
                    'skill': resume_skill['skill'],
                    'confidence': resume_skill['confidence'],
                    'match_type': 'exact'
                })
                matched_count += 1
        
        # Calculate job fit score
        job_fit_score = (matched_count / max(total_job_skills, 1)) * 100 if total_job_skills > 0 else 0
        
        return matched_skills, round(job_fit_score, 2)
    
    def _generate_suggestions(self, analysis: Dict[str, Any], text: str) -> List[str]:
        """Generate improvement suggestions based on analysis"""
        suggestions = []
        
        # Skills suggestions
        if len(analysis['skills']) < 10:
            suggestions.append("Add more relevant technical skills to increase your match with job requirements")
        
        # Contact information
        if not analysis['contact_info'].get('email'):
            suggestions.append("Ensure your email address is clearly visible")
        
        if not analysis['contact_info'].get('linkedin'):
            suggestions.append("Add your LinkedIn profile URL")
        
        # Education
        if not analysis['education']:
            suggestions.append("Include your educational background")
        
        return suggestions
    
    def _load_skills_database(self) -> Dict[str, List[str]]:
        """Load predefined skills database"""
        return {
            'programming': [
                'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
                'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'SQL', 'HTML', 'CSS', 'Sass', 'Less'
            ],
            'frameworks': [
                'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Express.js', 'Spring Boot',
                'Laravel', 'Ruby on Rails', 'ASP.NET', 'Node.js', 'Bootstrap', 'jQuery'
            ],
            'databases': [
                'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server',
                'Cassandra', 'DynamoDB', 'Elasticsearch'
            ],
            'cloud': [
                'AWS', 'Azure', 'Google Cloud', 'GCP', 'Docker', 'Kubernetes', 'Terraform',
                'Ansible', 'Jenkins', 'CI/CD', 'DevOps'
            ],
            'data_science': [
                'Machine Learning', 'Deep Learning', 'Data Analysis', 'Data Mining', 'Statistics',
                'Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Tableau', 'Power BI'
            ],
            'soft_skills': [
                'Leadership', 'Communication', 'Problem Solving', 'Teamwork', 'Project Management',
                'Agile', 'Scrum', 'Time Management', 'Critical Thinking', 'Adaptability'
            ]
        }
    
    def _extract_experience(self, text: str) -> List[Dict[str, str]]:
        """Extract work experience from resume text"""
        experience = []
        
        # Look for job titles and companies
        job_patterns = [
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+at\s+([A-Z][a-zA-Z\s&.]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+-\s+([A-Z][a-zA-Z\s&.]+)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)\s+\|\s+([A-Z][a-zA-Z\s&.]+)',
        ]
        
        for pattern in job_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                experience.append({
                    'position': match[0],
                    'company': match[1].strip()
                })
        
        return experience[:5]  # Return top 5 experiences
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications from resume text"""
        certifications = []
        text_lower = text.lower()
        
        # Common certifications
        cert_keywords = [
            'AWS Certified', 'Azure Certified', 'Google Cloud', 'PMP', 'Scrum Master',
            'CISSP', 'CompTIA', 'Cisco', 'Microsoft Certified', 'Oracle Certified',
            'Kubernetes', 'Docker Certified', 'Salesforce', 'Tableau', 'Power BI'
        ]
        
        for cert in cert_keywords:
            if cert.lower() in text_lower:
                certifications.append(cert)
        
        return certifications
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract programming/spoken languages from resume text"""
        languages = []
        text_lower = text.lower()
        
        # Programming languages
        prog_languages = [
            'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
            'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'SQL'
        ]
        
        # Spoken languages
        spoken_languages = [
            'English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese',
            'Korean', 'Italian', 'Portuguese', 'Russian', 'Arabic', 'Hindi'
        ]
        
        all_languages = prog_languages + spoken_languages
        
        for lang in all_languages:
            if lang.lower() in text_lower:
                languages.append(lang)
        
        return languages
    
    def _extract_projects(self, text: str) -> List[Dict[str, str]]:
        """Extract project information from resume text"""
        projects = []
        
        # Look for project sections and descriptions
        project_patterns = [
            r'Project:\s*([^\n]+)',
            r'([A-Z][a-zA-Z\s]+)\s+Project',
            r'Built\s+([^.]+)',
            r'Developed\s+([^.]+)',
            r'Created\s+([^.]+)'
        ]
        
        for pattern in project_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                projects.append({
                    'name': match.strip(),
                    'description': match.strip()
                })
        
        return projects[:3]  # Return top 3 projects
    
    def _find_quantifiable_achievements(self, text: str) -> List[str]:
        """Find quantifiable achievements in resume text"""
        achievements = []
        
        # Patterns for numbers and percentages
        patterns = [
            r'(increased?|improved?|reduced?|saved?|generated?)\s+[^\d]*([\d,]+\%?)',
            r'([\d,]+\%?)\s+(increase|improvement|reduction|growth)',
            r'(\$[\d,]+)\s+(saved?|generated?|revenue)',
            r'([\d,]+)\s+(users?|customers?|clients?|projects?)',
            r'(managed?|led)\s+([\d,]+)\s+(people|team|members)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                achievement = ' '.join(match).strip()
                if achievement:
                    achievements.append(achievement)
        
        return achievements[:5]  # Return top 5 achievements
    
    def _count_action_verbs(self, text: str) -> int:
        """Count action verbs in resume text"""
        text_lower = text.lower()
        count = 0
        
        for verb in self.action_verbs:
            count += len(re.findall(r'\b' + verb.lower() + r'\b', text_lower))
        
        return count
    
    def _calculate_ats_score(self, text: str) -> int:
        """Calculate ATS (Applicant Tracking System) friendliness score"""
        score = 0
        
        # Check for standard sections
        sections = ['experience', 'education', 'skills', 'contact']
        for section in sections:
            if section.lower() in text.lower():
                score += 20
        
        # Check for bullet points or structured format
        if '•' in text or '*' in text or '-' in text:
            score += 10
        
        # Check for phone and email
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 5
        if re.search(r'(\+?1?[-. ]?)?\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})', text):
            score += 5
        
        return min(score, 100)
    
    def _calculate_readability_score(self, text: str) -> int:
        """Calculate readability score using textstat library"""
        if ADVANCED_LIBS_AVAILABLE:
            try:
                # Flesch Reading Ease Score
                flesch_score = textstat.flesch_reading_ease(text)
                # Convert to 0-100 scale where higher is better
                return max(0, min(100, int(flesch_score)))
            except:
                pass
        
        # Fallback: simple readability based on sentence and word length
        sentences = text.split('.')
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 50
        
        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple scoring: penalize very long sentences and words
        score = 100
        if avg_sentence_length > 20:
            score -= 20
        if avg_word_length > 6:
            score -= 15
        
        return max(0, score)
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment of resume text"""
        if self.sentiment_analyzer:
            try:
                result = self.sentiment_analyzer(text[:512])  # Limit text length
                if result[0]['label'] == 'POSITIVE':
                    return result[0]['score']
                else:
                    return -result[0]['score']
            except:
                pass
        
        # Fallback using TextBlob if available
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                return blob.sentiment.polarity
            except:
                pass
        
        return 0.0  # Neutral sentiment as fallback
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords using advanced NLP techniques"""
        keywords = []
        
        # Use KeyBERT if available
        if self.keyword_extractor and ADVANCED_LIBS_AVAILABLE:
            try:
                keybert_keywords = self.keyword_extractor.extract_keywords(
                    text, 
                    keyphrase_ngram_range=(1, 3), 
                    stop_words='english',
                    top_k=15
                )
                keywords.extend([kw[0] for kw in keybert_keywords])
            except Exception as e:
                print(f"KeyBERT extraction failed: {e}")
        
        # Use YAKE if available
        if self.yake_extractor and ADVANCED_LIBS_AVAILABLE:
            try:
                yake_keywords = self.yake_extractor.extract_keywords(text)
                keywords.extend([kw[1] for kw in yake_keywords[:10]])
            except Exception as e:
                print(f"YAKE extraction failed: {e}")
        
        # Use spaCy if available
        if self.nlp_model:
            try:
                doc = self.nlp_model(text)
                # Extract named entities
                entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'PRODUCT', 'TECH']]
                keywords.extend(entities)
                
                # Extract noun phrases
                noun_phrases = [chunk.text for chunk in doc.noun_chunks if len(chunk.text.split()) <= 3]
                keywords.extend(noun_phrases[:10])
            except Exception as e:
                print(f"spaCy extraction failed: {e}")
        
        # Fallback: simple keyword extraction
        if not keywords:
            keywords = self._simple_keyword_extraction(text)
        
        # Remove duplicates and return top keywords
        unique_keywords = list(dict.fromkeys(keywords))  # Preserve order
        return unique_keywords[:20]
    
    def _simple_keyword_extraction(self, text: str) -> List[str]:
        """Simple keyword extraction fallback"""
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does',
            'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall'
        }
        
        # Extract words that appear frequently and are not stop words
        words = re.findall(r'\b[A-Za-z]{3,}\b', text.lower())
        word_freq = Counter(words)
        
        keywords = []
        for word, freq in word_freq.most_common(30):
            if word not in stop_words and freq > 1:
                keywords.append(word.title())
        
        return keywords[:15]
    
    def _load_job_titles_database(self) -> List[str]:
        """Load common job titles"""
        return [
            'Software Engineer', 'Software Developer', 'Full Stack Developer', 'Frontend Developer',
            'Backend Developer', 'Data Scientist', 'Data Analyst', 'Machine Learning Engineer',
            'DevOps Engineer', 'Product Manager', 'Project Manager', 'UX Designer', 'UI Designer',
            'QA Engineer', 'Test Engineer', 'System Administrator', 'Database Administrator'
        ]
    
    def _load_action_verbs(self) -> List[str]:
        """Load action verbs for resume analysis"""
        return [
            'achieved', 'adapted', 'administered', 'analyzed', 'built', 'collaborated', 'communicated',
            'created', 'delivered', 'demonstrated', 'designed', 'developed', 'enhanced', 'established',
            'executed', 'expanded', 'generated', 'implemented', 'improved', 'increased', 'initiated',
            'launched', 'led', 'managed', 'optimized', 'organized', 'produced', 'reduced', 'resolved',
            'streamlined', 'supervised', 'supported', 'trained', 'transformed', 'upgraded'
        ]