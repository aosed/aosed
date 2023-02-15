from django.urls import path
from . import views
from .views import PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('search/', views.search, name='search'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('detail/<int:post_id>/', views.post_detail, name='detail'),
    path('new_post/', PostCreateView.as_view(), name='new_post'),
    path('detail/<slug:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('detail/<slug:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
