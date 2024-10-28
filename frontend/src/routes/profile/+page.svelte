<script lang="ts">
	import { authenticatedFetch } from '$lib/api';
	import { onMount } from 'svelte';

	let profile = null;
	let error = '';
	let isEditing = false;
	let editedProfile = {};

	onMount(async () => {
		try {
			const response = await authenticatedFetch(`${import.meta.env.VITE_API_URL}/users/me`);
			if (response.ok) {
				profile = await response.json();
				editedProfile = { ...profile };
			} else {
				error = 'Failed to fetch profile';
			}
		} catch (err) {
			console.error('Error fetching profile:', err);
			error = 'An error occurred while fetching the profile';
		}
	});

	async function handleSubmit() {
		try {
			const response = await authenticatedFetch(`${import.meta.env.VITE_API_URL}/users`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(editedProfile)
			});

			if (response.ok) {
				profile = await response.json();
				isEditing = false;
				error = '';
			} else {
				error = 'Failed to update profile';
			}
		} catch (err) {
			console.error('Error updating profile:', err);
			error = 'An error occurred while updating the profile';
		}
	}
</script>

<div class="profile-container">
	<h1>User Profile</h1>

	{#if error}
		<p class="error">{error}</p>
	{/if}

	{#if profile}
		{#if isEditing}
			<form on:submit|preventDefault={handleSubmit}>
				<div class="form-group">
					<label for="username">Username:</label>
					<input type="text" id="username" bind:value={editedProfile.username} disabled />
				</div>
				<div class="form-group">
					<label for="email">Email:</label>
					<input type="email" id="email" bind:value={editedProfile.email} />
				</div>
				<div class="form-group">
					<label for="full_name">Full Name:</label>
					<input type="text" id="full_name" bind:value={editedProfile.full_name} />
				</div>
				<button type="submit">Save Changes</button>
				<button type="button" on:click={() => (isEditing = false)}>Cancel</button>
			</form>
		{:else}
			<div class="profile-info">
				<p><strong>Username:</strong> {profile.username}</p>
				<p><strong>Email:</strong> {profile.email}</p>
				<p><strong>Full Name:</strong> {profile.full_name || 'Not set'}</p>
				<p><strong>User ID:</strong> {profile.id}</p>
				<p><strong>Role:</strong> {profile.role}</p>
			</div>
			<button on:click={() => (isEditing = true)}>Edit Profile</button>
		{/if}
	{:else}
		<p>Loading profile...</p>
	{/if}
</div>

<style>
	.profile-container {
		max-width: 600px;
		margin: 0 auto;
		padding: 20px;
	}
	.profile-info p {
		margin: 10px 0;
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
		padding: 10px 15px;
		background-color: #0066cc;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		margin-right: 10px;
	}
	.error {
		color: red;
		margin-top: 10px;
	}
</style>
