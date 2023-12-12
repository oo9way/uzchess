from django.urls import path
from news.views import NewsAPIView


urlpatterns = [
    path('', NewsAPIView.as_view(), name='news-list'),
]
