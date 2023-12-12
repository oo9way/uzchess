from rest_framework import serializers
from news.models import News, PageViews

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'