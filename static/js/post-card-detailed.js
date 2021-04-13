class PostCardDetailed extends HTMLElement {
  constructor() {
    super();
    this.postData;
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (this.hasAttribute('postdata')) {
      this.postData = JSON.parse(newValue);
      this._render();
    }
  }

  static get observedAttributes() {
    return ['postdata'];
  }

  setPostData(postData) {
    this.postData = postData;
    this._render();
  }

  _render() {
    let postData = this.postData;
    let insertImage = '';
    if (postData.image.length > 0)
      insertImage = `<img src="data:image;base64,${postData.image}"/>`;
    let postTemplate = `
        <div class="post-card-detailed">
            <div class="post-card-detailed__avatar post-image">
                <a href="${postData.url}">
                    ${insertImage}                   
                </a>
            </div>
            <div class="post-card-detailed__content">
                <div class="post-detailed__title">
                    <a href="${postData.url}">${postData.title}</a>
                </div>
                <div class="post-card-detailed__avatar author-image">
                    <img src="data:image;base64,${postData.author.image}">
                    <div>
                        <div class="post-detailed__info">
                            By <a href="${postData.author.url}"> 
                            ${postData.author.username} </a>
                            on <a href="${postData.blog.url}">
                            ${postData.blog.title} </a>
                        </div>
                        <div class="post-detailed__published">${
                          postData.publish
                        }</div>
                    </div>
                </div>
                <div class="post-detailed__first-paragraph">
                    ${postData.text.slice(0, 200)}...
                </div>
                <div class="post-detailed__tags">
                    tags: ${
                      postData.tags.length !== 0
                        ? Array.from(postData.tags).map(
                            (tag) => ' #' + tag.name
                          )
                        : 'post not tagged'
                    }
                </div>
            </div>
        </div>
        `.trim();

    this.innerHTML = postTemplate;
  }
}

customElements.define('post-card-detailed', PostCardDetailed);
