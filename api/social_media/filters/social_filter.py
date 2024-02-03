# filters.py
from django_filters import rest_framework as filters

from api.social_media.models import AuthorSocialMediaContent


class MergedContentFilter(filters.FilterSet):
    author_username = filters.CharFilter(field_name='author__username', lookup_expr='exact')
    origin_platform = filters.CharFilter(field_name='origin_platform__name', lookup_expr='iexact')

    class Meta:
        model = AuthorSocialMediaContent
        fields = ['author_username', 'origin_platform']
