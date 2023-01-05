
from django.urls import path
from blogapp import views
app_name = 'blogapp'
urlpatterns = [
    path('', views.main_view, name='index'),
    path('merch/<int:id>/', views.post, name='merch'),
    path('goods', views.goods, name='goods'),
    path('send', views.send_merch, name='send'),
    path('request', views.request_merch, name='request'),

    path('good-list', views.GoodListView.as_view(), name='good_list'),
    path('good-ditail/<int:pk>/', views.GoodDetailView.as_view(), name='good_detail'),
    path('good-create', views.GoodCreateView.as_view(), name='good_create'),
    path('good-update/<int:pk>/', views.GoodUpdateView.as_view(), name='good_update'),
    path('good-delete/<int:pk>/', views.GoodDeleteView.as_view(), name='good_delete'),

]