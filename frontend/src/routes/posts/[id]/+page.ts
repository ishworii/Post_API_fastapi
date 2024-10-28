import { error } from '@sveltejs/kit';

export async function load({ params, fetch }) {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/posts/${params.id}`);
    
    if (!res.ok) {
        throw error(res.status, 'Failed to fetch post');
    }

    const post = await res.json();

    return {
        post
    };
}