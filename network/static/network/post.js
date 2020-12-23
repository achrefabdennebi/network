document.addEventListener('DOMContentLoaded', function ()  {
    // click post btn event
    if( document.querySelector('#postBtn')) {
        document.querySelector('#postBtn').addEventListener('click', () => savePost());
    }

    if( document.querySelectorAll('.edit-post') && document.querySelectorAll('.edit-post').length > 0) {
        const nodes = document.querySelectorAll('.edit-post');
        nodes.forEach(element => {
            element.addEventListener('click', (e) => editPost(e));
        });
    }

    if (document.querySelectorAll('.updateBtn')) {
        const nodes = document.querySelectorAll('.updateBtn');
        nodes.forEach(element => {
            element.addEventListener('click', (e) => updatePost(e));
        });
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
    const textAreaSelector = `.post-textarea__${value}`;
    const textAreaContentSelector = `#content__${value}`;
    document.querySelector(textAreaSelector).style.display = 'none';
    document.querySelector(textAreaContentSelector).style.display = 'block';
}

