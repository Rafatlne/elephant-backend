from rest_framework import serializers


class CreatorSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    followers = serializers.IntegerField()
    username = serializers.CharField()
    external_id = serializers.CharField()
    external_url = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    platform = serializers.CharField()
    profile_text = serializers.CharField()
    profile_picture_url = serializers.URLField()
    follower_count = serializers.CharField()

class ContentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    uuid = serializers.CharField()
    account = serializers.IntegerField()
    external_id = serializers.CharField()
    external_url = serializers.CharField()
    timestamp = serializers.DateTimeField()
    title = serializers.CharField()
    text = serializers.CharField()
    thumbnail_url = serializers.URLField()
    content_platform = serializers.CharField()
    content_type = serializers.CharField(allow_null=True)
    content_form = serializers.CharField()
    likes = serializers.IntegerField()
    comments = serializers.IntegerField()
    views = serializers.IntegerField()
    shares = serializers.IntegerField()
    total_engagement = serializers.IntegerField()
    engagement_of_views = serializers.FloatField()
    engagement_of_followers = serializers.FloatField()

class ListContentSerializer(serializers.Serializer):
    creator = CreatorSerializer()
    content = ContentSerializer()
