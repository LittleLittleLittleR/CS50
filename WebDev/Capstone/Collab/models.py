from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    def __str__(self):
        return f"{self.id} {self.username} {self.email}"


class Folder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject} by {self.user.username}"


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, max_length=1024)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.user.username}"

class Shared_Folder(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_folders')

    class Meta:
        unique_together = ('folder', 'user')

    def __str__(self):
        return f"Folder '{self.folder.subject}' shared with {self.user.username}"

class Shared_Note(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_with')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')

    class Meta:
        unique_together = ('note', 'user')

    def __str__(self):
        return f"Note '{self.note.title}' shared with {self.user.username}"
