
function toggleFollow(user_id) {
    let csrfToken = document.querySelector("#csrf-token").value;

    fetch(`/follow/${user_id}/`, {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update button text and dataset
            updateFollowButton(data.isFollowing);

            // Update followers count
            updateFollowerCount(data.isFollowing);
        } else {
            console.error("Error:", data.error);
        }
    })
    .catch(error => console.error("Fetch error:", error));
}

function updateFollowButton(isFollowing) {
    button = document.querySelector('#follow-unfollow-button');
    if (isFollowing) {
        button.innerHTML = 'Unfollow'
    } else {
        button.innerHTML = 'Follow'
    }
}

function updateFollowerCount(isFollowing) {
    let followerCountElement = document.querySelector('#followers-count');
    
    if (followerCountElement) {
        let currentCount = parseInt(followerCountElement.innerHTML) || 0;
        if (isFollowing) {
            followerCountElement.innerHTML = currentCount + 1;
        } else {
            followerCountElement.innerHTML = currentCount - 1;
        }
    } else {
        console.error("Follower count element not found!");
    }
}

function fetch_profile_page(element) {
    let page_no = element.getAttribute('data-page');
    let profile_id = document.querySelector('#profile-user-id').value;
    
    const route = `/fetch_profile_page/${profile_id}/${page_no}/`;
    fetch(route)
        .then(response => response.json())
        .then(data => {            
            updatePagination(data.user_id, data.post_page, data.page_no, data.page_count, data.page_list);
        });
}


function updatePagination(user_id, post_page, page_no, page_count, page_list) {
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
                    <p class="post-likes">❤️ <span class="likes-count">${post.likes_count}</span></p>
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
                <a class="page-link" data-page="${page_no - 1}" onclick="fetch_profile_page(this)">Previous</a>
            </li>`;
        }

        page_list.forEach(num => {
            if (num === page_no) {
                paginationHTML += `<li class="page-item active">
                    <a class="page-link">${num}</a>
                </li>`;
            } else {
                paginationHTML += `<li class="page-item">
                    <a class="page-link" data-page="${num}" onclick="fetch_profile_page(this)">${num}</a>
                </li>`;
            }
        });

        if (page_no < page_count) {
            paginationHTML += `<li class="page-item">
                <a class="page-link" data-page="${page_no + 1}" onclick="fetch_profile_page(this)">Next</a>
            </li>`;
        }

        paginationHTML += `</ul></nav>`;
    }

    postsDiv.innerHTML = "";
    postsDiv.innerHTML += postsHTML;
    postsDiv.innerHTML += paginationHTML;
}
