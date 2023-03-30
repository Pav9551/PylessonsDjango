from rest_framework import routers, serializers, viewsets
from .models import Good
from usersapp.models import BlogUser
# Serializers define the API representation.
class BlogUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BlogUser
        fields =  ['username']
class GoodSerializer(serializers.HyperlinkedModelSerializer):
    user = BlogUserSerializer(read_only=True)
    class Meta:
        model = Good
        fields = ['name', 'user']