from django.shortcuts import render
from .models import Good
# Create your views here.
def main_view(request):
    posts = Good.objects.all()
    return render(request, 'blogapp/index.html')