const postsList = document.querySelector('.posts-list');
let page = 1;
let n = 6;
let blockRequest = false;
let margin = 200;
const url = 'http://127.0.0.1:8000/posts/detailed';

async function getNextPostsHandler() {
  let fireFetch =
    document.body.offsetHeight -
      window.innerHeight -
      window.pageYOffset -
      margin <=
    0;

  if (fireFetch && blockRequest === false) {
    console.log('sending request');
    blockRequest = true;

    let response = await fetch(
      url +
        '?' +
        new URLSearchParams({
          page: page,
          n: n,
        }),
      {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      }
    );

    let result = await response.json();
    if (!result.empty) {
      let posts = await Promise.all(result.map((p) => JSON.parse(p)));
      if (posts.length > 0) {
        processPosts(posts);
        page += 1;
        blockRequest = false;
      } else if (page === 1) {
        postsList.innerHTML = '<p>No posts found :(</p>';
        blockRequest = true;
      } else {
        blockRequest = true;
      }
    }
  }
}

function processPosts(posts) {
  posts.forEach((postData) => createPostCardDetailed(postData));
}

function createPostCardDetailed(postData) {
  postCardDiv = document.createElement('div');
  let postCardDetailed = document.createElement('post-card-detailed');
  postCardDetailed.setPostData(postData);
  console.log(postCardDetailed);
  postsList.append(postCardDetailed);
}

getNextPostsHandler();
window.addEventListener('scroll', getNextPostsHandler, false);
