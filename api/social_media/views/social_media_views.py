# # views.py
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
#
# from api.social_media.services.social_media_content_service import process_author_social_content_json_entries, \
#     process_author_json
# from api.social_media.serializers.social_media_serializers import AuthorSerializer, AuthorSocialPlatformSerializer
#
#
# class ProcessFirstJsonView(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def post(self, request, *args, **kwargs):
#         json_data = request.data
#
#         try:
#             results = process_author_social_content_json_entries(json_data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(results, status=status.HTTP_200_OK)
#
#
# class ProcessSecondJsonView(APIView):
#     authentication_classes = []
#     permission_classes = []
#
#     def post(self, request, *args, **kwargs):
#         json_data = request.data
#
#         try:
#             result = process_author_json(json_data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(result, status=status.HTTP_200_OK)
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
from ..serializers.social_media_serializers import AuthorSocialMediaContentSerializer, StatisticsSerializer


class MergedContentView(ModelViewSet):
    permission_classes = []
    authentication_classes = []
    pagination_class = PageNumberPagination
    queryset = AuthorSocialMediaContent.objects.all()
    serializer_class = AuthorSocialMediaContentSerializer
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

                if author_data:
                    stats_data = AuthorSocialMediaStats.objects.filter(content_id=content_data['id']).values().first()

                    # Retrieve AuthorSocialPlatform information
                    platform_data = AuthorSocialPlatform.objects.filter(
                        id=content_data['origin_platform']).values().first()

                    merged_data.append({
                        'content': content_data,
                        'creator': author_data[0],
                        'stats_data': stats_data,
                        'platform_data': platform_data,
                    })
            return self.get_paginated_response(merged_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserStatisticsPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed


class StatisticsView(APIView, LimitOffsetPagination):
    authentication_classes = []  # No authentication
    permission_classes = []  # No permission checks

    # pagination_class = UserStatisticsPagination

    def get(self, request, *args, **kwargs):
        # Get all authors
        authors = Author.objects.all()

        # Calculate aggregate statistics per user
        user_statistics = []
        for author in authors:
            user_stats = AuthorSocialMediaStats.objects.filter(content__author=author)

            total_likes = user_stats.aggregate(Sum('likes_count'))['likes_count__sum']
            total_views = user_stats.aggregate(Sum('views_count'))['views_count__sum']
            total_comments = user_stats.aggregate(Sum('comments_count'))['comments_count__sum']

            user_statistics.append({
                'user_id': author.id,
                'total_likes': total_likes,
                'total_views': total_views,
                'total_comments': total_comments,
            })

        # Paginate the results
        page = self.paginate_queryset(user_statistics, request)
        if page is not None:
            serializer = StatisticsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # Create and return the response
        serializer = StatisticsSerializer(user_statistics, many=True)
        return Response(serializer.data)
