document.addEventListener('DOMContentLoaded', function ()  {
    // click post btn event
    if( document.querySelector('#postBtn')) {
        document.querySelector('#postBtn').addEventListener('click', () => savePost());
    }

    if( document.querySelectorAll('.edit-post') && document.querySelectorAll('.edit-post').length > 0) {
        const nodes = document.querySelectorAll('.edit-post');
        nodes.forEach(element => element.addEventListener('click', (e) => editPost(e)));
    }

    if (document.querySelectorAll('.updateBtn') && document.querySelectorAll('.updateBtn').length > 0) {
        const nodes = document.querySelectorAll('.updateBtn');
        nodes.forEach(element => element.addEventListener('click', (e) => updatePost(e)));
    }

    if (document.querySelectorAll('.btnLike') && document.querySelectorAll('.updateBtn').length > 0) {
        const nodes = document.querySelectorAll('.btnLike');
        nodes.forEach(element => element.addEventListener('click', (e) => likePost(e)));
    }
});

/** 
 *  API: SAVE POST 
 */
function savePostApi(postData) {
    // Post data of new data
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify(postData)
    })
    .then(response => response.json())
    .then(() => resetPostField());
}

/**
 * API: UPDATE POST
 */
function updatePostApi(postData) {
    fetch('update', {
        method: 'POST',
        body: JSON.stringify(postData)
    })
    .then((response) => response.json())
    .then(() => {
        hideTextareaUI(postData.content.id);
        updateContentPost(postData.content);
    });
}

/**
 * API: Like a POST
 * @param {*} postData 
 */
function likePostApi(postData) {
    fetch('like', {
        method: 'POST',
        body: JSON.stringify(postData)
    })
    .then((response) => response.json())
    .then((data) => console.log(data));
}

/**
 * Save post api
 */
function savePost() {
    const postContent = document.getElementById(`postContent`).value;
    const postData = {
        content: postContent
    }    
    savePostApi(postData)
}


/**
 * Update Textarea field aft
 */
function resetPostField () {
    document.getElementById(`postContent`).value = ``;
    window.location.replace(`${window.location.origin}/posts`);
}

/**
 * UI to edit post item
 */
function editPost(e) {
    const {target } = e;
    const { dataset } = target;
    const value = dataset['value'];
    const textAreaSelector = `.post-textarea__${value}`;
    const textAreaContentSelector = `#content__${value}`;
    // Toggle display
    if (document.querySelector(textAreaSelector).style.display === `block`) {
        document.querySelector(textAreaSelector).style.display = 'none';
        document.querySelector(textAreaContentSelector).style.display = 'block';
    } else {
        document.querySelector(textAreaSelector).style.display = 'block';
        document.querySelector(textAreaContentSelector).style.display = 'none';
    }
}

/**
 * Update post
 * @param {*} e 
 */
function updatePost(e) {
    const {target } = e;
    const { dataset } = target;
    const value = dataset['value'];
    const textAreaContainer = document.querySelector(`.post-textarea__${value}`);
    const postContent = textAreaContainer.children[0].value;
    
    if (postContent) {
        const postData = {
            content:  {
                id : value,
                post: postContent
            }
        };
    
        updatePostApi(postData);
    }
}

/**
 * Hide textarea input element
 * @param {*} postId 
 */
function hideTextareaUI(postId) {
    const textAreaSelector = `.post-textarea__${postId}`;
    const textAreaContentSelector = `#content__${postId}`;
    document.querySelector(textAreaSelector).style.display = 'none';
    document.querySelector(textAreaContentSelector).style.display = 'block';
}

function updateContentPost(content) {
   if (content && content.id) {
       const element = `#content__${content.id}`;
       document.querySelector(element).innerHTML = content.post;
   }
}

/**
 * Like post 
 * @param {*} e 
 */
function likePost(e) {
    let {target } = e;
    if (target.closest(`.btnLike`)) {
        target = target.closest(`.btnLike`);
        const { dataset } = target;
        const value = dataset['value'];

        const postData = {
            content : {
                id: value
            }
        };

        likePostApi(postData);
    }
}