from django.http import HttpResponse
from django.template import loader

from work.models import Work

def index(request):
    works = Work.objects.all()

    template = loader.get_template('event/index.html')
    context = { 'works': works }
    return HttpResponse(template.render(context, request))