document.addEventListener('DOMContentLoaded', function ()  {
    // click post btn event
    document.querySelector('#postBtn').addEventListener('click', () => savePost());
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
}

