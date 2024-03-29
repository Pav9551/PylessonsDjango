from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good, Merchandise, Coincidence, Post_for_Coincidence, create_new_post
from .forms import ContactForm,RequestForm, CreateForm, PostForm
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
#from edadeal import ED
from usersapp.models import BlogUser
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db.models import Count
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
        merch = Merchandise.objects.filter(user = user[0])
        return merch
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
        merch = Merchandise.objects.filter(user = self.request.user)
        list_result = [entry.name + ' в ' + entry.market_name for entry in merch]  # converts QuerySet into Python list
        myString = '\n'.join(list_result)
        send_mail(
            'Это список продуктов со скидками',
            f'{name}, сообщаю, что {message}\nНе забудь купить:\n{myString}',
            'pav9551@yandex.ru',
            [email],
            fail_silently=False,
        )

        #send_mail('Django mail', 'This e-mail was sent with Django.',
                  #'testnotion45@gmail.com', ['pav9551@yandex.ru'], fail_silently=False)

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
class CoincidenceListView(ListView):
    model = Coincidence
    template_name = 'blogapp/coincidence_list.html'
    def get_queryset(self):
        user = BlogUser.objects.filter(username=self.request.user)
        if len(user) == 0:
            user = BlogUser.objects.filter(is_superuser = True)
        #queryset = Coincidence.objects.filter(users__in = user)
        queryset = Coincidence.objects.annotate(num_related=Count('users')).filter(users__in = user, num_related__gt = 1)

        #queryset = Coincidence.objects.filter(users__in=user)
        #queryset = Coincidence.objects.filter(users__in=user[0])
        return queryset
class CoincidenceDetailView(DetailView):
    model = Coincidence
    template_name = 'blogapp/coincidence_detail.html'
    context_object_name = 'merch'

class PostListDetailView(DetailView):
    model = Coincidence
    template_name = 'blogapp/post_list.html'
    context_object_name = 'good'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get the coincidence object for this view
        coincidence = self.get_object()
        # order the posts by their creation time, from newest to oldest
        ordered_posts = coincidence.posts.order_by('create')
        context['ordered_posts'] = ordered_posts
        return context
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
        if (str(self.request.user) == 'AnonymousUser'):
            user = BlogUser.objects.filter(is_superuser=True)
            merch = Merchandise.objects.filter(user = user[0]).filter(good = good)
        else:
            merch = Merchandise.objects.filter(user=self.request.user).filter(good=good)
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
        #return HttpResponse("Invalid data")

        #self.request.user - текущий пользователь
        user = self.request.user
        form.instance.user = user
        name = form.cleaned_data['name']
        if (Good().is_unique(name, user)):
            return super().form_valid(form)
        else:
            return redirect('/good-list')


class GoodUpdateView(UpdateView):
    #fields = '__all__'
    fields = ('name',)
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_create.html'
    def get_form_kwargs(self):
        # Add the variable to the form kwargs
        kwargs = super().get_form_kwargs()
        if 'data' in kwargs:
            oldname = kwargs['instance']
            newname = kwargs['data']['name']
            username = self.request.user
            Good().del_good(oldname, username)
            Good().is_unique(newname, username)
        return kwargs
class GoodDeleteView(DeleteView):
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_delete_confirm.html'
    def get(self, request, *args, **kwargs):
        """
        Метод обработки get запроса
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        # Call the parent class's delete method to delete the object and get the HTTP response
        self.good_id = kwargs['pk']
        good = get_object_or_404(Good, pk=self.good_id)
        print(f'{good.user}.{good.name}')
        Good().del_good(good.name, good.user)
        response = super().delete(request, *args, **kwargs)
        # Do any additional processing here, such as sending a confirmation message to the user
        # Return the HTTP response
        return response
class DiscountDetailView(ListView):
    model = Merchandise
    template_name = 'blogapp/max_discount.html'
    context_object_name = 'merch'
    def get_queryset(self):
        return Merchandise().get_max_discount()
    def get_context_data(self, *args, **kwargs):
        """
        Отвечает за передачу параметров в контекст
        :param args:
        :param kwargs:
        :return:
        """
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'товары дня'
        # context['max_disc'] = Merchandise().get_max_discount()
        max_disc = Merchandise().get_max_discount_cached
        context['max_disc'] = max_disc
        for item in max_disc:
            print(item)
        return context
def create_post(request):
    if request.method == 'GET':
        form = PostForm()
        return render(request, 'blogapp/post_create.html', context={'form': form})
class PostCreateView(CreateView):
    form_class = PostForm
    #fields = ('name',)
    model = Post_for_Coincidence
    success_url = reverse_lazy('blog:coincidence_list')
    template_name = 'blogapp/post_create.html'
    #exclude = ('user',)

    def form_valid(self, form):
        """
        Метод срабатывает после того как форма валидна
        :param form:
        :return:
        """
        #return HttpResponse("Invalid data")

        #self.request.user - текущий пользователь
        user = self.request.user
        #list_сoincid = form.cleaned_data['сoincid']
        name = form.cleaned_data['name']
        text = form.cleaned_data['text']
        #print(name)
        #print(str(self.request.path)[13:-1])#костыль
        number = int(str(self.request.path)[13:-1])
        form.instance.user = user
        redir_url = '/post-list/' + str(self.request.path)[13:-1]+'/'
        create_new_post(name,text,user,number)
        return redirect(redir_url)



