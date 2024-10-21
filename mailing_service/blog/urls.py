from django.urls import path
from .views import blog_list, blog_detail_view, BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<int:pk>/', blog_detail_view, name='blog_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blog_create'),
    path('<int:pk>/update/', BlogPostUpdateView.as_view(), name='blog_update'),
    path('<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blog_delete'),
]
