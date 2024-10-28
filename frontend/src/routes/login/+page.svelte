<script lang="ts">
	import { goto } from '$app/navigation';
	import { login } from '$lib/stores/auth';

	let username = '';
	let password = '';
	let error = '';

	async function handleSubmit() {
		const formData = new URLSearchParams();
		formData.append('username', username);
		formData.append('password', password);

		try {
			const response = await fetch(`${import.meta.env.VITE_API_URL}/users/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/x-www-form-urlencoded'
				},
				body: formData
			});

			if (response.ok) {
				const data = await response.json();
				login(data.access_token);
				goto('/');
			} else {
				const errorData = await response.json();
				error = errorData.detail || 'Invalid username or password';
			}
		} catch (err) {
			console.error('Login error:', err);
			error = 'An error occurred during login';
		}
	}
</script>

<div class="form-container">
	<h1>Login</h1>
	<form on:submit|preventDefault={handleSubmit}>
		<div class="form-group">
			<label for="username">Username:</label>
			<input type="text" id="username" bind:value={username} required />
		</div>
		<div class="form-group">
			<label for="password">Password:</label>
			<input type="password" id="password" bind:value={password} required />
		</div>
		{#if error}
			<p class="error">{error}</p>
		{/if}
		<button type="submit">Login</button>
	</form>
</div>

<style>
	.form-container {
		max-width: 300px;
		margin: 0 auto;
		padding: 20px;
		border: 1px solid #ddd;
		border-radius: 5px;
	}
	.form-group {
		margin-bottom: 15px;
	}
	label {
		display: block;
		margin-bottom: 5px;
	}
	input {
		width: 100%;
		padding: 8px;
		border: 1px solid #ddd;
		border-radius: 4px;
	}
	button {
		width: 100%;
		padding: 10px;
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
