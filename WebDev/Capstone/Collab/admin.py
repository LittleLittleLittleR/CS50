from django.contrib import admin

# Register your models here.

from .models import User, Folder, Note, Shared_Folder, Shared_Note

admin.site.register(User)
admin.site.register(Folder)
admin.site.register(Note)
admin.site.register(Shared_Folder)
admin.site.register(Shared_Note)
