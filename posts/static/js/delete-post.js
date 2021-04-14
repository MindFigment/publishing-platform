let deleteBtns = document.querySelectorAll('.delete-post-btn');
const deleteModal = document.querySelector('delete-modal');
deleteModal.setDeleteBtns(deleteBtns);
deleteModal.setParentToDelete('.post-card-manage');
