const followBtn = document.querySelector('.follow.button');
const totalFollowersSpan = document.querySelector('.count .total');

async function followHandler(event) {
  let url = 'http://localhost:8000/blogs/follow/';
  let body = {
    id: this.dataset.id,
    action: this.dataset.action,
  };

  event.preventDefault();
  let response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(body),
  });

  let result = await response.json();

  if (result.status === 'ok') {
    updateFollowers();
  }
}

function updateFollowers() {
  let previous_action = followBtn.dataset.action;

  // toggle data-action
  followBtn.dataset.action =
    previous_action === 'follow' ? 'unfollow' : 'follow';

  // toggle link text
  followBtn.text = previous_action == 'follow' ? 'Unfollow' : 'Follow';

  // update total followers
  let previous_followers = parseInt(totalFollowersSpan.innerHTML);
  totalFollowersSpan.innerHTML =
    previous_action === 'follow'
      ? previous_followers + 1
      : previous_followers - 1;
}

if (followBtn !== null) {
  followBtn.addEventListener('click', followHandler, false);
}
