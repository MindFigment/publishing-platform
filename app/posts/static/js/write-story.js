const storyContent = document.querySelector('.story-content');
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

// Factory function for creating handlers responsible for removing different
// types of story items (subtitles, texts, images, dividers...)
function removeStoryItemHandlerFactory(
  totalForms,
  itemToRemoveIdentifier = '.story-content__item'
) {
  function removeStoryItemHandler() {
    this.closest(itemToRemoveIdentifier).remove();
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
  removeButton.setAttribute('value', 'x');
  removeButton.className = 'button-remove delete';

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
    wrapperDiv.classList.add('item__img-wrapper');
    buildImagePreview(inputFile);
  }

  const textArea = wrapperDiv.querySelector('textarea');
  if (textArea) {
    textArea.addEventListener('input', autoGrowTextFieldHandler, false);
  }

  return storyItemDiv;
}

function buildImagePreview(inputFile) {
  if (inputFile) {
    // Get input img element
    inputFile.addEventListener('change', function () {
      if (this.files && this.files[0]) {
        // Get img src element
        let img = inputFile.parentElement.querySelector('img');
        img.onload = () => {
          URL.revokeObjectURL(img.src); // no longer needed, free memory
        };
        img.src = URL.createObjectURL(this.files[0]); // set src to blob url
      }
    });
  }
}

// let inputFiles = document.querySelectorAll('input[type="file"]');
// inputFiles.forEach((inputFile) => buildImagePreview(inputFile));

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

function autoGrowTextFieldHandler() {
  this.style.height = 0;
  this.style.height = this.scrollHeight + 1 + 'px';
}

function autoGrowTextField(elem) {
  if (elem.scrollHeight > 0) {
    elem.style.height = 0;
    elem.style.height = elem.scrollHeight + 'px';
  }
}

function compareStoryItemsOrder(item1, item2) {
  value1 = item1.querySelector('input[name$=order]').value;
  value2 = item2.querySelector('input[name$=order]').value;
  return value1 - value2;
}

/* Sorting and adding necessary elements for story items */

function prepareStoryForEdit() {
  console.log('prepare', storyItems);
  if (storyItems.length > 0) {
    storyItems.sort(compareStoryItemsOrder);
    storyContent.innerHTML = '';
    storyItems.forEach((storyItem) => {
      type = storyItem.className.split(' ').pop();

      let wrapperDiv = storyItem.querySelector('.item__wrapper');

      let inputFile = storyItem.querySelector('input[type="file"]');
      console.log('inp', inputFile, wrapperDiv);
      if (inputFile) {
        let inputOrderHidden = storyItem.querySelector('input[type="hidden"]');
        let wrapperImg = storyItem.querySelector('.img-wrapper');
        let fileUrl = new URL(storyItem.querySelector('a').href);
        let img = storyItem.querySelector('img');
        img.src = fileUrl;
        wrapperDiv.classList.add('item__img-wrapper');
        wrapperDiv.innerHTML = '';
        wrapperDiv.append(inputFile);
        wrapperDiv.append(inputOrderHidden);
        wrapperDiv.append(wrapperImg);
        buildImagePreview(inputFile);
      }

      if (type !== 'title_' && type !== 'story_content__item') {
        let removeButton = document.createElement('input');
        removeButton.setAttribute('type', 'button');
        removeButton.setAttribute('value', 'x');
        removeButton.className = 'button-remove delete';

        if (type === 'text_') {
          removeButton.addEventListener('click', removeTextHandler);
        } else if (type === 'citation_') {
          removeButton.addEventListener('click', removeCitationHandler);
        } else if (type === 'image_') {
          removeButton.addEventListener('click', removeImageHandler);
        } else if (type === 'subtitle_') {
          removeButton.addEventListener('click', removeSubtitleHandler);
        }

        wrapperDiv = storyItem.children[0];
        wrapperDiv.append(removeButton);
      }

      // Set all necessary listeners, both for drag&drop and removing items
      applyDragAndDropListeners(storyItem);
      storyItem.style.display = '';
      storyContent.append(storyItem);
    });
  }

  const textareas = Array.from(storyContent.querySelectorAll('textarea'));
  textareas.forEach((textarea) => {
    autoGrowTextField(textarea);
    textarea.addEventListener('input', autoGrowTextFieldHandler, false);
  });
}

prepareStoryForEdit();
