"""Default URL Configuration"""
from django.contrib import admin
# from django.template.defaulttags import url
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'default'

urlpatterns = [
    # path('admin/offer/<int:offer_id>/', views.admin_offer_detail, name='admin_offer_detail'),
    path('admin/offer/matches/<int:offer_id>/', views.admin_offer_requests_matches, name='admin_offer_requests_matches'),
    # path('admin/request/<int:request_id>/', views.admin_request_detail, name='admin_request_detail'),
    path('admin/request/matches/<int:request_id>/', views.admin_request_offers_matches, name='admin_request_offers_matches'),
]
