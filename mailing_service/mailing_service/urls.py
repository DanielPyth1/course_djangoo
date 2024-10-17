from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from mailing.views import ManagerMailingListView, ManagerMessageListView, ManagerClientListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('mailing/', include('mailing.urls')),
    path('manager/mailings/', ManagerMailingListView.as_view(), name='manager_mailing_list'),
    path('manager/messages/', ManagerMessageListView.as_view(), name='manager_message_list'),
    path('manager/clients/', ManagerClientListView.as_view(), name='manager_client_list'),
    path('blog/', include('blog.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
