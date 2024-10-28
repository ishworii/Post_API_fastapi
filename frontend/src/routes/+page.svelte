<script lang="ts">
	import { goto } from '$app/navigation';
	import { logout } from '$lib/stores/auth';

	export let data;
	const { posts } = data;

	function handleLogout() {
		logout();
		goto('/');
	}
</script>

<h1>Latest Posts</h1>

{#if posts.length === 0}
	<p>No posts available.</p>
{:else}
	<div class="posts-grid">
		{#each posts as post}
			<div class="post-card">
				<a href="/posts/{post.id}" class="title">{post.title}</a>
				<div class="content">{post.content.slice(0, 100)}...</div>
				<div class="meta">
					By {post.author?.username} | Likes: {post.like_count} | Comments: {post.comment_count}
				</div>
			</div>
		{/each}
	</div>
{/if}

<style>
	.posts-grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1rem;
	}
	.post-card {
		border: 1px solid #ddd;
		padding: 1rem;
		border-radius: 8px;
		transition: box-shadow 0.3s ease;
	}
	.post-card:hover {
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
	}
	.title {
		font-weight: bold;
		font-size: 1.2rem;
		color: #0066cc;
		text-decoration: none;
	}
	.content {
		color: #333;
		margin: 0.5rem 0;
	}
	.meta {
		font-size: 0.8rem;
		color: #666;
	}
	nav {
		display: flex;
		justify-content: flex-end;
		padding: 1rem;
	}
	.nav-button {
		margin-left: 1rem;
		padding: 0.5rem 1rem;
		background-color: #0066cc;
		color: white;
		text-decoration: none;
		border-radius: 4px;
	}
</style>
