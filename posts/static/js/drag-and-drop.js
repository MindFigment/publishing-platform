const storyContent = document.getElementById('story-content');
let storyItems = Array.from(
  storyContent.querySelectorAll('.story-content__item')
);

// Get buttons which control adding sections to the story
const addTextBtn = document.getElementById('add-text');
const addSubtitleBtn = document.getElementById('add-subtitle');
const addImgBtn = document.getElementById('add-img');
const addCitationBtn = document.getElementById('add-citation');

/*
    Get all empty forms (provided by django) which are blueprints for adding 
    new story items.
    Additionaly, we keep track of total number of forms of each type. This info
    is needed when adding or deleting story item.
*/
const emptySubtitleForm = document.getElementById('empty-subtitle-form');
const emptyTextForm = document.getElementById('empty-text-form');
const emptyImageForm = document.getElementById('empty-image-form');
const emptyCitationForm = document.getElementById('empty-citation-form');
let totalSubtitleForms = document.getElementById('id_subtitle-TOTAL_FORMS');
let totalTextForms = document.getElementById('id_text-TOTAL_FORMS');
let totalImageForms = document.getElementById('id_image-TOTAL_FORMS');
let totalCitationForms = document.getElementById('id_citation-TOTAL_FORMS');
console.log('total image forms', totalImageForms.value);

// Factory function for creating handlers responsible for removing different
// types of story items (subtitles, texts, images, dividers...)
function removeStoryItemHandlerFactory(
  totalForms,
  itemToRemoveIdentifier = '.story-content__item'
) {
  function removeStoryItemHandler() {
    // event.target.parentElement.parentElement.remove();
    this.closest(itemToRemoveIdentifier).remove();
    // event.target.parentElement.parentElement.remove()
    totalForms.value = parseInt(totalForms.value) - 1;
  }
  return removeStoryItemHandler;
}

const removeSubtitleHandler = removeStoryItemHandlerFactory(totalSubtitleForms);
const removeTextHandler = removeStoryItemHandlerFactory(totalTextForms);
const removeImageHandler = removeStoryItemHandlerFactory(totalImageForms);
const removeCitationHandler = removeStoryItemHandlerFactory(totalCitationForms);

// Get title item, it cannot be removed, but its position can be changed.
// Meaning it doesn't have to be first item in the story. We can for example set
// image as a first item.
// let titleItem = document.getElementById('id-title').cloneNode(true);

// Helper function for building components encapsulating story items
function buildStoryItem(emptyForm, totalForms, removeItemHandeler) {
  let storyItemDiv = document.createElement('div');
  storyItemDiv.className = 'story-content__item';
  storyItemDiv.setAttribute('draggable', true);

  let wrapperDiv = document.createElement('div');
  wrapperDiv.className = 'item__wrapper';

  let removeButton = document.createElement('input');
  removeButton.setAttribute('type', 'button');
  removeButton.setAttribute('value', 'X');
  removeButton.className = 'button-remove';

  // Fill provided form skeleton
  wrapperDiv.innerHTML = emptyForm.innerHTML.replace(
    /__prefix__/g,
    totalForms.value
  );
  wrapperDiv.append(removeButton);
  storyItemDiv.append(wrapperDiv);

  // Set all necessary listeners, both for drag&drop and removing items
  applyDragAndDropListeners(storyItemDiv);
  removeButton.addEventListener('click', removeItemHandeler);

  const inputFile = wrapperDiv.querySelector('input[type="file"]');
  if (inputFile) {
    buildImagePreview(inputFile);
  }

  // // ###############
  // // #### IMAGE ####
  // // ###############

  // const inputFile = wrapperDiv.querySelector('input[type="file"]');
  // if (inputFile) {
  //   // Get input img element
  //   // const inputFile = wrapperDiv.querySelector('input[type="file"]');
  //   inputFile.addEventListener('change', function () {
  //     // console.log('input file', URL.createObjectURL(inputFile.value));
  //     if (this.files && this.files[0]) {
  //       // Get img src element
  //       let img = wrapperDiv.querySelector('img');
  //       img.onload = () => {
  //         console.log('img', img, new Image(), this.files);
  //         console.log(img.width + 'x' + img.height);
  //         // img.width = 200;
  //         // img.height = 200;
  //         // im = img;
  //         // URL.revokeObjectURL(img.src); // no longer needed, free memory
  //       };
  //       // img.src = this.value;
  //       img.src = URL.createObjectURL(this.files[0]); // set src to blob url
  //     }
  //   });
  // }

  return storyItemDiv;
}

function buildImagePreview(inputFile) {
  // ###############
  // #### IMAGE ####
  // ###############
  if (inputFile) {
    // Get input img element
    // const inputFile = wrapperDiv.querySelector('input[type="file"]');
    console.log('listener input file', inputFile.files);
    inputFile.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        // Get img src element
        let img = inputFile.parentElement.querySelector('img');
        img.onload = () => {
          console.log('img', img, new Image(), this.files);
          console.log(img.width + 'x' + img.height);
          // img.width = 200;
          // img.height = 200;
          // im = img;
          // URL.revokeObjectURL(img.src); // no longer needed, free memory
        };
        // img.src = this.value;
        img.src = URL.createObjectURL(this.files[0]); // set src to blob url
      }
    });
  }
}

let inputFiles = document.querySelectorAll('input[type="file"]');
console.log('input files', inputFiles);
inputFiles.forEach((inputFile) => buildImagePreview(inputFile));

function addStoryItemToDOMFactory(emptyForm, totalForms, removeItemHandeler) {
  storyItem = buildStoryItem(emptyForm, totalForms, removeItemHandeler);
  storyItems.push(storyItem);
  storyContent.append(storyItem);
  totalForms.value = parseInt(totalForms.value) + 1;
}

const addSubtitleToDOMHandler = () =>
  addStoryItemToDOMFactory(
    emptySubtitleForm,
    totalSubtitleForms,
    removeSubtitleHandler
  );
const addTextToDOMHandler = () =>
  addStoryItemToDOMFactory(emptyTextForm, totalTextForms, removeTextHandler);
const addCitationToDOMHandler = () =>
  addStoryItemToDOMFactory(
    emptyCitationForm,
    totalCitationForms,
    removeCitationHandler
  );
const addImageToDOMHandler = () =>
  addStoryItemToDOMFactory(emptyImageForm, totalImageForms, removeImageHandler);

addSubtitleBtn.addEventListener('click', addSubtitleToDOMHandler);
addTextBtn.addEventListener('click', addTextToDOMHandler);
addCitationBtn.addEventListener('click', addCitationToDOMHandler);
addImgBtn.addEventListener('click', addImageToDOMHandler);

// #######################
// #### DRAG AND DROP ####
// #######################

// Variables for holding currently dragged item (dragging)
// and item where we want insert it (draggedOver)
let dragging, draggedOver;

// EVENTS ON DRAGGABLE ELEMENTS
// When you drag an element, these events fire in the following sequence:
// 1. dragstart
// 2. drag
// 3. dragend

// The target of all events (event.target) is the element that is being dragged.

// When you hold a mouse button and begin to move the mouse,
// the dragstart event fires on the draggable element that you’re dragging.
// The cursor changes to a no-drop symbol (a circle with a line through it)
// to indicate that you cannot drop the element on itself.
function dragStartHandler() {
  dragging = this;
  // console.log('dragstart', dragging);
}

// After the dragstart event fires, the drag event fires repeatedly as
// long as you drag the element.
function dragHandler() {
  // console.log('drag');
}

// At the end, the dragend event fires when you stop dragging the element.
function dragEndHandler() {
  // console.log('dragend');
}

// EVENTS ON DROP TARGETS
// When you drag an element over a valid drop target, these events fire
// in the following sequence:
// 1. dragenter
// 2.dragover
// 3.dragleave or drop

// The target (e.target) of the dragenter, dragover, dragleave, and
// drop events are the drop target elements.

// The dragenter event fires as soon as you drag the element over a
// drop target.
function dragEnterHandler(event) {
  // console.log('dragenter');
  // if (event.stopPropagation) {
  //   event.stopPropagation(); // stops the browser from redirecting.
  // }
  // event.preventDefault();
  if (event.target === this) {
    // this.classList.add('story-content__item--dragged-over');
    // console.log('added class');
  }
}

// After the dragenter event fires, the dragover event fires repeatedly
// as long as you’re dragging the element within the boundary of the drop target.
function dragOverHandler(event) {
  if (event.preventDefault) {
    event.preventDefault();
  }
  return false;
}

// When you drag the element outside of the boundary of the drop target,
// the dragover event stops firing and the dragleave event fires.
function dragLeaveHandler(event) {
  // console.log('dragleave');
  // if (event.stopPropagation) {
  //   event.stopPropagation(); // stops the browser from redirecting.
  //   console.log('stop propagation');
  // }
  // console.log(event.target);
  // console.log(event.target, this, event.target === this);
  if (event.target === this) {
    // this.classList.remove('story-content__item--dragged-over');
    // console.log('removed class');
  }
}

// In case you drop the element on the target, the drop event fires instead
// of the dragleave event.
// Dropping element on another element, almost all of drag
// and drop logic resides here
function dropHandler(event) {
  console.log('aaa');
  if (event.stopPropagation) {
    event.stopPropagation(); // stops the browser from redirecting.
  }
  event.preventDefault();

  draggedOver = this;

  console.log('AAAAAAAAAAAAAABBBBBBBBBB', dragging !== draggedOver);

  if (dragging !== draggedOver) {
    let draggingDOMRect = event.target.getBoundingClientRect();
    let draggedOverDOMRect = draggedOver.getBoundingClientRect();
    let draggedOverMiddle =
      draggedOverDOMRect.y + 0.5 * draggedOverDOMRect.height;
    let draggingMiddle = draggingDOMRect.y + 0.5 * draggingDOMRect.height;
    let insertedStoryItem =
      draggedOverMiddle > draggingMiddle
        ? draggedOver.insertAdjacentElement('beforebegin', dragging)
        : draggedOver.insertAdjacentElement('afterend', dragging);

    console.log('dragging middle', draggingMiddle);
    console.log('dragged middle', draggedOverMiddle);
    console.log('inserted', insertedStoryItem);
  }

  return false;
}

function applyDragAndDropListeners(item) {
  item.draggable = true;

  // Events on draggable elements
  item.addEventListener('dragstart', dragStartHandler, false);
  item.addEventListener('drag', dragHandler, false);
  item.addEventListener('dragend', dragEndHandler, false);

  // Events on drop targets
  item.addEventListener('dragenter', dragEnterHandler, false);
  item.addEventListener('dragover', dragOverHandler, false);
  item.addEventListener('dragleave', dragLeaveHandler, false);
  item.addEventListener('drop', dropHandler, false);
}

storyItems.forEach(applyDragAndDropListeners);
console.log(storyItems);

function setStoryItemOrderBeforeSubmit(event) {
  let orderInps = Array.from(
    storyContent.querySelectorAll('.item__wrapper input[type="hidden"]')
  );
  let order = 0;
  orderInps.forEach((orderInp) => {
    orderInp.value = order;
    order++;
  });
  console.log('order inpts', orderInps);
  orderInps.forEach((o_i) => console.log(oi_, o_i.value));
  // event.preventDefault();
}
const submitStoryInp = document.querySelector('.form');
console.log('submitStoryInp', submitStoryInp);
submitStoryInp.addEventListener('submit', setStoryItemOrderBeforeSubmit, false);
