// src/routes/+page.ts
import { error } from '@sveltejs/kit';

export async function load({ fetch }) {
    const url = `${import.meta.env.VITE_API_URL}/posts`;
    const res = await fetch(url);
    
    if (!res.ok) {
        throw error(res.status, 'Failed to fetch posts');
    }

    const posts = await res.json();
    return { posts };
}