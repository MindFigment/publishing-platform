const postsBtn = document.querySelector('.posts-button');
const blogsBtn = document.querySelector('.blogs-button');

const postsList = document.querySelector('.blogs-detailed-list');
const blogsList = document.querySelector('.posts-detailed-list');

function toggleListsHandler() {
  postsList.classList.toggle('hidden');
  postsBtn.toggleAttribute('disabled');

  blogsList.classList.toggle('hidden');
  blogsBtn.toggleAttribute('disabled');
}

postsBtn.addEventListener('click', toggleListsHandler, false);
blogsBtn.addEventListener('click', toggleListsHandler, false);
