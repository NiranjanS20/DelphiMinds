// Career Advisor Homepage JavaScript

// Initialize particles
function createParticles() {
    const container = document.getElementById('particle-container');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 4 + 1;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100 + 100}%`;
        particle.style.animationDuration = `${Math.random() * 20 + 10}s`;
        particle.style.animationDelay = `${Math.random() * 20}s`;
        particle.style.opacity = `${Math.random() * 0.5 + 0.1}`;
        
        container.appendChild(particle);
    }
}

// Feature tiles data - Only existing working pages
const tiles = [
    { id: 'dashboard', title: 'Dashboard', description: 'View your skills, progress and career stats', icon: '📊', eta: '5 mins', badge: 'Start Here', difficulty: 'Beginner', url: '/dashboard.html' },
    { id: 'chatbot', title: 'AI Chatbot', description: 'Get personalized career advice and guidance', icon: '🤖', eta: '10 mins', difficulty: 'Beginner', url: '/chat.html' },
    { id: 'career-roadmap', title: 'Career Roadmap', description: 'Get personalized career paths and milestones', icon: '🛤️', eta: '15 mins', difficulty: 'Intermediate', url: '/roadmap.html' },
    { id: 'resume', title: 'Resume Analyzer', description: 'AI-powered resume analysis and optimization', icon: '📄', eta: '30 mins', badge: 'Popular', difficulty: 'Advanced', url: '/resume.html' },
    { id: 'insights', title: 'Job Insights', description: 'Latest job market trends and opportunities', icon: '📈', eta: '5 mins', difficulty: 'Beginner', url: '/insights.html' },
    { id: 'gamification', title: 'Achievements', description: 'Track your progress and earn badges', icon: '🏆', eta: '2 mins', difficulty: 'Beginner', url: '/gamification.html' },
];

// Create feature tiles
function createFeatureTiles() {
    const container = document.getElementById('feature-tiles');
    
    tiles.forEach((tile, index) => {
        const tileElement = document.createElement('div');
        tileElement.className = `group relative cursor-pointer bg-slate-900/60 backdrop-blur-xl rounded-2xl border border-white/10 hover:border-white/20 shadow-lg hover:shadow-2xl hover:shadow-cyan-500/20 transition-all duration-300 ease-out hover:-translate-y-2 hover:scale-105`;
        tileElement.onclick = () => handleTileClick(tile);
        
        const difficultyColors = {
            'Beginner': 'text-green-400 bg-green-400/10 border-green-400/20',
            'Intermediate': 'text-yellow-400 bg-yellow-400/10 border-yellow-400/20',
            'Advanced': 'text-red-400 bg-red-400/10 border-red-400/20'
        };
        
        tileElement.innerHTML = `
            ${tile.badge ? `
                <div class="absolute -top-2 -right-2 z-10">
                    <div class="bg-gradient-to-r from-cyan-400 to-blue-500 text-white text-xs font-semibold px-3 py-1 rounded-full shadow-lg">
                        ${tile.badge}
                    </div>
                </div>
            ` : ''}
            
            <div class="relative p-6 h-full flex flex-col">
                <div class="text-4xl mb-4 group-hover:scale-110 group-hover:rotate-3 transition-transform duration-200">
                    ${tile.icon}
                </div>
                
                <h3 class="text-xl font-bold mb-2 text-white group-hover:text-cyan-400 transition-colors duration-200">
                    ${tile.title}
                </h3>
                
                <p class="text-gray-400 text-sm mb-4 flex-grow leading-relaxed">
                    ${tile.description}
                </p>
                
                <div class="flex items-center justify-between text-xs">
                    <div class="flex items-center space-x-2">
                        <span class="text-gray-500">⏱️ ${tile.eta}</span>
                    </div>
                    <div class="px-2 py-1 rounded-full border text-xs font-medium ${difficultyColors[tile.difficulty]}">
                        ${tile.difficulty}
                    </div>
                </div>
                
                <div class="mt-4 pt-4 border-t border-white/10 opacity-0 group-hover:opacity-100 transform translate-y-2 group-hover:translate-y-0 transition-all duration-200">
                    <div class="flex items-center text-cyan-400 text-sm font-medium">
                        Get Started
                        <svg class="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                        </svg>
                    </div>
                </div>
            </div>
        `;
        
        // Add animation delay
        tileElement.style.animationDelay = `${index * 0.1}s`;
        container.appendChild(tileElement);
    });
}

// Handle tile clicks - Connect to actual pages
function handleTileClick(tile) {
    // Navigate directly to the working page
    if (tile.url) {
        window.location.href = tile.url;
    } else {
        console.error(`No URL defined for ${tile.title}`);
    }
}

// Chat functionality
let isAnimating = false;

function toggleChat() {
    if (isAnimating) return;
    isAnimating = true;
    
    const drawer = document.getElementById('chat-drawer');
    const isOpen = !drawer.classList.contains('hidden');
    
    if (isOpen) {
        drawer.classList.add('hidden');
    } else {
        drawer.classList.remove('hidden');
        document.getElementById('chat-input').focus();
    }
    
    setTimeout(() => {
        isAnimating = false;
    }, 300);
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Try to use the actual chatbot API
    fetch('/chatbot/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') || ''
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('API Error');
    })
    .then(data => {
        addChatMessage(data.response || data.message, 'ai');
    })
    .catch(error => {
        console.error('Chat error:', error);
        getOfflineResponse(message);
    });
}

// Offline/demo chat responses
function getOfflineResponse(message) {
    const response = getCareerResponse(message.toLowerCase());
    
    setTimeout(() => {
        addChatMessage(response, 'ai');
    }, 1000);
}

// Enhanced career-focused responses
function getCareerResponse(message) {
    const careerResponses = {
        skills: "I'd recommend focusing on in-demand skills like Python, JavaScript, data analysis, or cloud computing. Visit our Skills Manager to track your progress!",
        career: "Great question! Our Career Roadmap feature can help you explore different paths. Would you like to check out personalized recommendations?",
        resume: "For resume improvement, try our AI Resume Analyzer - it provides detailed feedback and optimization suggestions!",
        interview: "Interview preparation is crucial! While we're developing our Interview Lab, I recommend practicing common questions and researching the company.",
        salary: "Salary insights vary by location and experience. Check our Market Insights section for current industry trends!",
        learning: "Continuous learning is key! Our platform offers personalized learning recommendations based on your career goals.",
        test: "Take our Career Assessment tests to discover your strengths and ideal career paths!",
        community: "Connect with like-minded professionals in our Community section - it's great for networking and advice!"
    };
    
    for (const [key, response] of Object.entries(careerResponses)) {
        if (message.includes(key)) {
            return response;
        }
    }
    
    return "That's an interesting question! I'm here to help with career guidance, skills development, resume tips, and job market insights. What specific area would you like to explore?";
}

// Helper function for CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addChatMessage(message, sender) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageElement = document.createElement('div');
    messageElement.className = `flex ${sender === 'user' ? 'justify-end' : 'justify-start'}`;
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageElement.innerHTML = `
        <div class="max-w-[80%] rounded-2xl px-4 py-3 text-sm ${
            sender === 'user' 
                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white' 
                : 'glass-light border border-white/20 text-gray-200'
        }">
            <p class="mb-1">${message}</p>
            <p class="text-xs opacity-70 ${sender === 'user' ? 'text-white/70' : 'text-gray-400'}">
                ${time}
            </p>
        </div>
    `;
    
    messagesContainer.appendChild(messageElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        sendMessage();
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl+K to open chat
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        toggleChat();
    }
    
    // Escape to close chat
    if (event.key === 'Escape') {
        const drawer = document.getElementById('chat-drawer');
        if (!drawer.classList.contains('hidden')) {
            toggleChat();
        }
    }
});

// Scroll effects
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    const scrolled = window.scrollY > 20;
    
    if (scrolled) {
        header.classList.add('glass-dark', 'backdrop-blur-md', 'border-b', 'border-white/10');
    } else {
        header.classList.remove('glass-dark', 'backdrop-blur-md', 'border-b', 'border-white/10');
    }
});

// Initialize dashboard features animation
function initDashboardFeatures() {
    const features = [
        { title: 'Career Roadmap', description: 'Personalized paths', color: 'from-blue-500 to-cyan-400' },
        { title: 'Skill Assessment', description: 'AI evaluations', color: 'from-cyan-500 to-blue-400' },
        { title: 'Interview Prep', description: 'Mock interviews', color: 'from-indigo-500 to-blue-400' },
        { title: 'Market Insights', description: 'Industry trends', color: 'from-cyan-400 to-teal-500' },
    ];
    
    let currentFeature = 0;
    
    function updateFeatures() {
        const container = document.getElementById('dashboard-features');
        if (!container) return;
        
        container.innerHTML = '';
        
        features.forEach((feature, index) => {
            const featureElement = document.createElement('div');
            featureElement.className = `relative group transition-all duration-500 ${
                index === currentFeature ? 'scale-105 opacity-100' : 'opacity-60'
            }`;
            
            featureElement.innerHTML = `
                <div class="bg-white/5 backdrop-blur-sm rounded-xl p-4 border border-white/10 hover:border-white/20">
                    <div class="w-12 h-12 rounded-lg bg-gradient-to-br ${feature.color} mb-3 flex items-center justify-center">
                        <div class="w-6 h-6 bg-white/90 rounded"></div>
                    </div>
                    <h3 class="text-white font-semibold text-sm mb-1">${feature.title}</h3>
                    <p class="text-gray-400 text-xs">${feature.description}</p>
                </div>
            `;
            
            container.appendChild(featureElement);
        });
        
        currentFeature = (currentFeature + 1) % features.length;
    }
    
    updateFeatures();
    setInterval(updateFeatures, 3000);
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function() {
    createParticles();
    createFeatureTiles();
    initDashboardFeatures();
    
    // Add fade-in animation to sections
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
        
        setTimeout(() => {
            section.style.opacity = '1';
            section.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    console.log('🚀 Career Advisor Homepage loaded successfully!');
    console.log('💡 Press Ctrl+K to open AI chat');
    console.log('🎯 Click on any feature tile to explore');
});