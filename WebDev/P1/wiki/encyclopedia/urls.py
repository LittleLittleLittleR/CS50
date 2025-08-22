from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"), 
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.new, name="new"),
    path("save_new/", views.save_new, name="save_new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("random/", views.random_entry, name="random")
]
