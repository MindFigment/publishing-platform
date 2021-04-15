const post = JSON.parse(document.getElementById('post-data').textContent);
const similarDiv = document.querySelector('.similar');
const findSimilarBtn = document.querySelector('.find-similar-posts');

function findSimilarPostsHandler() {
  fetch(
    'http://localhost:8000/search/posts/similar?' +
      new URLSearchParams({
        slug: post,
        n: 6,
      })
  )
    .then((res) => res.json())
    .then((rawPosts) => Promise.all(rawPosts.map((p) => JSON.parse(p))))
    .then((posts) => {
      if (posts.length > 0) {
        similarDiv.innerHTML = `<h2>Similar posts (${posts.length})</h2>`;
        processSimilarPosts(posts);
      } else {
        similarDiv.innerHTML = '<p>No similar posts found :(</p>';
      }
    })
    .catch((err) => console.error(err));
}

function processSimilarPosts(posts) {
  posts.forEach((postData) => createPostCardDetailed(postData));
}

function createPostCardDetailed(postData) {
  postCardDiv = document.createElement('div');
  let postCardDetailed = document.createElement('post-card-detailed');
  postCardDetailed.setPostData(postData);
  similarDiv.append(postCardDetailed);
}

findSimilarBtn.addEventListener('click', findSimilarPostsHandler, false);
