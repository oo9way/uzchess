from news.serializers import NewsSerializer
from rest_framework.generics import ListCreateAPIView
from news.models import News
from news.permissions import DefaultMethodsPermission


class NewsAPIView(ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [DefaultMethodsPermission]
    

