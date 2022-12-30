
from django.urls import path
from blogapp import views
app_name = 'blogapp'
urlpatterns = [
    path('', views.main_view, name='index'),
    path('merch/<int:id>/', views.post, name='merch'),
    path('goods', views.goods, name='goods'),
    path('send', views.send_merch, name='send'),
    path('request', views.request_merch, name='request'),



]