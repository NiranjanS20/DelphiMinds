// Authentication utility functions
function isAuthenticated() {
    const token = localStorage.getItem('access_token');
    if (!token) return false;
    
    try {
        // Check if token is expired
        const payload = JSON.parse(atob(token.split('.')[1]));
        const currentTime = Math.floor(Date.now() / 1000);
        
        if (payload.exp < currentTime) {
            // Token expired, try to refresh
            refreshToken();
            return false;
        }
        
        return true;
    } catch (error) {
        console.error('Token validation error:', error);
        return false;
    }
}

function getUserData() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
}

function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    window.location.href = '/login.html';
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    if (!refreshToken) {
        logout();
        return false;
    }
    
    try {
        const response = await fetch('/auth/refresh/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                refresh: refreshToken
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } else {
            logout();
            return false;
        }
    } catch (error) {
        console.error('Token refresh error:', error);
        logout();
        return false;
    }
}

// Protect page function - call this on pages that require authentication
function protectPage() {
    if (!isAuthenticated()) {
        alert('Please login to access this feature.');
        window.location.href = '/login.html';
        return false;
    }
    return true;
}

// Add authentication header to fetch requests
function getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return {
        'Content-Type': 'application/json',
        'Authorization': token ? `Bearer ${token}` : '',
    };
}

// Enhanced fetch with automatic token refresh
async function authenticatedFetch(url, options = {}) {
    const headers = getAuthHeaders();
    
    const response = await fetch(url, {
        ...options,
        headers: {
            ...headers,
            ...options.headers
        }
    });
    
    if (response.status === 401) {
        // Try to refresh token
        const refreshed = await refreshToken();
        if (refreshed) {
            // Retry the request with new token
            const newHeaders = getAuthHeaders();
            return fetch(url, {
                ...options,
                headers: {
                    ...newHeaders,
                    ...options.headers
                }
            });
        }
    }
    
    return response;
}