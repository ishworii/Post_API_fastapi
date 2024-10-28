import { token } from './stores/auth';

export async function authenticatedFetch(url: string, options: RequestInit = {}) {
    let authToken: string;
    token.subscribe(value => {
        authToken = value;
    })();

    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${authToken}`
    };

    return fetch(url, { ...options, headers });
}