from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good, Merchandise
from .forms import ContactForm,RequestForm, CreateForm
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
#from edadeal import ED
from usersapp.models import BlogUser
from django.core.paginator import Paginator
# Create your views here.
class MainListView(ListView):
    model = Merchandise
    template_name = 'blogapp/index.html'
    context_object_name = 'merch'
    paginate_by = 80 # Number of items to show per page
    def get_queryset(self):
        user = BlogUser.objects.filter(username=self.request.user)
        if len(user) == 0:
            user = BlogUser.objects.filter(is_superuser = True)
        return Merchandise.objects.filter(user = user[0])
    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'главная страница'

        paginator = Paginator(self.object_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context
class MainDetailView(DetailView):
    model = Merchandise
    template_name = 'blogapp/merch.html'
    context_object_name = 'merch'
class MerchFormView(FormView):
    form_class = RequestForm
    success_url = reverse_lazy('blog:index')
    template_name = 'blogapp/request.html'
    def form_valid(self, form):
        #superuser = BlogUser.objects.filter(is_superuser=True)
        #user = superuser[0]
        #form.instance.user = self.request.user
        user = BlogUser.objects.filter(username = self.request.user)
        markets = form.cleaned_data['favorite_markets']
        city = form.cleaned_data['favorite_cities']
        print(form.cleaned_data)
        Merchandise.objects.filter(user = self.request.user).delete()
        for market in markets:
            Merchandise().fill_base(user, city, market)
            pass
        return super().form_valid(form)
class SendFormView(FormView):
    form_class = ContactForm
    success_url = reverse_lazy('blog:index')
    template_name = 'blogapp/send.html'
    def form_valid(self, form):
        # Получить данные из формы
        name = form.cleaned_data['name']
        message = form.cleaned_data['message']
        email = form.cleaned_data['email']
        merch = Merchandise.objects.all()
        list_result = [entry.name + ' в ' + entry.market_name for entry in merch]  # converts QuerySet into Python list
        myString = '\n'.join(list_result)
        send_mail(
            'Contact message',
            f'{name}, сообщаю, что {message}\nНе забудь купить:\n{myString}',
            'from@example.com',
            [email],
            fail_silently=True,
        )
        return super().form_valid(form)
class GoodListView(ListView):
    model = Good
    template_name = 'blogapp/good_list.html'
    def get_queryset(self):
        user = BlogUser.objects.filter(username=self.request.user)
        if len(user) == 0:
            user = BlogUser.objects.filter(is_superuser = True)
        queryset = Good.active_objects.get_queryset_user(user[0])
        return queryset

class GoodDetailView(DetailView):

    model = Good
    template_name = 'blogapp/good_detail.html'
    context_object_name = 'merch'

    def get(self, request, *args, **kwargs):
        """
        Метод обработки get запроса
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.good_id = kwargs['pk']
        return super().get(request, *args, **kwargs)
    def get_object(self, queryset=None):
        """
        Получение этого объекта
        :param queryset:
        :return:
        """
        good = get_object_or_404(Good, pk=self.good_id)
        merch = Merchandise.objects.filter(good = good)
        self.len_merch = len(merch)
        return merch
    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['len'] = self.len_merch
        return context
#создание поста
class GoodCreateView(CreateView):
    #form_class = CreateForm
    fields = ('name',)
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_create.html'
    #exclude = ('user',)
    def form_valid(self, form):
        """
        Метод срабатывает после того как форма валидна
        :param form:
        :return:
        """
        #self.request.user - текущий пользователь
        form.instance.user = self.request.user
        return super().form_valid(form)
class GoodUpdateView(UpdateView):
    #fields = '__all__'
    fields = ('name',)
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_create.html'
class GoodDeleteView(DeleteView):
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_delete_confirm.html'
