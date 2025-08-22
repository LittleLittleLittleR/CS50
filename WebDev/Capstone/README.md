# CS50 Web Programming Capstone Project - Collabs

## Description
This is a web application platform for note-taking, folder-based organization, and collaboration. Users can create nested folders, add and edit notes, and share individual notes or entire folders with collaborators. The inspiration behind this project stems from the collaborative editing power of Google Docs that allows simple yet seamless sharing and collaboration across users in.

The project implements a structured folder/file system, share permissions, and optional collaboration modes, all wrapped in a Dockerized Django backend.

## Project Structure (Simplified)
```
root/
├── Capstone/
├── Collab/             # Core Django app
│   ├── migrations/
│   ├── static/Collab
│   │   ├── script/
│   │   └── style/
│   ├── templates/Collab
│   ├── _init_.py
│   ├── admin.py
│   ├── apps.py
│   ├── views.py
│   ├── tests.py
│   ├── models.py
│   └── urls.py
├── db.sqlite3
├── dockerfile
├── manage.py
├── README.md
└── requirements.txt
```

## Getting Started and Running the Application
You can run this app in two main ways: Docker (recommended for portability) or locally via pip.

### Running with Docker + uv (recommended)
1. Install Docker or Docker Desktop
2. Start Docker Desktop
3. Build the container: 
```
docker build -t capstone .
```
4. Run the container: 
```
docker run -p 8000:8000 capstone
```
5. Visit the app at: http://localhost:8000

### Running with pip (manual setup)
1. Create a virtual environment (optional but recommended)
2. Install dependencies: 
```
pip install -r requirements.txt
```
3. Start the server: 
```
python manage.py runserver
```
4. Visit: http://localhost:8000

## Endpoints
Below are the key routes exposed by the application:

### Authentication
- `login/` - Log in
- `logout/` - Log out
- `register/` - Create a new account

### Folder & Notes Navigation
- `/` - Index, the home page, that displays the 10 most recent notes that were worked out, from Personal Notes and Collab Notes each
- `notes/` - Personal Notes, notes that are owned by the user
- `collabs/` - Collab Notes, notes that are shared with the user
- `add_note/` - Create a new note in that specific folder which this endpoint is called
- `notes/<int:note_id>/` - View and Edit a note
- `notes/<int:note_id>/autosave/` - Called every 1 second after the user types in the note, saving the content and title of the note
- `notes/<int:note_id>/delete/` - Delete note
- `notes/<int:note_id>/rename/` - Rename note
- `notes/<int:note_id>/share/` - Share note via email
- `add_folder/` - Create a new folder
- `folders/<int:folder_id>/` - View contents of the folder, which includes all notes and folders in it
- `folders/<int:folder_id>/delete/` - Delete folder
- `folders/<int:folder_id>/rename/` - Rename folder
- `folders/<int:folder_id>/share/` - Share folder via email

## Templates
Below are the HTML files and their contents

- `layout.html` - Basic structor for all the other pages
- `login.html` - Login and register page (login.css, login.js)
- `index.html` - The home page, which displays the 10 most recently edited notes from Personal and Collabs folder respectively (index.css)
- `folder.html` - The folder view, containing all the notes and nested folders in that specific folder. (folder.css, folder.js)
- `note.html` - The note view, containing the content and note title of the note (note.css, note.js)


## Distinctiveness and Complexity

Apart from having a different concept from the rest (neither a scial network nor e-commerce site), here is what sets it apart:

#### Nested Folder/File Structure
- Users can create folders inside folders, and notes inside any folder, creating a full tree structure. This proved to be a greater challenge while creating the models.

#### Shareable Notes and Folders
- You can share individual notes or entire folders.
- Sharing a folder automatically gives access to everything inside it, respecting the hierarchy.

#### Docker + uv Integration
- Docker allows you to containerize the entire application, ensuring it runs identically in any environment.
- `uv` is a next-gen Python package manager that installs faster and resolves dependencies more reliably than `pip`.
- Retained `requirements.txt` (instead of `pyproject.toml`) to comply with course requirements, though `uv` natively supports TOML.

## Future Improvements
Here are features planned for the next iteration:

- **Move Notes and Folders**: Add moving of notes and folders option, with drag-and-drop or context menus to relocate notes and folders.
- **Permission Types**: Share as view-only, comment-only, or full edit.
- **RAG (Retrieval-Augmented Generation) Summarizer**: A planned AI assistant to help summarize or explain notes using NLP. 

footnote: This project was initially going to be a notes co-pilot. That is why I want to implement an AI RAG assistant in the future, and also why I dockerised the web-app and the implementation of `uv` was to help with the installation of large dependencies such as `transformers`. but model limitations on CPU and local resources made it impractical for now. In the future, hosting the model and web app on a cloud server (e.g. AWS) will allow full integration of this assistant.