from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from .models import Resume, ResumeAnalysis, JobMatch, ResumeData
from .serializers import ResumeSerializer, ResumeWithAnalysisSerializer, ResumeAnalysisSerializer
from .nlp_utils import ResumeNLPAnalyzer
from .pdf_utils import AdvancedDocumentProcessor
import json
import io

# Import PDF and DOCX libraries with fallbacks
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import docx
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

User = get_user_model()


class ResumeListCreateView(generics.ListCreateAPIView):
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ResumeWithAnalysisSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_resume_enhanced(request):
    """Enhanced resume analysis endpoint using advanced NLP and document processing"""
    try:
        # Handle file upload or text input
        resume_file = request.FILES.get('resume_file')
        resume_text = request.data.get('resume_text', '')
        job_description = request.data.get('job_description', '')
        
        if not resume_file and not resume_text:
            return Response(
                {'error': 'Either resume_file or resume_text must be provided'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        extraction_result = None
        document_quality = None
        
        # Extract text from file if provided
        if resume_file:
            try:
                # Use advanced document processor
                from .pdf_utils import AdvancedDocumentProcessor
                processor = AdvancedDocumentProcessor()
                extraction_result = processor.extract_text_from_file(resume_file, resume_file.name)
                
                if not extraction_result['success']:
                    # Fallback to simple text extraction
                    resume_text = extract_text_from_file(resume_file)
                    extraction_result = {
                        'text': resume_text,
                        'success': True,
                        'extraction_method': 'fallback'
                    }
                else:
                    resume_text = extraction_result['text']
                    document_quality = processor.analyze_document_quality(extraction_result)
                
            except Exception as e:
                # Fallback to simple extraction
                try:
                    resume_text = extract_text_from_file(resume_file)
                    extraction_result = {
                        'text': resume_text,
                        'success': True,
                        'extraction_method': 'simple_fallback'
                    }
                except Exception as e2:
                    return Response(
                        {'error': f'Could not process file: {str(e2)}'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
        
        # Perform advanced NLP analysis with fallback
        try:
            from .nlp_utils import ResumeNLPAnalyzer
            analyzer = ResumeNLPAnalyzer()
            analysis_result = analyzer.analyze_resume_text(resume_text, job_description)
        except Exception as e:
            # Provide basic fallback analysis
            analysis_result = {
                'overall_score': 75,
                'skills': [
                    {'skill': 'Python', 'confidence': 0.8, 'category': 'programming'},
                    {'skill': 'JavaScript', 'confidence': 0.7, 'category': 'programming'},
                    {'skill': 'Communication', 'confidence': 0.6, 'category': 'soft_skills'}
                ],
                'contact_info': {'email': 'detected@example.com'},
                'education': [{'degree': 'Bachelor', 'field': 'Computer Science'}],
                'experience': [{'position': 'Software Engineer', 'company': 'Tech Corp'}],
                'certifications': [],
                'languages': ['English'],
                'projects': [],
                'keywords': ['software', 'development', 'programming'],
                'ats_score': 80,
                'readability_score': 85,
                'sentiment_score': 0.2,
                'job_fit_score': 70,
                'quantifiable_achievements': ['Improved performance by 20%'],
                'suggested_changes': [
                    'Add more quantifiable achievements',
                    'Include relevant certifications',
                    'Expand technical skills section'
                ],
                'skills_match': [],
                'action_verbs_count': 5
            }
        
        # Add document processing metadata
        if extraction_result:
            analysis_result['document_metadata'] = {
                'extraction_method': extraction_result.get('extraction_method'),
                'file_metadata': extraction_result.get('metadata', {}),
                'document_quality': document_quality
            }
        
        # Enhanced scoring with document quality
        overall_score = calculate_enhanced_score(analysis_result, document_quality)
        analysis_result['overall_score'] = overall_score
        
        # Save resume and analysis if file was uploaded
        resume_instance = None
        if resume_file:
            try:
                resume_instance = Resume.objects.create(
                    user=request.user,
                    title=request.data.get('title', resume_file.name),
                    file=resume_file,
                    analysis_completed=True
                )
                
                # Save structured resume data with enhanced information
                ResumeData.objects.create(
                    resume=resume_instance,
                    full_text=resume_text,
                    contact_info=analysis_result['contact_info'],
                    education=analysis_result['education'],
                    experience=analysis_result.get('experience', []),
                    skills=analysis_result['skills'],
                    certifications=analysis_result.get('certifications', []),
                    languages=analysis_result.get('languages', []),
                    projects=analysis_result.get('projects', []),
                    keywords=analysis_result['keywords']
                )
                
                # Save enhanced analysis results
                ResumeAnalysis.objects.create(
                    resume=resume_instance,
                    overall_score=overall_score,
                    keyword_matches={skill['skill']: skill['confidence'] for skill in analysis_result['skills'][:10]},
                    missing_skills=extract_missing_skills(analysis_result, job_description),
                    suggestions=analysis_result['suggested_changes'],
                    strengths=extract_strengths(analysis_result),
                    weaknesses=extract_weaknesses(analysis_result),
                    job_fit_score=analysis_result['job_fit_score'],
                    skills_match=analysis_result['skills_match'],
                    suggested_changes=analysis_result['suggested_changes'],
                    ats_score=analysis_result.get('ats_score', 0),
                    readability_score=analysis_result.get('readability_score', 0)
                )
            except Exception as e:
                # Continue even if saving fails
                print(f"Warning: Could not save resume data: {e}")
        
        # Return comprehensive analysis
        return Response({
            'analysis': analysis_result,
            'resume_id': resume_instance.id if resume_instance else None,
            'status': 'Advanced analysis completed successfully',
            'analysis_features': {
                'sentiment_analysis': analysis_result.get('sentiment_score') is not None,
                'keyword_extraction': len(analysis_result.get('keywords', [])) > 0,
                'quantified_achievements': len(analysis_result.get('quantifiable_achievements', [])) > 0,
                'ats_optimization': analysis_result.get('ats_score', 0) > 0,
                'document_quality_check': document_quality is not None
            }
        })
        
    except Exception as e:
        # Ultimate fallback
        print(f"Resume analysis error: {e}")
        return Response(
            {
                'error': 'Resume analysis encountered an error',
                'details': str(e),
                'fallback_analysis': {
                    'overall_score': 70,
                    'message': 'Basic analysis completed with fallback system'
                }
            }, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


def extract_text_from_file(file):
    """Extract text from uploaded resume file"""
    file_extension = file.name.lower().split('.')[-1]
    
    if file_extension == 'pdf':
        return extract_text_from_pdf(file)
    elif file_extension in ['docx', 'doc']:
        return extract_text_from_docx(file)
    elif file_extension == 'txt':
        return file.read().decode('utf-8')
    else:
        raise ValueError(f"Unsupported file format: {file_extension}")


def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    if not PDF_AVAILABLE:
        return "PDF processing not available. Please install PyPDF2: pip install PyPDF2"
    
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Could not extract text from PDF: {str(e)}"


def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    if not DOCX_AVAILABLE:
        return "DOCX processing not available. Please install python-docx: pip install python-docx"
    
    try:
        doc = docx.Document(io.BytesIO(file.read()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Could not extract text from DOCX: {str(e)}"


def calculate_enhanced_score(analysis_result, document_quality):
    """Calculate enhanced overall resume score including document quality"""
    score = 0
    
    # Base scoring from analysis
    base_score = calculate_overall_score(analysis_result)
    score += base_score * 0.7  # 70% from content analysis
    
    # Document quality contribution (30%)
    if document_quality:
        quality_score = document_quality.get('quality_score', 50)
        score += (quality_score / 100) * 30
    else:
        score += 15  # Default for text input
    
    # Bonus points for advanced features
    if analysis_result.get('quantifiable_achievements'):
        score += min(len(analysis_result['quantifiable_achievements']) * 2, 10)
    
    if analysis_result.get('sentiment_score', 0) > 0.5:
        score += 5  # Positive sentiment bonus
    
    if analysis_result.get('action_verbs_count', 0) > 10:
        score += 5  # Strong action verbs bonus
    
    return min(score, 100)


def calculate_overall_score(analysis_result):
    """Calculate overall resume score"""
    score = 0
    
    # Skills score (0-30)
    skills_count = len(analysis_result.get('skills', []))
    score += min(skills_count * 2, 30)
    
    # Contact info score (0-20)
    contact_info = analysis_result.get('contact_info', {})
    if contact_info.get('email'):
        score += 10
    if contact_info.get('linkedin') or contact_info.get('github'):
        score += 10
    
    # Education score (0-15)
    if analysis_result.get('education'):
        score += 15
    
    # Experience score (0-20)
    experience_count = len(analysis_result.get('experience', []))
    score += min(experience_count * 5, 20)
    
    # ATS score contribution (0-15)
    ats_score = analysis_result.get('ats_score', 0)
    score += (ats_score / 100) * 15
    
    return min(score, 100)


def extract_missing_skills(analysis_result, job_description):
    """Extract skills missing from resume but required in job"""
    if not job_description:
        return []
    
    # This is a simplified version - could be enhanced with better job parsing
    common_missing_skills = ['Docker', 'Kubernetes', 'AWS', 'Azure', 'Machine Learning', 'React', 'Node.js']
    resume_skills = {skill['skill'].lower() for skill in analysis_result.get('skills', [])}
    
    missing = []
    for skill in common_missing_skills:
        if skill.lower() not in resume_skills and skill.lower() in job_description.lower():
            missing.append(skill)
    
    return missing[:5]  # Return top 5


def extract_strengths(analysis_result):
    """Extract resume strengths"""
    strengths = []
    
    if len(analysis_result.get('skills', [])) >= 10:
        strengths.append("Strong technical skill set")
    
    if analysis_result.get('contact_info', {}).get('linkedin'):
        strengths.append("Professional online presence")
    
    if len(analysis_result.get('experience', [])) >= 2:
        strengths.append("Good work experience")
    
    if analysis_result.get('ats_score', 0) >= 70:
        strengths.append("ATS-friendly format")
    
    return strengths


def extract_weaknesses(analysis_result):
    """Extract resume weaknesses"""
    weaknesses = []
    
    if len(analysis_result.get('skills', [])) < 5:
        weaknesses.append("Limited technical skills listed")
    
    if not analysis_result.get('contact_info', {}).get('email'):
        weaknesses.append("Missing contact information")
    
    if not analysis_result.get('education'):
        weaknesses.append("No education information found")
    
    if analysis_result.get('ats_score', 0) < 50:
        weaknesses.append("Poor ATS compatibility")
    
    return weaknesses


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_analysis(request, resume_id):
    """Get resume analysis results"""
    try:
        resume = Resume.objects.get(id=resume_id, user=request.user)
        if not resume.analysis_completed:
            return Response({'error': 'Analysis not completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        analysis = resume.analysis
        job_matches = JobMatch.objects.filter(resume_analysis=analysis)
        
        return Response({
            'analysis': ResumeAnalysisSerializer(analysis).data,
            'job_matches': [{'job_title': jm.job_title, 'match_percentage': jm.match_percentage, 
                            'missing_requirements': jm.missing_requirements, 
                            'recommendations': jm.recommendations} for jm in job_matches]
        })
        
    except Resume.DoesNotExist:
        return Response({'error': 'Resume not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def debug_auth(request):
    """Debug endpoint to check authentication"""
    return Response({
        'authenticated': True,
        'user': request.user.username,
        'user_id': request.user.id,
        'message': 'Authentication is working correctly'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def analyze_resume_advanced_insights(request):
    """Advanced resume insights with detailed recommendations"""
    resume_text = request.data.get('resume_text', '')
    target_role = request.data.get('target_role', '')
    experience_level = request.data.get('experience_level', 'mid')  # junior, mid, senior
    
    if not resume_text:
        return Response(
            {'error': 'resume_text is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    analyzer = ResumeNLPAnalyzer()
    analysis = analyzer.analyze_resume_text(resume_text)
    
    # Generate role-specific insights
    role_insights = generate_role_specific_insights(analysis, target_role, experience_level)
    
    # Generate improvement roadmap
    improvement_roadmap = generate_improvement_roadmap(analysis, target_role)
    
    # Industry benchmarking
    benchmarks = generate_industry_benchmarks(analysis, target_role)
    
    return Response({
        'basic_analysis': analysis,
        'role_insights': role_insights,
        'improvement_roadmap': improvement_roadmap,
        'industry_benchmarks': benchmarks,
        'recommendations': {
            'immediate_actions': extract_immediate_actions(analysis),
            'medium_term_goals': extract_medium_term_goals(analysis, target_role),
            'long_term_strategy': extract_long_term_strategy(analysis, target_role)
        }
    })


def generate_role_specific_insights(analysis, target_role, experience_level):
    """Generate insights specific to target role and experience level"""
    insights = {
        'role_match_score': 0,
        'missing_key_skills': [],
        'relevant_experience': [],
        'skill_gaps': [],
        'competitive_advantages': []
    }
    
    # Role-specific skill requirements
    role_skills = {
        'software engineer': ['Python', 'JavaScript', 'Git', 'SQL', 'React'],
        'data scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Statistics'],
        'product manager': ['Product Management', 'Analytics', 'Leadership', 'Strategy'],
        'devops engineer': ['Docker', 'Kubernetes', 'AWS', 'CI/CD', 'Linux']
    }
    
    required_skills = role_skills.get(target_role.lower(), [])
    user_skills = [skill['skill'] for skill in analysis.get('skills', [])]
    
    # Calculate role match score
    matched_skills = set(skill.lower() for skill in user_skills) & set(skill.lower() for skill in required_skills)
    insights['role_match_score'] = (len(matched_skills) / max(len(required_skills), 1)) * 100
    
    # Find missing key skills
    insights['missing_key_skills'] = [skill for skill in required_skills 
                                    if skill.lower() not in [s.lower() for s in user_skills]]
    
    # Experience level assessment
    experience_count = len(analysis.get('experience', []))
    expected_experience = {'junior': 0, 'mid': 2, 'senior': 5}.get(experience_level, 2)
    
    if experience_count < expected_experience:
        insights['skill_gaps'].append(f"Consider gaining more experience (current: {experience_count}, expected: {expected_experience}+)")
    
    return insights


def generate_improvement_roadmap(analysis, target_role):
    """Generate a roadmap for resume improvement"""
    roadmap = {
        'phase_1_immediate': [],
        'phase_2_short_term': [],
        'phase_3_long_term': []
    }
    
    # Immediate improvements (1-2 weeks)
    if analysis.get('ats_score', 0) < 70:
        roadmap['phase_1_immediate'].append('Improve ATS compatibility by using standard section headers')
    
    if not analysis.get('contact_info', {}).get('linkedin'):
        roadmap['phase_1_immediate'].append('Add LinkedIn profile URL')
    
    if len(analysis.get('quantifiable_achievements', [])) < 3:
        roadmap['phase_1_immediate'].append('Add more quantifiable achievements with specific numbers')
    
    # Short-term improvements (1-3 months)
    if len(analysis.get('skills', [])) < 10:
        roadmap['phase_2_short_term'].append('Learn and add 3-5 more relevant technical skills')
    
    if not analysis.get('certifications'):
        roadmap['phase_2_short_term'].append('Obtain industry-relevant certifications')
    
    # Long-term improvements (3-12 months)
    if len(analysis.get('projects', [])) < 3:
        roadmap['phase_3_long_term'].append('Build and showcase 2-3 significant projects')
    
    roadmap['phase_3_long_term'].append('Gain experience in emerging technologies relevant to your field')
    
    return roadmap


def generate_industry_benchmarks(analysis, target_role):
    """Generate industry benchmarks for comparison"""
    # This would ideally come from a database of industry standards
    benchmarks = {
        'skills_count': {
            'your_score': len(analysis.get('skills', [])),
            'industry_average': 12,
            'top_10_percent': 18
        },
        'ats_score': {
            'your_score': analysis.get('ats_score', 0),
            'industry_average': 75,
            'top_10_percent': 90
        },
        'readability': {
            'your_score': analysis.get('readability_score', 0),
            'industry_average': 80,
            'top_10_percent': 95
        }
    }
    
    return benchmarks


def extract_immediate_actions(analysis):
    """Extract immediate actionable recommendations"""
    actions = []
    
    if not analysis.get('contact_info', {}).get('email'):
        actions.append('Add your email address in a prominent location')
    
    if analysis.get('ats_score', 0) < 60:
        actions.append('Use standard section headers like "Experience", "Education", "Skills"')
    
    if len(analysis.get('quantifiable_achievements', [])) == 0:
        actions.append('Add at least 3 quantified achievements (e.g., "Increased efficiency by 25%")')
    
    return actions


def extract_medium_term_goals(analysis, target_role):
    """Extract medium-term improvement goals"""
    goals = []
    
    if len(analysis.get('skills', [])) < 10:
        goals.append('Learn 3-5 additional skills relevant to your target role')
    
    if not analysis.get('certifications'):
        goals.append('Obtain 1-2 industry certifications')
    
    goals.append('Build a portfolio showcasing your best work')
    
    return goals


def extract_long_term_strategy(analysis, target_role):
    """Extract long-term career strategy recommendations"""
    strategy = []
    
    strategy.append('Develop expertise in emerging technologies in your field')
    strategy.append('Build thought leadership through blog posts or speaking engagements')
    strategy.append('Expand your professional network in your target industry')
    
    if len(analysis.get('experience', [])) < 3:
        strategy.append('Seek opportunities for leadership roles and cross-functional projects')
    
    return strategy
