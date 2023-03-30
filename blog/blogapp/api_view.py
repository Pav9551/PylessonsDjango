# ViewSets define the view behavior.
from rest_framework import routers, serializers, viewsets
from .models import Good
from .serializer import GoodSerializer
class GoodViewSet(viewsets.ModelViewSet):
    queryset = Good.objects.all()
    serializer_class = GoodSerializer