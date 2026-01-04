/**
 * Simple fetch wrapper for API requests
 * Note: GET endpoints are public, POST/PUT/DELETE require server-side authentication
 */
async function authFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        }
    };
    
    return fetch(url, { ...options, ...defaultOptions });
}

// Export for use in other scripts
window.authFetch = authFetch;
