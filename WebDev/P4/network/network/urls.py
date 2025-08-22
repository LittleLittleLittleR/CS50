from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("new-post", views.new_post, name="new-post"),
    path("create-post", views.create_post, name="create-post"), 
    path("following", views.following, name="following"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path('fetch_page/<str:filter>/<int:page_no>/', views.fetch_page, name='fetch_page'),
    path('fetch_profile_page/<int:profile_id>/<int:page_no>/', views.fetch_profile_page, name='fetch_profile_page'),
    path("edit_post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("like_post/<int:post_id>/", views.like_post, name="like_post"),
]