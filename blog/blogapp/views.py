from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good, Merchandise
# Create your views here.
def main_view(request):
    merch = Merchandise.objects.all()
    return render(request, 'blogapp/index.html', context={'merch': merch})
def post(request, id):
    merch = get_object_or_404(Merchandise, id=id)
    return render(request, 'blogapp/merch.html', context={'merch': merch})