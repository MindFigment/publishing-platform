const followersList = document.querySelector('.followers-list');
let page = 2;
let blockRequest = false;
let margin = 100;
const url = document.getElementById('url').dataset.url;

async function getNextFollowersHandler() {
  let fireFetch =
    document.body.offsetHeight -
      window.innerHeight -
      window.pageYOffset -
      margin <=
    0;

  if (fireFetch && blockRequest === false) {
    blockRequest = true;

    let response = await fetch(
      url +
        '?' +
        new URLSearchParams({
          page: page,
        }),
      {
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        },
      }
    );

    let result = await response.text();

    if (result !== '') {
      page += 1;
      followersList.innerHTML += result;
    }

    blockRequest = false;
  }
}

window.addEventListener('scroll', getNextFollowersHandler, false);
