# ViewSets define the view behavior.
from rest_framework import routers, serializers, viewsets
from .models import Good, Merchandise
from usersapp.models import BlogUser
from .serializer import GoodSerializer, UsersSerializer, MerchSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import ReadOnly, IsAuthor
class GoodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & ReadOnly]
    queryset = Good.objects.all()
    serializer_class = GoodSerializer
class UsersVeiwSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser & ReadOnly]
    queryset = BlogUser.objects.all()
    serializer_class = UsersSerializer

class MerchVeiwSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated & ReadOnly]
    queryset = Merchandise.objects.select_related('user').order_by('name').values('good', 'name','imageUrl', 'priceBefore','priceAfter', 'amount',
                  'discount', 'market_name',).distinct()
    serializer_class = MerchSerializer