# DelphiMinds - AI-Powered Career & Skills Advisor

🚀 A comprehensive career guidance platform featuring user authentication, job market insights, AI chatbot, resume analysis, and personalized career roadmaps. Built with Django REST Framework backend and modern responsive frontend.

## ✨ Key Features

### 🔐 **Secure Authentication System**
- User registration and login with JWT tokens
- Automatic login after signup
- Role-based access (Student/Admin)
- Protected pages requiring authentication
- Token refresh and session management
- Comprehensive error handling for existing usernames/emails

### 📊 **Job Market Insights**
- Interactive charts showing job market trends
- Top in-demand skills visualization
- Salary insights across different roles
- Recent job postings with company details
- Real-time market data and growth statistics

### 🤖 **AI Career Chatbot**
- Interactive AI assistant for career guidance
- Quick action buttons for common queries
- Demo mode available for non-authenticated users
- Career advice, skill recommendations, and market insights
- Integration ready for multiple AI providers

### 📈 **Interactive Dashboard**
- Personal skills management system
- Career recommendations based on user profile
- Progress tracking and statistics
- User profile management
- Achievement badges and learning streaks

### 🏘️ **Community Features**
- Professional networking platform
- Discussion forums and career groups
- Knowledge sharing and mentorship
- Industry-specific communities

### 📄 **Resume Analysis & Tools**
- Resume upload and analysis
- ATS compatibility checking
- Skills extraction and recommendations
- Career roadmap generation
- Psychometric career assessments

### 🎯 **Gamification System**
- Achievement badges and rewards
- Learning streaks and progress tracking
- Leaderboards and challenges
- Skill-based progression system

## 🛠️ Tech Stack

### **Backend**
- **Framework**: Django 5.2.6 with Django REST Framework
- **Authentication**: JWT tokens with SimpleJWT
- **Database**: SQLite (development) / PostgreSQL (production)
- **API Architecture**: RESTful APIs with proper serialization

### **Frontend**
- **Styling**: Tailwind CSS for modern, responsive design
- **JavaScript**: Vanilla JS with modular architecture
- **Charts**: Chart.js for data visualization
- **Authentication**: JWT token management and automatic refresh

### **Key Libraries & Tools**
- **AI/ML**: spaCy, Hugging Face Transformers, scikit-learn
- **External APIs**: OpenAI, Hugging Face, Adzuna, Jooble
- **File Processing**: PDF and document analysis
- **Data Visualization**: Interactive charts and dashboards

## 🚀 Quick Start Guide

### 1. **Clone and Setup**

```bash
# Clone the repository
git clone <repository-url>
cd DelphiMinds3

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. **Database Setup**

```bash
# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# (Optional) Load demo data
python manage.py loaddata fixtures/demo_data.json
```

### 3. **Environment Configuration**

Create a `.env` file in the root directory:

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional - defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# API Keys (optional for enhanced features)
HUGGINGFACE_API_KEY=your_huggingface_api_key
OPENAI_API_KEY=your_openai_api_key
ADZUNA_API_ID=your_adzuna_api_id
ADZUNA_API_KEY=your_adzuna_api_key
```

### 4. **Start the Application**

```bash
# Start Django development server
python manage.py runserver

# Server will start at http://127.0.0.1:8000/
```

### 5. **Access the Platform**

🌐 **Main Pages:**
- **Homepage**: `http://127.0.0.1:8000/` - Landing page
- **Sign Up**: `http://127.0.0.1:8000/signup.html` - Create account
- **Login**: `http://127.0.0.1:8000/login.html` - User login
- **Dashboard**: `http://127.0.0.1:8000/dashboard.html` - Main user dashboard

📦 **Feature Pages** (Login Required):
- **Job Insights**: `http://127.0.0.1:8000/insights.html` - Market analysis
- **AI Chatbot**: `http://127.0.0.1:8000/chat.html` - Career assistant
- **Community**: `http://127.0.0.1:8000/community.html` - Professional network
- **Resume Tools**: `http://127.0.0.1:8000/resume.html` - Resume analysis
- **Career Roadmap**: `http://127.0.0.1:8000/roadmap.html` - Personalized paths
- **Career Test**: `http://127.0.0.1:8000/psychometric.html` - Assessments
- **Achievements**: `http://127.0.0.1:8000/gamification.html` - Progress tracking

## 📚 API Documentation

### **Authentication System**
```http
POST /auth/register/     # User registration with auto-login
POST /auth/login/        # JWT token authentication
POST /auth/refresh/      # Token refresh
```

**Registration Example:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "password": "securepassword123",
  "role": "student"
}
```

### **Core Features**
```http
# Skills Management
GET /skills/             # List all available skills
GET /skills/my/          # Get user's skills
POST /skills/my/         # Add skill to user profile

# Career Recommendations
GET /recommendations/    # Get personalized career suggestions

# Job Market Insights
GET /insights/           # Market trends and salary data

# AI Chatbot
POST /chatbot/           # Send message to career assistant

# Resume Analysis
POST /resume/analyze/    # Upload and analyze resume
GET /resume/             # List user resumes

# Community Features
GET /community/posts/    # Community discussions
POST /community/posts/   # Create new post
```

### **Response Format**
All API responses follow this structure:
```json
{
  "success": true,
  "data": { /* response data */ },
  "message": "Operation completed successfully"
}
```

## 📦 Project Structure

```
DelphiMinds3/
├── backend/                 # Django project settings
│   ├── settings.py          # Main configuration
│   ├── urls.py              # URL routing
│   └── views.py             # Core views
│
├── accounts/               # User management & authentication
│   ├── models.py            # User and UserProfile models
│   ├── views.py             # Registration & login views
│   ├── serializers.py       # User serialization
│   └── urls.py              # Auth endpoints
│
├── chatbot/                # AI career assistant
│   ├── views.py             # Chatbot API endpoints
│   ├── models.py            # Chat history models
│   └── ai_service.py        # AI integration logic
│
├── careers/                # Career recommendations
│   ├── models.py            # Career paths & recommendations
│   ├── views.py             # Career API endpoints
│   └── recommendation_engine.py  # ML recommendation logic
│
├── insights/               # Job market analytics
│   ├── views.py             # Market insights API
│   ├── models.py            # Market data models
│   └── data_sources.py      # External API integration
│
├── skills/                 # Skills management
│   ├── models.py            # Skills & user skills models
│   ├── views.py             # Skills API endpoints
│   └── serializers.py       # Skills serialization
│
├── resume/                 # Resume analysis tools
│   ├── views.py             # Resume upload & analysis
│   ├── models.py            # Resume storage models
│   └── analyzer.py          # NLP analysis engine
│
├── community/              # Professional networking
│   ├── models.py            # Posts, groups, connections
│   ├── views.py             # Community API endpoints
│   └── serializers.py       # Community serialization
│
├── gamification/           # Achievement system
│   ├── models.py            # Badges, achievements, progress
│   ├── views.py             # Gamification endpoints
│   └── achievement_engine.py # Progress tracking logic
│
├── frontend/               # Frontend assets
│   ├── *.html               # Page templates
│   ├── app.js               # Core JavaScript functions
│   ├── auth-utils.js        # Authentication utilities
│   └── career-advisor/      # Career advisor components
│
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
└── db.sqlite3              # SQLite database (development)
```

## 🔧 Development & Testing

### **Running Tests**

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts    # Authentication tests
python manage.py test chatbot     # Chatbot functionality
python manage.py test insights    # Market insights tests
python manage.py test skills      # Skills management tests

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### **Development Workflow**

1. **Feature Development**:
   - Create feature branch: `git checkout -b feature/feature-name`
   - Implement changes with proper testing
   - Update documentation as needed

2. **Code Quality**:
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Write unit tests for new functionality
   - Use meaningful commit messages

3. **Database Changes**:
   ```bash
   # Create migrations for model changes
   python manage.py makemigrations
   
   # Apply migrations
   python manage.py migrate
   
   # Create fixtures for test data
   python manage.py dumpdata app_name > fixtures/app_data.json
   ```

### **Common Development Tasks**

```bash
# Create new Django app
python manage.py startapp app_name

# Create superuser
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic

# Shell access with Django context
python manage.py shell

# Database shell
python manage.py dbshell
```

## ⚙️ Configuration & Setup

### **External API Configuration (Optional)**

For enhanced features, configure these APIs in your `.env` file:

#### **Hugging Face API** (AI Features)
```env
HUGGINGFACE_API_KEY=your_huggingface_token
```
1. Sign up at [huggingface.co](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create a new token

#### **OpenAI API** (Advanced AI Chat)
```env
OPENAI_API_KEY=your_openai_api_key
```
1. Register at [openai.com](https://openai.com/)
2. Create API key in dashboard

#### **Job Market APIs** (Live Data)
```env
# Adzuna Jobs API
ADZUNA_API_ID=your_adzuna_id
ADZUNA_API_KEY=your_adzuna_key

# Jooble API
JOOBLE_API_KEY=your_jooble_key
```

### **Database Options**

#### **SQLite (Default - No Setup Required)**
- Perfect for development and testing
- Database file: `db.sqlite3`
- No additional configuration needed

#### **PostgreSQL (Production Recommended)**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/delphiminds_db
```

1. Install PostgreSQL
2. Create database:
   ```sql
   CREATE DATABASE delphiminds_db;
   CREATE USER delphiminds_user WITH PASSWORD 'yourpassword';
   GRANT ALL PRIVILEGES ON DATABASE delphiminds_db TO delphiminds_user;
   ```

### **Enhanced Features Setup**

#### **NLP Models (Resume Analysis)**
```bash
# Install spaCy model for text processing
python -m spacy download en_core_web_sm

# Install additional NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

#### **File Upload Configuration**
```python
# In settings.py - configure file uploads
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
```

## 🚀 Production Deployment

### **Environment Configuration**

For production deployment, update your `.env` file:

```env
# Production settings
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_SECRET_KEY=your-super-secure-production-secret-key

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@localhost:5432/delphiminds_prod

# Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Static files (use CDN in production)
STATIC_URL=/static/
MEDIA_URL=/media/
```

### **Deployment Checklist**

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use strong `SECRET_KEY`
- [ ] Set up PostgreSQL database
- [ ] Configure HTTPS/SSL
- [ ] Set up static file serving
- [ ] Configure email backend
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Test all features in production environment

## 🔍 Troubleshooting

### **Common Issues & Solutions**

#### **Authentication Problems**
```
Error: Login failed / Token invalid
Solution: Check JWT token expiration, clear localStorage, re-login
```

#### **Database Errors**
```
Error: No such table / Migration errors
Solution: Run 'python manage.py migrate' to apply database changes
```

#### **Module Import Errors**
```
Error: ModuleNotFoundError
Solution: Activate virtual environment, install requirements
```

#### **Static Files Not Loading**
```
Error: 404 on static files
Solution: Run 'python manage.py collectstatic' and check STATIC_URL
```

## 📈 Performance & Scaling

- **Database**: Use connection pooling, add indexes, optimize queries
- **Caching**: Implement Redis/Memcached for frequently accessed data
- **Static Files**: Use CDN for better global performance
- **API Calls**: Implement request throttling and caching
- **Frontend**: Minify JavaScript/CSS, optimize images

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with proper testing
4. **Commit changes**: `git commit -m 'Add amazing feature'`
5. **Push to branch**: `git push origin feature/amazing-feature`
6. **Submit Pull Request** with detailed description

### **Code Style Guidelines**
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Write unit tests for new functionality
- Update documentation for API changes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

For support, questions, or contributions:

- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues) for bugs or feature requests
- **Documentation**: Check this README for setup and usage instructions
- **Email**: your-email@example.com for direct support

### **When Reporting Issues**
Please include:
- Error messages and stack traces
- Steps to reproduce the issue
- Your operating system and Python version
- Django version and other relevant dependencies

---

**Made with ❤️ for career guidance and professional development**

*DelphiMinds - Empowering careers through AI-powered insights and personalized guidance*