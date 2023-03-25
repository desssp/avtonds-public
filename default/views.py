from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import Http404, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Offer, Request, CarMark, CarModel
from .serializers import CarModelSerializer, RequestSerializer, OfferSerializer


class OfferListView(ListView):
    queryset = Offer.objects.all()


@staff_member_required
def admin_offer_detail(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    return render(request,
                  'admin/offers/offer/detail.html',
                  {'offer': offer})


@staff_member_required
def admin_request_detail(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    return render(request,
                  'admin/requests/request/detail.html',
                  {'request': req})


@staff_member_required
def admin_offer_requests_matches(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id)
    try:
        qs = Request.objects.filter(car_mark=offer.car_mark, car_model=offer.car_model)
    except Request.DoesNotExist:
        raise Http404(
            "No matches the given query."
        )
    return render(request,
                  'admin/offers/offer/requests_matches.html',
                  {
                      'offer': offer,
                      'request_set': qs,
                      'is_admin': request.user.is_superuser
                  })


@staff_member_required
def admin_request_offers_matches(request, request_id):
    req = get_object_or_404(Request, id=request_id)
    try:
        qs = Offer.objects.filter(car_mark=req.car_mark, car_model=req.car_model)
    except Offer.DoesNotExist:
        raise Http404(
            "No matches the given query."
        )
    return render(request,
                  'admin/requests/request/offers_matches.html',
                  {
                      'request': req,
                      'offer_set': qs,
                      'is_admin': request.user.is_superuser
                  })


def base(request):
    try:
        request_set = Request.objects.all().select_related('car_mark', 'car_model')
        offer_set = Offer.objects.all().select_related('car_mark', 'car_model')
        car_mark_set = request_set.values(
            'car_mark_id',
            'car_mark__name'
        ).union(
            offer_set.values(
                'car_mark_id',
                'car_mark__name'
            )
        )
    except Offer.DoesNotExist or Request.DoesNotExist:
        raise Http404(
            "No matches the given query."
        )
    return render(request,
                  'main/base.html',
                  {
                      'request_set': request_set,
                      'offer_set': offer_set,
                      'car_mark_set': car_mark_set,
                      'is_admin': request.user.is_superuser
                  })


# @api_view(['GET'])
@csrf_exempt
def car_mark_models_list(request, car_mark_id):
    if request.method == 'GET':
        request_set = Request.objects.filter(car_mark_id=car_mark_id)
        offer_set = Offer.objects.filter(car_mark_id=car_mark_id)
        car_model_id_set = request_set.values('car_model_id').union(offer_set.values('car_model_id'))
        car_models = CarModel.objects.filter(id__in=car_model_id_set.values('car_model_id'))
        serializer = CarModelSerializer(car_models, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    else:
        return Http404("Not found")


@csrf_exempt
def request_list(request):
    if request.method == 'GET':
        car_mark_id = int(request.GET.get('car_mark_id'))
        car_model_id = request.GET.get('car_model_id')
        if car_model_id:
            car_model_id = int(car_model_id)
            request_set = Request.objects.filter(
                car_mark_id=car_mark_id,
                car_model_id=car_model_id
            ).select_related(
                'car_mark',
                'car_model',
                'status',
                'user'
            )
        else:
            request_set = Request.objects.filter(
                car_mark_id=car_mark_id
            ).select_related(
                'car_mark',
                'car_model',
                'status',
                'user'
            )
        if request_set:
            serializer = RequestSerializer(request_set, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    return Http404("Not found")


@csrf_exempt
def offer_list(request):
    if request.method == 'GET':
        car_mark_id = int(request.GET.get('car_mark_id'))
        car_model_id = request.GET.get('car_model_id')
        if car_model_id:
            car_model_id = int(car_model_id)
            offer_set = Offer.objects.filter(
                car_mark_id=car_mark_id,
                car_model_id=car_model_id
            ).select_related(
                'car_mark',
                'car_model',
                'status',
                'user'
            )
        else:
            offer_set = Offer.objects.filter(
                car_mark_id=car_mark_id
            ).select_related(
                'car_mark',
                'car_model',
                'status',
                'user'
            )
        if offer_set:
            serializer = OfferSerializer(offer_set, many=True)
            return JsonResponse(serializer.data, status=200, safe=False)
        else:
            return JsonResponse([], status=200, safe=False)
    return Http404("Not found")


def index(request):
    return render(request, 'example/index.html', {})
