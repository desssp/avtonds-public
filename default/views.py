from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Offer, Request


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
