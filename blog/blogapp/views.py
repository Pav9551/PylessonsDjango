from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from .models import Good
# Create your views here.
def main_view(request):
    good = Good.objects.all()
    return render(request, 'blogapp/index.html', context={'posts': good})
def post(request, id):
    good = get_object_or_404(Good, id=id)
    return render(request, 'blogapp/post.html', context={'post': good})