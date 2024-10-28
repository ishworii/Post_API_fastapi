<script lang="ts">
	import { goto } from '$app/navigation';
	import { authenticatedFetch } from '$lib/api';

	let title = '';
	let content = '';
	let error = '';

	async function handleSubmit() {
		if (!title || !content) {
			error = 'Please fill in both title and content';
			return;
		}

		try {
			const response = await authenticatedFetch(`${import.meta.env.VITE_API_URL}/posts`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ title, content })
			});

			if (response.ok) {
				const newPost = await response.json();
				console.log('New post created:', newPost);
				goto('/'); // Redirect to homepage after successful post creation
			} else {
				const errorData = await response.json();
				error = errorData.detail || 'Failed to create post';
			}
		} catch (err) {
			console.error('Error creating post:', err);
			error = 'An error occurred while creating the post';
		}
	}
</script>

<div class="create-post-container">
	<h1>Create New Post</h1>

	<form on:submit|preventDefault={handleSubmit}>
		<div class="form-group">
			<label for="title">Title:</label>
			<input type="text" id="title" bind:value={title} required />
		</div>
		<div class="form-group">
			<label for="content">Content:</label>
			<textarea id="content" bind:value={content} required></textarea>
		</div>
		{#if error}
			<p class="error">{error}</p>
		{/if}
		<button type="submit">Create Post</button>
	</form>
</div>

<style>
	.create-post-container {
		max-width: 600px;
		margin: 0 auto;
		padding: 20px;
	}
	.form-group {
		margin-bottom: 15px;
	}
	label {
		display: block;
		margin-bottom: 5px;
	}
	input,
	textarea {
		width: 100%;
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
	}
	textarea {
		height: 150px;
		resize: vertical;
	}
	button {
		padding: 10px 15px;
		background-color: #0066cc;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
	}
	.error {
		color: red;
		margin-top: 10px;
	}
</style>
