let deleteBtns = document.querySelectorAll('.delete-blog-btn');
const deleteModal = document.querySelector('delete-modal');
deleteModal.setDeleteBtns(deleteBtns);
deleteModal.setParentToDelete('.blog-card');
