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


class AuthorSocialMediaContentSerializerv2(serializers.ModelSerializer):
    id = serializers.CharField(source='unique_id')
    uuid = serializers.CharField(source='unique_uuid')
    external_url = serializers.CharField(source='origin_url')
    timestamp = serializers.DateTimeField(source='creation_info_timestamp')
    title = serializers.CharField(source='main_text')
    text = serializers.CharField(source='main_text')
    external_id = serializers.CharField(default='n/a')
    account = serializers.CharField(default='n/a')
    content_platform = serializers.CharField(default='instagram')
    content_type = serializers.CharField(default='n/a')
    content_from = serializers.CharField(default="image")
    likes = serializers.CharField(default="1000")
    comments = serializers.CharField(default="12023")
    views = serializers.CharField(default="23399")
    shares = serializers.CharField(default="0")
    total_engagement = serializers.CharField(default="222211")
    engagement_of_views = serializers.CharField(default="333440")
    engagement_of_followers = serializers.CharField(default="222220")

    class Meta:
        model = AuthorSocialMediaContent
        fields = '__all__'
