const blogsList = document.querySelector('.blogs-list-detailed');
let page = 1;
let n = 6;
let blockRequest = false;
let margin = 200;
const url = 'http://127.0.0.1:8000/blogs/detailed';

async function getNextBlogsHandler() {
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
      let blogs = await Promise.all(result.map((b) => JSON.parse(b)));
      if (blogs.length > 0) {
        processBlogs(blogs);
        page += 1;
        blockRequest = false;
      } else if (page === 1) {
        blogsList.innerHTML = '<p>No blogs found :(</p>';
        blockRequest = true;
      } else {
        blockRequest = true;
      }
    }
  }
}

function processBlogs(blogs) {
  blogs.forEach((blogData) => createBlogCardDetailed(blogData));
}

function createBlogCardDetailed(blogData) {
  blogCardDiv = document.createElement('div');
  let blogCardDetailed = document.createElement('blog-card-detailed');
  blogCardDetailed.setBlogData(blogData);
  console.log(blogCardDetailed);
  blogsList.append(blogCardDetailed);
}

getNextBlogsHandler();
window.addEventListener('scroll', getNextBlogsHandler, false);
