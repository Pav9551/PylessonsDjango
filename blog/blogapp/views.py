from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good, Merchandise
from .forms import ContactForm,RequestForm
from django.core.mail import send_mail
from django.urls import reverse
# Create your views here.
def main_view(request):
    merch = Merchandise.objects.all()
    return render(request, 'blogapp/index.html', context={'merch': merch})
def post(request, id):
    merch = get_object_or_404(Merchandise, id=id)
    return render(request, 'blogapp/merch.html', context={'merch': merch})
def goods(request):
    goods = Good.objects.all()
    return render(request, 'blogapp/goods.html', context={'goods': goods})

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
def request_merch(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
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
            return render(request, 'blogapp/request.html', context={'form': form})
    else:
        form = RequestForm()
        return render(request, 'blogapp/request.html', context={'form': form})