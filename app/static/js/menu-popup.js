const heroImg = document.querySelector('#hero');
const menuPopup = document.querySelector('#menu-popup');

function fadeToggleHandler(event) {
  menuPopup.classList.toggle('fade');
}

function closeMenuPopupHandler(event) {
  if (
    heroImg !== event.target &&
    menuPopup !== event.target &&
    !menuPopup.contains(event.target)
  )
    menuPopup.classList.add('fade');
}

if (heroImg) {
  heroImg.addEventListener('click', fadeToggleHandler, false);
  window.addEventListener('mouseup', closeMenuPopupHandler, false);
}
