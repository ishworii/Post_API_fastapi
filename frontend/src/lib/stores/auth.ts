// src/lib/stores/auth.ts
import { browser } from '$app/environment';
import { writable } from 'svelte/store';

const storedToken = browser ? localStorage.getItem('token') : null;

export const token = writable(storedToken);
export const isAuthenticated = writable(!!storedToken);

export function login(accessToken: string) {
    token.set(accessToken);
    isAuthenticated.set(true);
    if (browser) {
        localStorage.setItem('token', accessToken);
    }
}

export function logout() {
    token.set(null);
    isAuthenticated.set(false);
    if (browser) {
        localStorage.removeItem('token');
    }
}