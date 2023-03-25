"""Default URL Configuration"""
from django.contrib import admin
# from django.template.defaulttags import url
from django.urls import path, re_path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'default'

urlpatterns = [
    path('', views.base, name='base'),
    path('api/car_mark_models/<int:car_mark_id>/', views.car_mark_models_list, name='car_mark_models_list'),
    path('api/request_list/', views.request_list, name='request_list'),
    path('api/offer_list/', views.offer_list, name='offer_list'),
    # path('admin/offer/<int:offer_id>/', views.admin_offer_detail, name='admin_offer_detail'),
    path('admin/offer/matches/<int:offer_id>/', views.admin_offer_requests_matches, name='admin_offer_requests_matches'),
    # path('admin/request/<int:request_id>/', views.admin_request_detail, name='admin_request_detail'),
    path('admin/request/matches/<int:request_id>/', views.admin_request_offers_matches, name='admin_request_offers_matches'),
]
