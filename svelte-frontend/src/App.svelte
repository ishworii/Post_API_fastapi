<script>
  let posts = [];

  const fetchPosts = async () => {
    try {
      const res = await fetch("http://localhost:8000/posts");
      posts = await res.json();
      console.log(posts);
    } catch (error) {
      console.error("Error fetching posts:", error);
    }
  };

  // Fetch posts when the component is mounted
  fetchPosts();
</script>

<main>
  <h1>Posts</h1>
  {#if posts.length > 0}
    <ul>
      {#each posts as post}
        <li>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </li>
      {/each}
    </ul>
  {:else}
    <p>No posts available</p>
  {/if}
</main>
