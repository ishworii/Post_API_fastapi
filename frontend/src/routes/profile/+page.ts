import { isAuthenticated } from '$lib/stores/auth';
import { redirect } from '@sveltejs/kit';

export function load() {
    let authenticated;
    isAuthenticated.subscribe(value => {
        authenticated = value;
    })();

    if (!authenticated) {
        throw redirect(302, '/login');
    }
}