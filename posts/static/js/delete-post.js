const modalBackground = document.querySelector('.modal-background');
const deleteModal = modalBackground.querySelector('.delete-modal');
const deleteModalH2 = deleteModal.querySelector('h2');
const cancelModalBtn = deleteModal.querySelector('.cancel-modal-button');
const closeModalDiv = deleteModal.querySelector('.close-modal');
const deletePostBtn = deleteModal.querySelector('.delete-blog-button');

function closeModalOnWindowClickHandler(event) {
  if (
    !event.target.classList.contains('delete') &&
    !(event.target === deleteModal) &&
    !deleteModal.contains(event.target)
  )
    modalBackground.classList.add('hidden');
}

function openModalHandler() {
  modalBackground.classList.remove('hidden');
  let postId = this.getAttribute('data-id');
  let postTitle = this.getAttribute('data-title');
  setModalDataAttrs(postId, postTitle);
  window.addEventListener('click', closeModalOnWindowClickHandler, false);
}

function setModalDataAttrs(postId, postTitle) {
  deleteModal.setAttribute('data-id', postId);
  deleteModal.setAttribute('data-title', postTitle);
  deleteModalH2.textContent = `Delete ${postTitle} post`;
}

function closeModalHandler() {
  window.removeEventListener('click', closeModalOnWindowClickHandler);
  modalBackground.classList.add('hidden');
}

function deletePostFromDOM(postId) {
  const postDeleteBtns = Array.from(
    document.querySelectorAll('.delete-blog-btn')
  );
  const postDeleteBtn = postDeleteBtns.filter((btn) => {
    return parseInt(btn.getAttribute('data-id')) === parseInt(postId);
  })[0];
  console.log('btn to delete', postDeleteBtn);
  postDeleteBtn.closest('.post-card-manage').remove();
}

async function deletePostFetchCallHandler() {
  let postId = deleteModal.getAttribute('data-id');
  let url = `http://127.0.0.1:8000/posts/delete/${postId}`;

  const headers = new Headers({
    Accept: 'application/json',
    'X-CSRFToken': getCookie('csrftoken'),
  });

  let response = await fetch(url, {
    method: 'DELETE',
    mode: 'same-origin',
    headers,
  });

  let result = await response.json();

  if (result.status === 'ok') {
    console.log(result.status);
    deletePostFromDOM(postId);
    closeModalHandler();
  } else {
    console.error(result.status);
  }
}

deletePostBtn.addEventListener('click', deletePostFetchCallHandler, false);

let deleteBtns = document.querySelectorAll('.delete-blog-btn');
deleteBtns.forEach((btn) => {
  btn.addEventListener('click', openModalHandler, false);
});

cancelModalBtn.addEventListener('click', closeModalHandler, false);
closeModalDiv.addEventListener('click', closeModalHandler, false);
