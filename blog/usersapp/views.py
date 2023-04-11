from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, HttpResponseRedirect
from .forms import RegistrationForm
from django.views.generic import CreateView, DetailView
from .models import BlogUser
from rest_framework.authtoken.models import Token
from django.urls import reverse, reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
# Create your views here.
class UserLoginView(LoginView):
    template_name = 'usersapp/login.html'
    #success_url = reverse_lazy('blog:good_list')
    #success_url = reverse_lazy('blog:good_list')


class UserCreateView(CreateView):
    model = BlogUser
    template_name = 'usersapp/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')



# Create your views here.


class UserDetailView(DetailView):
    template_name = 'usersapp/profile.html'
    model = BlogUser


def update_token(request):
    user = request.user
    # если уже есть
    if user.auth_token:
        # обновить
        user.auth_token.delete()
        Token.objects.create(user=user)
    else:
        # создать
        Token.objects.create(user=user)
    return HttpResponseRedirect(reverse('users:profile', kwargs={'pk': user.pk}))


def update_token_ajax(request):
    user = request.user
    # если уже есть
    if user.auth_token:
        # обновить
        user.auth_token.delete()
        token = Token.objects.create(user=user)
    else:
        # создать
        token = Token.objects.create(user=user)
    return JsonResponse({'key': token.key})