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
  // console.log('drag enter', event.target, this, event.currentTarget);
  // if (event.currentTarget === this) {
  //   this.classList.add('story-content__item--dragged-over');
  //   console.log('added class');
  // }
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
  // if (event.target === this) {
  //   this.classList.remove('story-content__item--dragged-over');
  //   console.log('removed class');
  // }
}

// In case you drop the element on the target, the drop event fires instead
// of the dragleave event.
// Dropping element on another element, almost all of drag
// and drop logic resides here
function dropHandler(event) {
  if (event.stopPropagation) {
    event.stopPropagation(); // stops the browser from redirecting.
  }
  event.preventDefault();

  draggedOver = this;

  if (dragging !== draggedOver) {
    let draggedOverDOMRect = draggedOver.getBoundingClientRect();
    let draggedOverMiddle =
      draggedOverDOMRect.y + 0.5 * draggedOverDOMRect.height;
    let draggingMiddle = event.clientY;
    if (draggedOverMiddle > draggingMiddle) {
      draggedOver.insertAdjacentElement('beforebegin', dragging);
    } else {
      draggedOver.insertAdjacentElement('afterend', dragging);
    }
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
  // item.addEventListener('dragenter', dragEnterHandler, false);
  item.addEventListener('dragover', dragOverHandler, false);
  // item.addEventListener('dragleave', dragLeaveHandler, false);
  item.addEventListener('drop', dropHandler, false);
}
