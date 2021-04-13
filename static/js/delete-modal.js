class DeleteModal extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
    this.shadowRoot.innerHTML = `
        <style>
            .modal-background {
                position: fixed;
                z-index: 1;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0, 0, 0, 0.5);
            }

            .delete-modal {
                position: absolute;
                background-color: white;
                width: 25rem;
                height: 15rem;
                top: calc(50% - 7.5rem);
                left: calc(50% - 12.5rem);
                display: grid;
                grid-template-columns: 2rem 1fr 2rem;
                grid-template-rows: 2rem 1fr 2rem;
                border-radius: 5%;
            }

            .close-modal {
                grid-column-start: 3;
                grid-column-end: span 1;
                grid-row-start: 1;
                grid-row-end: span 1;
                width: 100%;
                height: 100%;
                text-align: center;
                padding: auto;
                display: flex;
                justify-content: center;
                align-content: center;
                cursor: pointer;
            }

            .close-modal span {
                margin: auto;
                text-align: center;
            }

            .modal-content {
                display: grid;
                grid-template-columns: 50% 50%;
                grid-template-rows: 4rem 2rem 1fr;
                grid-column-start: 2;
                grid-column-end: span 1;
                grid-row-start: 2;
                grid-row-end: span 1;
            }

            .modal-content>h2 {
                grid-column-start: 1;
                grid-column-end: span 2;
                grid-row-start: 1;
                grid-row-end: span 1;
                justify-content: center;
                margin: auto;
            }

            .modal-content>p {
                grid-column-start: 1;
                grid-column-end: span 2;
                grid-row-start: 2;
                grid-row-end: span 1;
                justify-self: start;
                align-self: center;
                margin: 0.5rem 0;
            }

            .cancel-modal-button {
                grid-column-start: 1;
                grid-column-end: span 1;
                grid-row-start: 3;
                grid-row-end: span 1;
                margin: auto;
            }

            .delete-element-button {
                grid-column-start: 2;
                grid-column-end: span 1;
                grid-row-start: 3;
                grid-row-end: span 1;
                margin: auto;
            }

            .hidden {
                display: none;
            }
            button {
              font-weight: bold;
              background: #bfc5c2;
              color: #fff;
              padding: 10px 20px;
              font-size: 14px;
              text-transform: uppercase;
              border-radius: 5%;
              outline: none;
              border: none;
              cursor: pointer;
            }

            button:hover {
              background: #b3b9b6;
            }

            button.delete {
              background: #8d450b;
            }

            button.delete:hover {
              background: #c05f10;
            }
        </style>
        <div class='modal-background hidden'>
            <div class='delete-modal'>
                <div class='close-modal'>
                    <span>X</span>
                </div>
                <div class='modal-content'>
                    <h2>Delete</h2>
                    <p>Are you sure you want to this?</p>
                    <button class='cancel-modal-button'>
                        Cancel
                    </button>
                    <button class='delete-element-button delete'>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    `.trim();

    this.elementDeleteBtns;
    this.parentToDelete;
    this.url = 'http://dummy/url/';

    this.modalBackground = this.shadowRoot.querySelector('.modal-background');
    this.deleteModal = this.modalBackground.querySelector('.delete-modal');
    this.deleteModalH2 = this.deleteModal.querySelector('h2');
    this.cancelModalBtn = this.deleteModal.querySelector(
      '.cancel-modal-button'
    );
    this.closeModalDiv = this.deleteModal.querySelector('.close-modal');
    this.deleteElementBtn = this.deleteModal.querySelector(
      '.delete-element-button'
    );
  }

  connectedCallback() {
    this.cancelModalBtn.addEventListener(
      'click',
      this._closeModalHandler.bind(this),
      false
    );
    this.closeModalDiv.addEventListener(
      'click',
      this._closeModalHandler.bind(this),
      false
    );

    this.deleteElementBtn.addEventListener(
      'click',
      this._deleteElementFetchCallHandler.bind(this),
      false
    );
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (this.hasAttribute('url')) {
      this.url = newValue;
    }
  }

  static get observedAttributes() {
    return ['url'];
  }

  setDeleteBtns(deleteBtns) {
    this.elementDeleteBtns = Array.from(deleteBtns);
    this.elementDeleteBtns.forEach((btn) => {
      btn.addEventListener('click', this._openModalHandler, false);
    });
  }

  setParentToDelete(parentToDelete) {
    this.parentToDelete = parentToDelete;
  }

  _closeModalOnWindowClickHandler(event) {
    let deleteModalBox = this.deleteModal.getBoundingClientRect();
    let left = deleteModalBox.x;
    let right = left + deleteModalBox.width;
    let up = deleteModalBox.y;
    let down = up + deleteModalBox.height;
    if (
      event.target === this &&
      !(
        event.clientX > left &&
        event.clientX < right &&
        event.clientY > up &&
        event.clientY < down
      )
    )
      this.modalBackground.classList.add('hidden');
  }

  _openModalHandler() {
    const deleteModal = document.querySelector('delete-modal');
    const modalBackground = deleteModal.shadowRoot.querySelector(
      '.modal-background'
    );

    let elementId = this.getAttribute('data-id');
    let elementTitle = this.getAttribute('data-title');

    modalBackground.classList.remove('hidden');
    deleteModal._setModalDataAttrs(elementId, elementTitle);
    window.addEventListener(
      'click',
      deleteModal._closeModalOnWindowClickHandler.bind(deleteModal),
      false
    );
  }

  _setModalDataAttrs(elementId, elementTitle) {
    this.setAttribute('data-id', elementId);
    this.setAttribute('data-title', elementTitle);
    let elementObject = this.getAttribute('data-object');
    this.deleteModalH2.textContent = `Delete ${elementTitle} ${elementObject}`;
  }

  _closeModalHandler() {
    window.removeEventListener('click', this._closeModalOnWindowClickHandler);
    this.modalBackground.classList.add('hidden');
  }

  _deleteElementFromDOM(elementId) {
    const elementDeleteBtn = this.elementDeleteBtns.filter((btn) => {
      return parseInt(btn.getAttribute('data-id')) === parseInt(elementId);
    })[0];
    elementDeleteBtn.closest(this.parentToDelete).remove();
  }

  async _deleteElementFetchCallHandler() {
    let elementId = this.getAttribute('data-id');
    let url = this.url + elementId;

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
      this._deleteElementFromDOM(elementId);
      this._closeModalHandler();
    } else {
      console.error(result.status);
    }
  }
}

customElements.define('delete-modal', DeleteModal);
