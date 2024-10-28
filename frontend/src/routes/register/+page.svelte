<script lang="ts">
	import { goto } from '$app/navigation';

	let username = '';
	let email = '';
	let password = '';
	let error = '';

	async function handleSubmit() {
		const response = await fetch(`${import.meta.env.VITE_API_URL}/users/register`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ username, email, password })
		});

		if (response.ok) {
			const data = await response.json();
			console.log('Registration successful', data);
			goto('/login'); // Redirect to login page after successful registration
		} else {
			const errorData = await response.json();
			error = errorData.detail || 'Registration failed';
		}
	}
</script>

<div class="form-container">
	<h1>Register</h1>
	<form on:submit|preventDefault={handleSubmit}>
		<div class="form-group">
			<label for="username">Username:</label>
			<input type="text" id="username" bind:value={username} required />
		</div>
		<div class="form-group">
			<label for="email">Email:</label>
			<input type="email" id="email" bind:value={email} required />
		</div>
		<div class="form-group">
			<label for="password">Password:</label>
			<input type="password" id="password" bind:value={password} required />
		</div>
		{#if error}
			<p class="error">{error}</p>
		{/if}
		<button type="submit">Register</button>
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
