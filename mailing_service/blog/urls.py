from django.urls import path
from .views import blog_list, blog_detail_view

urlpatterns = [
    path('', blog_list, name='blog_list'),
    path('<int:pk>/', blog_detail_view, name='blog_detail'),
]
