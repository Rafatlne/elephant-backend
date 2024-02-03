# serializers.py
from rest_framework import serializers

from api.social_media.models import Author, AuthorSocialPlatform, AuthorSocialMediaContent, \
    AuthorSocialMediaContentMedia, AuthorSocialMediaStats


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class AuthorSocialPlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSocialPlatform
        fields = '__all__'


class AuthorSocialMediaContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSocialMediaContent
        fields = '__all__'


class AuthorSocialMediaContentMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSocialMediaContentMedia
        fields = '__all__'


class AuthorSocialMediaStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorSocialMediaStats
        fields = '__all__'


class StatisticsSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    total_likes = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_comments = serializers.IntegerField()
