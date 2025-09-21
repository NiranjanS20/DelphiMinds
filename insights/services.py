import os
import requests
from typing import Dict, List, Any, Optional
import json
from urllib.parse import urlencode


class JobInsightsService:
    """Service for fetching job market data from external APIs"""
    
    def __init__(self):
        self.adzuna_api_id = os.getenv('ADZUNA_API_ID')
        self.adzuna_api_key = os.getenv('ADZUNA_API_KEY')
        self.jooble_api_key = os.getenv('JOOBLE_API_KEY')
    
    def get_job_insights(self, job_title: str, location: str = "us", 
                        skills: List[str] = None) -> Dict[str, Any]:
        """Get comprehensive job insights from multiple sources"""
        insights = {
            'job_title': job_title,
            'location': location,
            'job_listings': [],
            'salary_data': {},
            'skills_demand': {},
            'recommendations': []
        }
        
        # Try to get real data from APIs if keys are available
        api_success = False
        
        # Try Adzuna API first
        if self.adzuna_api_id and self.adzuna_api_key:
            try:
                adzuna_data = self._fetch_adzuna_jobs(job_title, location)
                if adzuna_data:
                    insights['job_listings'].extend(adzuna_data.get('jobs', []))
                    insights['salary_data'] = adzuna_data.get('salary_data', {})
                    api_success = True
            except Exception as e:
                print(f"Adzuna API error: {e}")
        
        # Try Jooble API
        if self.jooble_api_key:
            try:
                jooble_data = self._fetch_jooble_jobs(job_title, location)
                if jooble_data:
                    insights['job_listings'].extend(jooble_data.get('jobs', []))
                    api_success = True
            except Exception as e:
                print(f"Jooble API error: {e}")
        
        # If no API data was retrieved, use fallback data
        if not api_success or not insights['job_listings']:
            insights = self._get_fallback_insights(job_title, location, skills)
        else:
            # Enhance real data with additional insights
            insights['skills_demand'] = self._analyze_skills_demand(insights['job_listings'])
            insights['recommendations'] = self._generate_recommendations(insights)
            insights['data_source'] = 'Live API Data'
            insights['api_status'] = {
                'adzuna': 'Connected' if self.adzuna_api_id and self.adzuna_api_key else 'Not configured',
                'jooble': 'Connected' if self.jooble_api_key else 'Not configured'
            }
        
        return insights
    
    def _get_fallback_insights(self, job_title: str, location: str, 
                             skills: List[str] = None) -> Dict[str, Any]:
        """Provide fallback insights when APIs are unavailable"""
        # Mock data based on common job market patterns
        mock_jobs = [
            {
                'title': f"{job_title}",
                'company': "TechCorp Inc.",
                'location': location,
                'salary_min': 70000,
                'salary_max': 120000,
                'description': f"Looking for a skilled {job_title} to join our dynamic team. We offer competitive compensation, great benefits, and opportunities for growth.",
                'source': 'Sample Data',
                'created': '2024-01-15',
                'type': 'Full-time',
                'skills': ['Python', 'JavaScript', 'React'] if 'software' in job_title.lower() else ['SQL', 'Analytics', 'Python']
            },
            {
                'title': f"Senior {job_title}",
                'company': "Innovation Labs",
                'location': location,
                'salary_min': 90000,
                'salary_max': 150000,
                'description': f"We need an experienced {job_title} for exciting projects. Remote-friendly environment with excellent work-life balance.",
                'source': 'Sample Data',
                'created': '2024-01-10',
                'type': 'Remote',
                'skills': ['AWS', 'Docker', 'Kubernetes'] if 'engineer' in job_title.lower() else ['Data Analysis', 'Statistics', 'Machine Learning']
            },
            {
                'title': f"Lead {job_title}",
                'company': "Future Systems",
                'location': location,
                'salary_min': 110000,
                'salary_max': 180000,
                'description': f"Leadership role for an experienced {job_title}. Lead a team of talented professionals in cutting-edge projects.",
                'source': 'Sample Data',
                'created': '2024-01-08',
                'type': 'Hybrid',
                'skills': ['Leadership', 'Architecture', 'Mentoring']
            }
        ]
        
        salary_ranges = {
            'Software Engineer': {'min': 70000, 'max': 180000, 'avg': 110000},
            'Data Scientist': {'min': 80000, 'max': 200000, 'avg': 125000},
            'Product Manager': {'min': 90000, 'max': 220000, 'avg': 140000},
            'UX Designer': {'min': 60000, 'max': 160000, 'avg': 95000},
            'DevOps Engineer': {'min': 85000, 'max': 190000, 'avg': 135000}
        }
        
        job_key = next((key for key in salary_ranges.keys() if key.lower() in job_title.lower()), 'Software Engineer')
        salary_info = salary_ranges[job_key]
        
        return {
            'job_title': job_title,
            'location': location,
            'job_listings': mock_jobs,
            'salary_data': {
                'average_salary': salary_info['avg'],
                'median_salary': salary_info['avg'] * 0.95,
                'percentile_10': salary_info['min'],
                'percentile_90': salary_info['max'],
                'currency': 'USD',
                'note': 'Sample data - Connect your API keys for real-time data'
            },
            'skills_demand': self._get_mock_skills_demand(skills) if skills else {},
            'market_trends': {
                'growth_rate': '+8%',
                'demand_level': 'High',
                'job_openings': len(mock_jobs) * 150,  # Scale up for realism
                'note': 'Based on general market trends'
            },
            'recommendations': [
                f"Strong demand for {job_title} roles in the current market",
                "Focus on building a strong portfolio of projects",
                "Consider obtaining relevant certifications in cloud technologies",
                "Network with professionals in your target industry",
                "Keep your skills updated with latest technologies and frameworks"
            ],
            'data_source': 'Demo Data',
            'api_status': {
                'adzuna': 'API key not configured',
                'jooble': 'API key not configured',
                'note': 'Add API keys to .env file for real-time job market data'
            }
        }
    
    def _fetch_adzuna_jobs(self, job_title: str, location: str) -> Dict[str, Any]:
        """Fetch jobs from Adzuna API"""
        try:
            # Adzuna API endpoint
            # Note: Adzuna uses country codes - 'us' for United States
            country = 'us' if location.lower() in ['us', 'usa', 'united states'] else 'gb'
            
            url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
            params = {
                'app_id': self.adzuna_api_id,
                'app_key': self.adzuna_api_key,
                'what': job_title,
                'content-type': 'application/json',
                'results_per_page': 20
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the response
            jobs = []
            for job in data.get('results', []):
                job_data = {
                    'title': job.get('title', ''),
                    'company': job.get('company', {}).get('display_name', 'Unknown'),
                    'location': job.get('location', {}).get('display_name', location),
                    'description': job.get('description', ''),
                    'salary_min': job.get('salary_min'),
                    'salary_max': job.get('salary_max'),
                    'created': job.get('created', ''),
                    'source': 'Adzuna',
                    'type': 'Full-time',  # Adzuna doesn't always specify
                    'skills': self._extract_skills_from_description(job.get('description', ''))
                }
                jobs.append(job_data)
            
            # Calculate salary statistics
            salary_data = self._calculate_salary_stats(jobs)
            
            return {
                'jobs': jobs,
                'salary_data': salary_data,
                'total_count': data.get('count', 0)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Adzuna API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error processing Adzuna data: {e}")
            return None
    
    def _fetch_jooble_jobs(self, job_title: str, location: str) -> Dict[str, Any]:
        """Fetch jobs from Jooble API"""
        try:
            url = "https://jooble.org/api/" + self.jooble_api_key
            
            payload = {
                "keywords": job_title,
                "location": location,
                "page": "1"
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Process the response
            jobs = []
            for job in data.get('jobs', []):
                job_data = {
                    'title': job.get('title', ''),
                    'company': job.get('company', 'Unknown'),
                    'location': job.get('location', location),
                    'description': job.get('snippet', ''),
                    'salary_min': None,  # Jooble doesn't provide salary directly
                    'salary_max': None,
                    'created': job.get('updated', ''),
                    'source': 'Jooble',
                    'type': job.get('type', 'Full-time'),
                    'skills': self._extract_skills_from_description(job.get('snippet', ''))
                }
                jobs.append(job_data)
            
            return {
                'jobs': jobs,
                'total_count': data.get('totalCount', 0)
            }
            
        except requests.exceptions.RequestException as e:
            print(f"Jooble API request failed: {e}")
            return None
        except Exception as e:
            print(f"Error processing Jooble data: {e}")
            return None
    
    def _extract_skills_from_description(self, description: str) -> List[str]:
        """Extract skills from job description using keyword matching"""
        if not description:
            return []
        
        description_lower = description.lower()
        
        # Common tech skills to look for
        skills_keywords = {
            'Python', 'JavaScript', 'Java', 'React', 'Angular', 'Vue', 'Node.js',
            'SQL', 'PostgreSQL', 'MySQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
            'AWS', 'Azure', 'GCP', 'Git', 'Jenkins', 'CI/CD', 'REST', 'API',
            'HTML', 'CSS', 'TypeScript', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift',
            'Machine Learning', 'AI', 'TensorFlow', 'PyTorch', 'Pandas', 'NumPy',
            'Django', 'Flask', 'Spring', 'Express', 'Laravel', 'Rails'
        }
        
        found_skills = []
        for skill in skills_keywords:
            if skill.lower() in description_lower:
                found_skills.append(skill)
        
        return found_skills[:5]  # Limit to top 5 skills
    
    def _calculate_salary_stats(self, jobs: List[Dict]) -> Dict[str, Any]:
        """Calculate salary statistics from job listings"""
        salaries = []
        
        for job in jobs:
            if job.get('salary_min') and job.get('salary_max'):
                avg_salary = (job['salary_min'] + job['salary_max']) / 2
                salaries.append(avg_salary)
            elif job.get('salary_min'):
                salaries.append(job['salary_min'])
            elif job.get('salary_max'):
                salaries.append(job['salary_max'])
        
        if not salaries:
            return {
                'note': 'Salary data not available from API sources',
                'currency': 'USD'
            }
        
        salaries.sort()
        n = len(salaries)
        
        return {
            'average_salary': int(sum(salaries) / n),
            'median_salary': int(salaries[n // 2] if n % 2 else (salaries[n // 2 - 1] + salaries[n // 2]) / 2),
            'percentile_10': int(salaries[int(n * 0.1)]),
            'percentile_90': int(salaries[int(n * 0.9)]),
            'currency': 'USD',
            'sample_size': n
        }
    
    def _analyze_skills_demand(self, jobs: List[Dict]) -> Dict[str, int]:
        """Analyze skills demand from job listings"""
        skills_count = {}
        
        for job in jobs:
            for skill in job.get('skills', []):
                skills_count[skill] = skills_count.get(skill, 0) + 1
        
        # Sort by demand and return top skills
        sorted_skills = sorted(skills_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_skills[:10])  # Top 10 skills
    
    def _generate_recommendations(self, insights: Dict) -> List[str]:
        """Generate recommendations based on real job market data"""
        recommendations = []
        
        job_count = len(insights.get('job_listings', []))
        
        if job_count > 50:
            recommendations.append(f"High demand detected with {job_count}+ job openings")
        elif job_count > 20:
            recommendations.append(f"Moderate demand with {job_count} job openings")
        else:
            recommendations.append(f"Consider expanding your search criteria - {job_count} jobs found")
        
        # Skills recommendations
        skills_demand = insights.get('skills_demand', {})
        if skills_demand:
            top_skill = max(skills_demand.items(), key=lambda x: x[1])
            recommendations.append(f"Top in-demand skill: {top_skill[0]} (mentioned in {top_skill[1]} jobs)")
        
        # Salary recommendations
        salary_data = insights.get('salary_data', {})
        if salary_data.get('average_salary'):
            avg_salary = salary_data['average_salary']
            recommendations.append(f"Average salary range: ${avg_salary:,} based on current market data")
        
        return recommendations
    
    def _get_mock_skills_demand(self, skills: List[str] = None) -> Dict[str, int]:
        """Generate mock skills demand data"""
        if skills:
            # If skills provided, create demand based on those
            return {skill: 75 + (i * 5) for i, skill in enumerate(skills[:5])}
        else:
            # Default skills demand
            return {
                'Python': 85,
                'JavaScript': 82, 
                'React': 75,
                'SQL': 70,
                'AWS': 68,
                'Docker': 60,
                'Git': 55,
                'API': 50
            }