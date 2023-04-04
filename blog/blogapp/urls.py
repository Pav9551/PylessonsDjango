
from django.urls import path
from blogapp import views
app_name = 'blogapp'
urlpatterns = [
    path('', views.MainListView.as_view(), name='index'),
    path('merch/<int:pk>/', views.MainDetailView.as_view(), name='merch'),
    path('send', views.SendFormView.as_view(), name='send'),
    path('request', views.MerchFormView.as_view(), name='request'),
    path('good-list', views.GoodListView.as_view(), name='good_list'),
    path('good-ditail/<int:pk>/', views.GoodDetailView.as_view(), name='good_detail'),
    path('good-create', views.GoodCreateView.as_view(), name='good_create'),
    path('good-update/<int:pk>/', views.GoodUpdateView.as_view(), name='good_update'),
    path('good-delete/<int:pk>/', views.GoodDeleteView.as_view(), name='good_delete'),
    path('max_discount', views.DiscountDetailView.as_view(), name='max_discount'),
    path('coincidence-list', views.CoincidenceListView.as_view(), name='coincidence_list'),
    path('coincidence-ditail/<int:pk>/', views.CoincidenceDetailView.as_view(), name='coincidence_detail'),
    path('post-ditail/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

]