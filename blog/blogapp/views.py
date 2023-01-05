from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good, Merchandise
from .forms import ContactForm,RequestForm
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from edadeal import ED
# Create your views here.
"""def main_view(request):
    merch = Merchandise.objects.all()
    return render(request, 'blogapp/index.html', context={'merch': merch})

def post(request, id):
    merch = get_object_or_404(Merchandise, id=id)
    return render(request, 'blogapp/merch.html', context={'merch': merch})"""
def send_merch(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Получить данные из формы
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            merch = Merchandise.objects.all()
            list_result = [entry.name+' в '+entry.market_name for entry in merch]  # converts QuerySet into Python list
            myString = '\n'.join(list_result)
            send_mail(
                'Contact message',
                f'{name}, сообщаю, что {message}\nНе забудь купить:\n{myString}',
                'from@example.com',
                [email],
                fail_silently=True,
            )
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blogapp/send.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'blogapp/send.html', context={'form': form})
class MainListView(ListView):
    model = Merchandise
    template_name = 'blogapp/index.html'
    context_object_name = 'merch'
class MainDetailView(DetailView):
    model = Merchandise
    template_name = 'blogapp/merch.html'
    context_object_name = 'merch'
class MerchCreateView(FormView):
    form_class = RequestForm
    success_url = reverse_lazy('blog:index')
    template_name = 'blogapp/request.html'
    def form_valid(self, form):
        markets = form.cleaned_data['favorite_markets']
        Merchandise.objects.all().delete()
        for market in markets:
            edmarket = ED(CITY="moskva", SHOP=market)  # создаем экземпляр класса
            edmarket.load_goods_from_base()
            edmarket.get_df_discount()  # запрашиваем список товаров со скидками с сайта
            edmarket.search_and_refrash()  # сопоставляем искомые товары с перечнем скидок и сохраняем в базу
        return super().form_valid(form)
class GoodListView(ListView):
    model = Good
    template_name = 'blogapp/good_list.html'

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
    fields = '__all__'
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_create.html'
class GoodUpdateView(UpdateView):
    fields = '__all__'
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_create.html'
class GoodDeleteView(DeleteView):
    model = Good
    success_url = reverse_lazy('blog:good_list')
    template_name = 'blogapp/good_delete_confirm.html'
