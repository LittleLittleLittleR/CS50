
function fetch_page(element, filter) {
    let page_no = element.getAttribute('data-page');
    
    const route = `/fetch_page/${filter}/${page_no}/`;
    fetch(route)
        .then(response => response.json())
        .then(data => {            
            updatePagination(data.user_id, data.post_page, data.page_no, data.page_count, data.page_list, filter);
        });
}

function updatePagination(user_id, post_page, page_no, page_count, page_list, filter) {
    let postsDiv = document.querySelector("#posts-div");

    // Construct posts HTML
    let postsHTML = "";
    post_page.forEach(post => {
        postsHTML += `
            <div class="post-div">
                <input type="hidden" class="post-id" value="${post.id}">
                <div class="post-header-div">
                    <h5 class="post-user"><a href="/profile/${post.user.id}">@${post.user.username}</a></h5>
                    <div class="post-datetime">${post.datetime}</div>
                </div>
                <div class="post-content-div">
                    <p class="post-content">${post.content}</p>
                    ${user_id == post.user.id ? '<button class="edit-post-button" onclick="edit_post(this)">edit</button>' : ''}
                </div>
                <div class="post-like-div">
                    <p class="post-likes">❤️ <span class="likes-count">${post.likes_count }</span></p>
                    <button class="like-post-button" onclick="like_post(this)">like</button>
                </div>
            </div>
        `;
    });

    // Construct pagination HTML
    let paginationHTML = "";
    if (page_list.length > 0) {
        paginationHTML = `<nav aria-label="Page navigation example" id="pagination-nav">
            <ul class="pagination">`;
        
        if (page_no > 1) {
            paginationHTML += `<li class="page-item">
                <a class="page-link" data-page="${page_no - 1}" onclick="fetch_page(this, '${filter}')">Previous</a>
            </li>`;
        }

        page_list.forEach(num => {
            if (num === page_no) {
                paginationHTML += `<li class="page-item active">
                    <a class="page-link">${num}</a>
                </li>`;
            } else {
                paginationHTML += `<li class="page-item">
                    <a class="page-link" data-page="${num}" onclick="fetch_page(this, '${filter}')">${num}</a>
                </li>`;
            }
        });

        if (page_no < page_count) {
            paginationHTML += `<li class="page-item">
                <a class="page-link" data-page="${page_no + 1}" onclick="fetch_page(this, '${filter}')">Next</a>
            </li>`;
        }

        paginationHTML += `</ul></nav>`;
    }

    postsDiv.innerHTML = "";
    postsDiv.innerHTML += postsHTML;
    postsDiv.innerHTML += paginationHTML;
}


function edit_post(edit_button) {
    let post_div = edit_button.closest(".post-div");
    let content_ptag = post_div.querySelector(".post-content");

    // Create textarea with existing content
    let content_textarea = document.createElement("textarea");
    content_textarea.classList.add("content-textarea");
    content_textarea.value = content_ptag.textContent;

    // Create confirm button
    let confirm_button = document.createElement("button");
    confirm_button.textContent = "confirm";
    confirm_button.classList.add("confirm-post-button");

    // Replace p tag with textarea
    content_ptag.replaceWith(content_textarea);
    edit_button.replaceWith(confirm_button);

    // Handle confirm button click
    confirm_button.onclick = function () {
        let csrfToken = document.querySelector("#csrf-token").value;
        let new_content = content_textarea.value;
        let post_id = post_div.querySelector(".post-id").value;

        // Send updated content to backend
        fetch(`/edit_post/${post_id}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ content: new_content })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to update post.");
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                // Update UI
                let new_ptag = document.createElement("p");
                new_ptag.classList.add("post-content");
                new_ptag.textContent = new_content;

                content_textarea.replaceWith(new_ptag);
                confirm_button.replaceWith(edit_button);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    };
}


function like_post(like_button) {
    let csrfToken = document.querySelector("#csrf-token").value;
    let post_div = like_button.closest(".post-div");
    let post_id = post_div.querySelector(".post-id").value;
    let like_count = post_div.querySelector(".likes-count");

    fetch(`/like_post/${post_id}/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Failed to update likes.");
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Update UI
            if (data.isLiked) {
                like_button.innerText = "Unlike";
                like_count.innerText ++;
            } else {
                like_button.innerText = "Like";
                like_count.innerText --;
            }
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}