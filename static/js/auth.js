// API Authentication Helper
const API_TOKEN = 'PeHnk_zstaGVHLFLWERm32Lj19ueAc4q1IE_vX59N08';

/**
 * Authenticated fetch wrapper
 * Automatically includes Authorization header for all API requests
 */
async function authFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Authorization': `Bearer ${API_TOKEN}`,
            'Content-Type': 'application/json',
            ...options.headers
        }
    };
    
    return fetch(url, { ...options, ...defaultOptions });
}

// Export for use in other scripts
window.authFetch = authFetch;
