from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    # path("", views.PostListView.as_view(), name="index"),
    path("", views.index, name="index"),
    path("<int:pk>" , views.PostDetailView.as_view(), name="details"),
    # path("<int:pk>" , views.PostDetailView, name="details"),
    path("create/",views.CreatePostView.as_view(),name="create"),
    path("edit/<int:pk>",views.EditPostView.as_view(), name="edit"),
    path("delete/<int:pk>",views.DeletePostView.as_view(),name="delete"),
    path('<int:pk>/comment/', views.AddCommentView.as_view(), name='add-comment'),
    path('comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='delete-comment'),
    
]
