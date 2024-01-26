from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Work
from .serializers import WorkSerializer

class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer