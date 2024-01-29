from django.http import HttpResponse
from django.template import loader

from work.models import Work
from coupon.models import Coupon

def index(request):
    works = Work.objects.all()
    coupon = Coupon.objects.get(pk=1)

    template = loader.get_template('event/index.html')
    context = { 'works': works, 'couponCount' : coupon.count}
    return HttpResponse(template.render(context, request))