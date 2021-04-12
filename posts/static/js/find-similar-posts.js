const post = JSON.parse(document.getElementById('post-data').textContent);
const similarDiv = document.querySelector('.similar');
const findSimilarBtn = document.querySelector('.find-similar-posts');

function processSimilarPosts(posts) {
  posts.forEach((postData) => createPostCard(postData));
}

function createPostCard(postData) {
  postCardDiv = document.createElement('div');
  postCardDiv.innerHTML = displayPostCard(postData);
  similarDiv.append(postCardDiv.firstChild);
}

function displayPostCard(postData) {
  let insertImage = '';
  if (postData.image.length > 0)
    insertImage = `<img src="data:image;base64,${postData.image}"/>`;

  postTemplate = `
            <div class="post-card-detailed">
                <div class="post-card-detailed__avatar post-image">
                    <a href="${postData.url}">
                        ${insertImage}                   
                    </a>
                </div>
                <div class="post-card-detailed__content">
                    <div class="post-detailed__title">
                        <a href="${postData.url}">${postData.title}</a>
                    </div>
                    <div class="post-card-detailed__avatar author-image">
                        <img src="data:image;base64,${postData.author.image}">
                        <div>
                            <div class="post-detailed__info">
                                By <a href="${postData.author.url}"> 
                                ${postData.author.username} </a>
                                on <a href="${postData.blog.url}">
                                ${postData.blog.title} </a>
                            </div>
                            <div class="post-detailed__published">${
                              postData.publish
                            }</div>
                        </div>
                    </div>
                    <div class="post-detailed__first-paragraph">
                        ${postData.text.slice(0, 200)}...
                    </div>
                    <div class="post-detailed__tags">
                        tags: ${
                          postData.tags.length !== 0
                            ? Array.from(postData.tags).map(
                                (tag) => ' #' + tag.name
                              )
                            : 'post not tagged'
                        }
                    </div>
                </div>
            </div>
            `.trim();
  return postTemplate;
}

function findSimilarPostsHandler() {
  console.log(post);
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

findSimilarBtn.addEventListener('click', findSimilarPostsHandler, false);
