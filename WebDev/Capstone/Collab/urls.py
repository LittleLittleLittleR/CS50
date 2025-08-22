from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    # Page URLs
    path('notes/', views.notes, name='notes'),
    path("collabs/", views.collabs, name="collabs"),
    # Notes URLs
    path('add_note/', views.add_note, name='add_note'),
    path('notes/<int:note_id>/', views.note_view, name='note_view'),
    path('notes/<int:note_id>/autosave/', views.autosave_note, name='autosave_note'),
    path('notes/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('notes/<int:note_id>/rename/', views.rename_note, name='rename_note'),
    path('notes/<int:note_id>/share/', views.share_note, name='share_note'),
    # Folder URLs
    path('add_folder/', views.add_folder, name='add_folder'),
    path('folders/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('folders/<int:folder_id>/delete/', views.delete_folder, name='delete_folder'),
    path('folders/<int:folder_id>/rename/', views.rename_folder, name='rename_folder'),
    path('folders/<int:folder_id>/share/', views.share_folder, name='share_folder'),
]