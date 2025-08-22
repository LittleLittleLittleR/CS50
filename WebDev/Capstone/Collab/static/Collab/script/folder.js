
// Toggle Rename Divs
function toggleRename(type, id, name) {
    let message = `Rename "${name}"`

    if (type === "folder") {
        let folderOverlay = document.getElementById("rename-folder-overlay");
        let folderIdInput = document.getElementById("rename-folder-id");
        let folderText = document.getElementById("rename-folder-text");
        const isVisible = folderOverlay.style.display === "flex";

        folderOverlay.style.display = isVisible ? "none" : "flex";
        folderIdInput.value = id;
        folderText.innerText = message;

    } else if (type === "note") {
        let noteOverlay = document.getElementById("rename-note-overlay");
        let noteIdInput = document.getElementById("rename-note-id");
        let noteText = document.getElementById("rename-note-text");
        const isVisible = noteOverlay.style.display === "flex";

        noteOverlay.style.display = isVisible ? "none" : "flex";
        noteIdInput.value = id;
        noteText.innerText = message;        
    }
}


// Toggle Delete Divs
function toggleDelete(type, id, name) {
    let message = `Delete "${name}"`

    if (type === "folder") {
        let folderOverlay = document.getElementById("delete-folder-overlay");
        let folderIdInput = document.getElementById("delete-folder-id");
        let folderText = document.getElementById("delete-folder-text");
        const isVisible = folderOverlay.style.display === "flex";

        folderOverlay.style.display = isVisible ? "none" : "flex";
        folderText.innerText = message;
        folderIdInput.value = id;
    } else if (type === "note") {
        let noteOverlay = document.getElementById("delete-note-overlay");
        let noteIdInput = document.getElementById("delete-note-id");
        let noteText = document.getElementById("delete-note-text");
        const isVisible = noteOverlay.style.display === "flex";

        noteOverlay.style.display = isVisible ? "none" : "flex";
        noteText.innerText = message;
        noteIdInput.value = id;
    }
}

function toggleShare(type, id, name) {
    let message = `Share "${name}"`

    if (type === "folder") {
        let folderOverlay = document.getElementById("share-folder-overlay");
        let folderIdInput = document.getElementById("share-folder-id");
        let folderText = document.getElementById("share-folder-text");
        const isVisible = folderOverlay.style.display === "flex";

        folderOverlay.style.display = isVisible ? "none" : "flex";
        folderText.innerText = message;
        folderIdInput.value = id;
    } else if (type === "note") {
        let noteOverlay = document.getElementById("share-note-overlay");
        let noteIdInput = document.getElementById("share-note-id");
        let noteText = document.getElementById("share-note-text");
        const isVisible = noteOverlay.style.display === "flex";

        noteOverlay.style.display = isVisible ? "none" : "flex";
        noteText.innerText = message;
        noteIdInput.value = id;
    }
}


function closeOverlay() {
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.style.display = "none";

        // Clear inputs inside the modal (including hidden inputs)
        let inputs = overlay.querySelectorAll('input');
        inputs.forEach(input => input.value = "");

        // Clear text elements (like prompt messages)
        let texts = overlay.querySelectorAll('p');
        texts.forEach(p => p.innerText = "");
    });
}

// Eventlistener to close overlay when onclicked
document.querySelectorAll('.modal-overlay').forEach(overlay => {
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) {
            overlay.style.display = 'none';
        }
    });
});


// Rename
function renameFolder(event) {
    event.preventDefault();

    const folderId = document.getElementById("rename-folder-id").value;
    const newSubject = document.getElementById("new-subject").value;

    fetch(`/folders/${folderId}/rename/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            new_subject: newSubject
        })
    })
    .then(data => {
        location.reload(); 
    })
    .catch(error => alert(error.message))
    .finally(() => {
        closeOverlay();
    });
}

function renameNote(event) {
    event.preventDefault();

    const noteId = document.getElementById("rename-note-id").value;
    const newTitle = document.getElementById("new-title").value;

    fetch(`/notes/${noteId}/rename/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            new_title: newTitle
        })
    })
    .then(response => {})
    .then(data => {
        location.reload();
    })
    .catch(error => alert(error.message))
    .finally(() => {
        closeOverlay();
    });
}


// Delete
function deleteFolder(event) {
    event.preventDefault();

    const folderId = document.getElementById("delete-folder-id").value;

    fetch(`/folders/${folderId}/delete/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        }
    })
    .then(response => {
        if (!response.ok) throw new Error("Failed to delete folder.");
        return response.json();
    })
    .then(data => {
        location.reload();
    })
    .catch(error => alert(error.message))
    .finally(() => {
        closeOverlay();
    });
}



function deleteNote(event) {
    event.preventDefault();

    const noteId = document.getElementById("delete-note-id").value;
    const folderInput = document.getElementById("note-folder-id");
    const folderId = folderInput ? folderInput.value : null;

    fetch(`/notes/${noteId}/delete/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        }
    })
    .then(response => {
        closeOverlay();
        if (response.ok) {
            const redirectUrl = folderId ? `/folders/${folderId}` : "/notes/";
            window.location.href = redirectUrl;
        } else {
            alert("Failed to delete note.");
        }
    })
}

function shareFolder(event) {
    event.preventDefault();

    const folderId = document.getElementById("share-folder-id").value;
    const useremail = document.getElementById("share-folder-useremail").value;

    fetch(`/folders/${folderId}/share/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            useremail: useremail
        })
    })
    .then(data => {
        location.reload();
    })
    .catch(error => alert(error.message))
    .finally(() => {
        closeOverlay();
    });
}

function shareNote(event) {
    event.preventDefault();

    const noteId = document.getElementById("share-note-id").value;
    const useremail = document.getElementById("share-note-useremail").value;

    fetch(`/notes/${noteId}/share/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            useremail: useremail
        })
    })
    .then(data => {
        location.reload();
    })
    .catch(error => alert(error.message))
    .finally(() => {
        closeOverlay();
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
