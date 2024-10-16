from django.urls import path
from .views import SignUpView
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('profile/', TemplateView.as_view(template_name='accounts/profile.html'), name='profile'),
]
