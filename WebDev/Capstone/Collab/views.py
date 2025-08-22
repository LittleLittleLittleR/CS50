from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404

import json

from .models import User, Folder, Note, Shared_Folder, Shared_Note


## Helpers

def redirect_back(request, fallback='notes'):
    return redirect(request.META.get('HTTP_REFERER', fallback))

## Views

def index(request):
    if request.user.is_authenticated:
        personal_notes = Note.objects.filter(user=request.user).order_by('-updated_at')[:10]
        collab_notes = Note.objects.filter(shared_with__user=request.user).order_by('-updated_at')[:10]

        return render(request, "Collab/index.html", {
            "user": request.user,
            "personal_notes": personal_notes,
            "collab_notes": collab_notes,
        })
    else:
        return render(request, "Collab/login.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Collab/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Collab/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "Collab/login.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Collab/login.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Collab/login.html")



## Notes Views ##

@login_required
def notes(request):
    # Get folders owned by the user
    folders = Folder.objects.filter(user=request.user, parent__isnull=True).order_by('-updated_at')
    
    # Get notes that are not in any folder
    ungrouped_notes = Note.objects.filter(user=request.user, folder__isnull=True).order_by('-updated_at')
    
    return render(request, "Collab/folder.html", {
        "folders": folders,
        "notes": ungrouped_notes,
        "is_collab": False,
    })


@login_required
def collabs(request):
    shared_notes = Note.objects.filter(shared_with__user=request.user, folder__isnull=True).order_by('-updated_at')
    shared_folders = Folder.objects.filter(shared_with__user=request.user, parent__isnull=True).order_by('-updated_at')

    return render(request, "Collab/folder.html", {
        "folders": shared_folders,
        "notes": shared_notes,
        "is_collab": True, 
    })


@login_required
def add_note(request):
    if request.method == "POST":
        title = "Untitled Note"
        content = ""
        folder_id = request.POST.get("folder", None)

        note = Note(user=request.user, title=title, content=content)
        
        if folder_id:
            folder = Folder.objects.get(id=folder_id, user=request.user)
            note.folder = folder

        note.save()
    return redirect_back(request)


@login_required
def note_view(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.user != request.user and not note.shared_with.filter(user=request.user).exists():
        return HttpResponseForbidden()
    
    folder = note.folder
    is_collab = request.GET.get("is_collab") == "1"
    
    if folder and folder.user != request.user and not folder.shared_with.filter(user=request.user).exists():
        folder = None


    return render(request, "Collab/note.html", {
        "note": note,
        "folder": folder,
        "is_collab": is_collab,
    })


@require_POST
@login_required
@csrf_exempt
def autosave_note(request, note_id):
    try:
        data = json.loads(request.body)
        note = get_object_or_404(Note, id=note_id)
        note.title = data.get("title", note.title)
        note.content = data.get("content", note.content)
        note.save()
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)



@login_required
def delete_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.delete()
        return JsonResponse({"success": True})
    return HttpResponseBadRequest("Invalid method")

@login_required
def rename_note(request, note_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_title = data.get("new_title")

        note = get_object_or_404(Note, id=note_id, user=request.user)
        note.title = new_title
        note.save()

    return JsonResponse({"success": True, "new_title": new_title})

@login_required
def share_note(request, note_id):
    if request.method == "POST":
        data = json.loads(request.body)
        useremail = data.get("useremail")
        user = get_object_or_404(User, email=useremail)
        note = get_object_or_404(Note, pk=note_id)

        if note.user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        _, created = Shared_Note.objects.get_or_create(note=note, user=user)
        return JsonResponse({"success": f"Note shared with {useremail}"})


## Folders Views ##

@login_required
def add_folder(request):
    if request.method == "POST":
        subject = "Untitled Folder"
        parent_id = request.POST.get("parent", None)

        folder = Folder(user=request.user, subject=subject)

        if parent_id:
            # Ensure the parent folder exists and belongs to the user
            parent_folder = get_object_or_404(Folder, id=parent_id, user=request.user)
            folder.parent = parent_folder
        else:
            folder.parent = None

        folder.save()
    return redirect_back(request)


@login_required
def folder_view(request, folder_id):

    folder = get_object_or_404(Folder, id=folder_id)
    if folder.user != request.user and not folder.shared_with.filter(user=request.user).exists():
        return HttpResponseForbidden()

    path = []
    current = folder
    while current:
        path.insert(0, current)
        parent = current.parent
        if not parent:
            break
        if parent.user != request.user and not parent.shared_with.filter(user=request.user).exists():
            break
        current = parent

    is_collab = request.GET.get("is_collab") == "1"
    notes = Note.objects.filter(folder=folder).order_by('-updated_at')
    subfolders = Folder.objects.filter(parent=folder).order_by('-updated_at')

    return render(request, "Collab/folder.html", {
        "dir_path": path,
        "parent_folder": folder,
        "folders": subfolders,
        "notes": notes,
        "is_collab": is_collab,
    })


@login_required
def delete_folder(request, folder_id):
    if request.method == "POST":
        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        folder.delete()
        return JsonResponse({"success": True})
    return HttpResponseBadRequest("Invalid method")


@login_required
def rename_folder(request, folder_id):
    if request.method == "POST":
        data = json.loads(request.body)
        new_subject = data.get("new_subject")

        folder = get_object_or_404(Folder, id=folder_id, user=request.user)
        folder.subject = new_subject
        folder.save()

    return JsonResponse({"success": True, "new_subject": new_subject})


@login_required
def share_folder(request, folder_id):
    if request.method == "POST":
        data = json.loads(request.body)
        useremail = data.get("useremail")
        user = get_object_or_404(User, email=useremail)
        folder = get_object_or_404(Folder, pk=folder_id)

        if folder.user != request.user:
            return JsonResponse({"error": "Unauthorized"}, status=403)

        _, created = Shared_Folder.objects.get_or_create(folder=folder, user=user)
        return JsonResponse({"success": f"Folder shared with {useremail}"})