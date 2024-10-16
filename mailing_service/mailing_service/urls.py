from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mailing/', include('mailing.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),  # Главная страница
]
