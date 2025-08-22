let isEditing = true;
const titleInput = document.getElementById("note-title");
const contentInput = document.getElementById("content-textarea");
const toggleButton = document.getElementById("toggle-edit");
const statusText = document.getElementById("save-status");

let saveTimer = null;

titleInput.addEventListener("input", handleInputChange);
contentInput.addEventListener("input", handleInputChange);

toggleButton.addEventListener("click", () => {
    isEditing = !isEditing;
    titleInput.readOnly = !isEditing;
    contentInput.readOnly = !isEditing;
    toggleButton.textContent = isEditing ? "View Mode" : "Edit Mode";

    if (isEditing) {
        enableAutoSaveOnChange();
    } else {
        removeAutoSaveListeners();
        saveNote();
    }
});

function enableAutoSaveOnChange() {
    titleInput.addEventListener("input", handleInputChange);
    contentInput.addEventListener("input", handleInputChange);
}

function removeAutoSaveListeners() {
    titleInput.removeEventListener("input", handleInputChange);
    contentInput.removeEventListener("input", handleInputChange);
}

titleInput.addEventListener("blur", () => {
    if (isEditing) saveNote();
});

function handleInputChange() {
    if (saveTimer) clearTimeout(saveTimer);
    statusText.textContent = "Saving...";
    saveTimer = setTimeout(saveNote, 1000); // debounce 1s
}

function saveNote() {
    const title = titleInput.value;
    const content = contentInput.value;

    statusText.textContent = "Saving...";

    fetch(`/notes/${noteId}/autosave/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ 
            title, 
            content,
        })
    }).then(res => {
        if (res.ok) {
            statusText.textContent = "All changes saved";
        } else {
            statusText.textContent = "Error saving changes";
        }
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
