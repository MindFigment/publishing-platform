const modalBackground = document.querySelector('.modal-background');
const deleteModal = modalBackground.querySelector('.delete-modal');
const deleteModalH2 = deleteModal.querySelector('h2');
const cancelModalBtn = deleteModal.querySelector('.cancel-modal-button');
const closeModalDiv = deleteModal.querySelector('.close-modal');
const deleteBlogBtn = deleteModal.querySelector('.delete-blog-button');

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
  let blogId = this.getAttribute('data-id');
  let blogTitle = this.getAttribute('data-title');
  setModalDataAttrs(blogId, blogTitle);
  window.addEventListener('click', closeModalOnWindowClickHandler, false);
}

function setModalDataAttrs(blogId, blogTitle) {
  deleteModal.setAttribute('data-id', blogId);
  deleteModal.setAttribute('data-title', blogTitle);
  deleteModalH2.textContent = `Delete ${blogTitle} blog`;
}

function closeModalHandler() {
  window.removeEventListener('click', closeModalOnWindowClickHandler);
  modalBackground.classList.add('hidden');
}

function deleteBlogFromDOM(blogId) {
  const blogDeleteBtns = Array.from(
    document.querySelectorAll('.delete-blog-btn')
  );
  const blogDeleteBtn = blogDeleteBtns.filter((btn) => {
    return parseInt(btn.getAttribute('data-id')) === parseInt(blogId);
  })[0];
  console.log('btn to delete', blogDeleteBtn);
  blogDeleteBtn.closest('.blog-card').remove();
}

async function deleteBlogFetchCallHandler() {
  let blogId = deleteModal.getAttribute('data-id');
  let url = `http://127.0.0.1:8000/blogs/delete/${blogId}`;

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
    deleteBlogFromDOM(blogId);
    closeModalHandler();
  } else {
    console.error(result.status);
  }
}

deleteBlogBtn.addEventListener('click', deleteBlogFetchCallHandler, false);

let deleteBtns = document.querySelectorAll('.delete-blog-btn');
deleteBtns.forEach((btn) => {
  btn.addEventListener('click', openModalHandler, false);
});

cancelModalBtn.addEventListener('click', closeModalHandler, false);
closeModalDiv.addEventListener('click', closeModalHandler, false);
