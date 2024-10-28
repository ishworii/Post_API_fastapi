<script lang="ts">
	import { goto } from '$app/navigation';
	import { isAuthenticated, logout } from '$lib/stores/auth';

	function handleLogout() {
		logout();
		goto('/');
	}
</script>

<div class="app-container">
	<nav>
		<div class="left-nav">
			<a href="/" class="nav-button">Home</a>
			{#if $isAuthenticated}
				<a href="/create-post" class="nav-button">Create Post</a>
			{/if}
		</div>
		<div class="right-nav">
			{#if $isAuthenticated}
				<a href="/profile" class="nav-button">Profile</a>
				<button on:click={handleLogout} class="nav-button">Logout</button>
			{:else}
				<a href="/login" class="nav-button">Login</a>
				<a href="/register" class="nav-button">Register</a>
			{/if}
		</div>
	</nav>

	<main>
		<slot></slot>
	</main>
</div>

<style>
	.app-container {
		max-width: 1200px;
		margin: 0 auto;
		padding: 0 20px;
	}
	nav {
		display: flex;
		justify-content: space-between;
		padding: 1rem 0;
		border-bottom: 1px solid #ddd;
	}
	.left-nav,
	.right-nav {
		display: flex;
		gap: 1rem;
	}
	.nav-button {
		padding: 0.5rem 1rem;
		background-color: #0066cc;
		color: white;
		text-decoration: none;
		border-radius: 4px;
		border: none;
		cursor: pointer;
		font-size: 1rem;
	}
	main {
		padding: 2rem 0;
	}
</style>
