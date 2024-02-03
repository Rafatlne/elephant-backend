from api.social_media.models import AuthorSocialMediaStats, AuthorSocialPlatform
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..filters.social_filter import MergedContentFilter
from ..models import Author, AuthorSocialPlatform, AuthorSocialMediaContent, AuthorSocialMediaContentMedia, \
    AuthorSocialMediaStats
from ..serializers.social_media_serializers import AuthorSocialMediaContentSerializer, StatisticsSerializer, \
    AuthorSocialMediaContentSerializerv2


class FrontendAPIView(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    pagination_class = PageNumberPagination
    queryset = AuthorSocialMediaContent.objects.all()
    serializer_class = AuthorSocialMediaContentSerializerv2
    # filter_backends = [DjangoFilterBackend]
    filterset_class = MergedContentFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            merged_data = []
            for content_data in serializer.data:
                author_data = Author.objects.filter(id=content_data['author']).values()
                authro_data = {
                    "id": author_data[0]["unique_id"],
                    "username": author_data[0]["username"],
                    "external_id": author_data[0]["username"]

                }
                if author_data:
                    stats_data = AuthorSocialMediaStats.objects.filter(content_id=content_data['id']).values().first()

                    # Retrieve AuthorSocialPlatform information
                    platform_data = AuthorSocialPlatform.objects.filter(
                        id=content_data['origin_platform']).values().first()
                    authro_data["external_url"] = ""
                    authro_data["name"] = platform_data["name"]
                    authro_data["name"] = platform_data["name"]
                    authro_data["profile_text"] = platform_data["profile_text"]
                    authro_data["profile_picture_url"] = platform_data["avatar_url"]
                    authro_data["followers_count"] = platform_data["followers_count"]


                    merged_data.append({
                        'content': content_data,
                        'author_details': author_data[0],
                        'stats_data': stats_data,
                        'platform_data': platform_data,
                        'creator': authro_data,
                    })
            return self.get_paginated_response(merged_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
