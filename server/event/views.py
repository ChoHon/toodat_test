from django.http import HttpResponse
from django.template import loader

from work.models import Work
from coupon.models import Coupon

def index(request):
    COUPON_ID = 1
    coupon = Coupon.objects.filter(id=COUPON_ID).first()
    works = Work.objects.all()
    
    eventState = True if coupon is not None else False    
    eventState = False if eventState and coupon.count <= 0 else eventState

    template = loader.get_template('event/index.html')
    context = { 'works': works, 'coupon' : coupon, 'eventState' : eventState }
    return HttpResponse(template.render(context, request))