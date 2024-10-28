<script lang="ts">
	import { authenticatedFetch } from '$lib/api';
	import { isAuthenticated } from '$lib/stores/auth';
	import { onMount } from 'svelte';

	export let data;
	let post = data.post;
	let commentContent = '';
	let comments = [];
	let error = '';

	onMount(async () => {
		await fetchComments();
	});

	async function fetchComments() {
		try {
			const response = await fetch(`${import.meta.env.VITE_API_URL}/posts/${post.id}/comments`);
			if (response.ok) {
				comments = await response.json();
			} else {
				error = 'Failed to fetch comments';
			}
		} catch (err) {
			console.error('Error fetching comments:', err);
			error = 'An error occurred while fetching comments';
		}
	}

	async function handleComment() {
		if (!commentContent.trim()) return;

		try {
			const response = await authenticatedFetch(
				`${import.meta.env.VITE_API_URL}/posts/${post.id}/comments`,
				{
					method: 'POST',
					headers: { 'Content-Type': 'application/json' },
					body: JSON.stringify({ content: commentContent })
				}
			);

			if (response.ok) {
				const newComment = await response.json();
				comments = [...comments, newComment];
				commentContent = '';
				error = '';
			} else {
				error = 'Failed to post comment';
			}
		} catch (err) {
			console.error('Error posting comment:', err);
			error = 'An error occurred while posting the comment';
		}
	}

	async function handleLike(isLike = true) {
		try {
			const response = await authenticatedFetch(
				`${import.meta.env.VITE_API_URL}/posts/${post.id}/${isLike ? 'like' : 'dislike'}`,
				{
					method: 'POST'
				}
			);

			if (response.ok) {
				const updatedPost = await response.json();
				// Update the post object with the new like/dislike counts
				post = {
					...post,
					like_count: updatedPost.like_count,
					dislike_count: updatedPost.dislike_count
				};
				error = '';
			} else {
				error = `Failed to ${isLike ? 'like' : 'dislike'} post`;
			}
		} catch (err) {
			console.error(`Error ${isLike ? 'liking' : 'disliking'} post:`, err);
			error = `An error occurred while ${isLike ? 'liking' : 'disliking'} the post`;
		}
	}
</script>

<div class="post-details">
	<h1>{post.title}</h1>
	<p class="meta">By {post.author?.username} on {new Date(post.created_at).toLocaleDateString()}</p>
	<div class="content">{post.content}</div>

	{#if $isAuthenticated}
		<div class="actions">
			<button on:click={() => handleLike(true)}>Like ({post.like_count})</button>
			<button on:click={() => handleLike(false)}>Dislike ({post.dislike_count})</button>
		</div>
	{/if}

	<h2>Comments ({comments.length})</h2>

	{#if $isAuthenticated}
		<div class="comment-form">
			<textarea bind:value={commentContent} placeholder="Write a comment..."></textarea>
			<button on:click={handleComment}>Post Comment</button>
		</div>
	{/if}

	{#if error}
		<p class="error">{error}</p>
	{/if}

	<div class="comments-list">
		{#each comments as comment}
			<div class="comment">
				<p class="comment-meta">
					By {comment.author?.username} on {new Date(comment.created_at).toLocaleDateString()}
				</p>
				<p>{comment.content}</p>
			</div>
		{/each}
	</div>
</div>

<style>
	.post-details {
		max-width: 800px;
		margin: 0 auto;
	}
	.meta {
		color: #666;
		font-size: 0.9rem;
	}
	.content {
		margin: 1rem 0;
		line-height: 1.6;
	}
	.actions {
		margin: 1rem 0;
	}
	.actions button {
		margin-right: 1rem;
	}
	.comment-form {
		margin: 1rem 0;
	}
	textarea {
		width: 100%;
		height: 100px;
		margin-bottom: 0.5rem;
	}
	.comments-list {
		margin-top: 1rem;
	}
	.comment {
		border-bottom: 1px solid #eee;
		padding: 1rem 0;
	}
	.comment-meta {
		font-size: 0.8rem;
		color: #666;
	}
	.error {
		color: red;
	}
</style>
