class BlogCardDetailed extends HTMLElement {
  constructor() {
    super();
    this.blogData;
  }

  attributeChangedCallback(name, oldValue, newValue) {
    if (this.hasAttribute('blogdata')) {
      this.blogData = JSON.parse(newValue);
      this._render();
    }
  }

  static get observedAttributes() {
    return ['blogdata'];
  }

  setBlogData(blogData) {
    this.blogData = blogData;
    this._render();
  }

  _render() {
    let blogData = this.blogData;
    let insertImage = '';
    if (blogData.image.length > 0)
      insertImage = `<img src="data:image;base64,${blogData.image}"/>`;
    let blogTemplate = `
        <div class="blog-card-detailed">
            <div class="blog-card-detailed__blog-avatar">
                <a href="${blogData.url}">
                    ${insertImage}                   
                </a>
            </div>
            <div class="blog-card-detailed__content">
                <div class="blog-detailed__title">
                    <a href="${blogData.url}">${blogData.title}</a>
                </div>
                <div class="blog-card-detailed__author-avatar">
                    <img src="data:image;base64,${blogData.author.image}">
                    <div class="author-info">
                      <div class="author-info__first-row">
                        By
                        <a href="${blogData.author.url}" class="emphasis">
                          ${blogData.author.username}
                        </a>
                      </div>
                      <div class="author-info__second-row">
                        Blog active since ${blogData.created}
                      </div>
                    </div>
                </div>
                <div class="blog-detailed__about">
                    ${blogData.about.slice(0, 220)}...
                </div>
                <div class="blog-detailed__tags">
                    tags: ${
                      blogData.tags.length !== 0
                        ? Array.from(blogData.tags).map(
                            (tag) => ' #' + tag.name
                          )
                        : 'blog not tagged'
                    }
                </div>
            </div>
        </div>
        `.trim();

    this.innerHTML = blogTemplate;
  }
}

customElements.define('blog-card-detailed', BlogCardDetailed);
