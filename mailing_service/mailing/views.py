from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Client, Message, Mailing
from .forms import ClientForm, MessageForm, MailingForm
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from blog.models import BlogPost
import random
from django.shortcuts import render
from django.core.cache import cache


User = get_user_model()


class ManagerUserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'manager/user_list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()


class ManagerUserBlockView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ['is_active']
    template_name = 'manager/user_block_confirm.html'
    success_url = reverse_lazy('manager_user_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.is_active = False
        user.save()
        return redirect('manager_user_list')


# Клиенты
class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client_list.html'

    def get_queryset(self):
        return Client.objects.filter(owner=self.request.user)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('client_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client_form.html'
    success_url = reverse_lazy('client_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.owner


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    template_name = 'client_confirm_delete.html'
    success_url = reverse_lazy('client_list')

    def test_func(self):
        client = self.get_object()
        return self.request.user == client.owner


# Сообщения
class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message_list.html'

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('message_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'message_form.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.owner


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    template_name = 'message_confirm_delete.html'
    success_url = reverse_lazy('message_list')

    def test_func(self):
        message = self.get_object()
        return self.request.user == message.owner


# Рассылки
class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(owner=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner


class MailingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')

    def test_func(self):
        mailing = self.get_object()
        return self.request.user == mailing.owner


class ManagerMailingListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Mailing
    template_name = 'manager/mailing_list_manager.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def get_queryset(self):
        return Mailing.objects.all()


class ManagerClientListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Client
    template_name = 'mailing/client_list_manager.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def get_queryset(self):
        return Client.objects.all()


class ManagerMessageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Message
    template_name = 'mailing/message_list_manager.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def get_queryset(self):
        return Message.objects.all()


class ManagerMailingDisableView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Mailing
    fields = ['is_active']
    template_name = 'manager/mailing_disable_confirm.html'
    success_url = reverse_lazy('manager_mailing_list')

    def test_func(self):
        return self.request.user.groups.filter(name='Manager').exists()

    def post(self, request, *args, **kwargs):
        mailing = get_object_or_404(Mailing, pk=kwargs['pk'])
        mailing.is_active = False
        mailing.save()
        return redirect('manager_mailing_list')

@cache_page(60 * 15)
def home_view(request):
    total_mailings = Mailing.objects.count()

    active_mailings = Mailing.objects.filter(is_active=True).count()

    unique_clients = Client.objects.aggregate(total_clients=Count('email', distinct=True))['total_clients']

    blog_posts = list(BlogPost.objects.all())
    random_blog_posts = random.sample(blog_posts, min(3, len(blog_posts)))

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_clients': unique_clients,
        'blog_posts': random_blog_posts,
    }

    return render(request, 'home.html', context)