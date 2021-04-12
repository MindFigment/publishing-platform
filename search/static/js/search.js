const searchPosts = JSON.parse(
  document.getElementById('search_posts').textContent
);
const searchBlogs = JSON.parse(
  document.getElementById('search_blogs').textContent
);

if (searchPosts && searchBlogs) {
  const postsBtn = document.querySelector('.posts-button');
  const blogsBtn = document.querySelector('.blogs-button');

  const postsList = document.querySelector('.search-result-list.posts');
  const blogsList = document.querySelector('.search-result-list.blogs');

  function toggleSearchResultsHandler() {
    postsList.classList.toggle('hidden');
    postsBtn.toggleAttribute('disabled');

    blogsList.classList.toggle('hidden');
    blogsBtn.toggleAttribute('disabled');
  }

  postsBtn.addEventListener('click', toggleSearchResultsHandler, false);
  blogsBtn.addEventListener('click', toggleSearchResultsHandler, false);
}
