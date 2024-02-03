from django.urls import re_path, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from api.social_media.views.social_media_views import MergedContentView, StatisticsView

# from api.social_media.views.social_media_views import ProcessFirstJsonView, ProcessSecondJsonView


router = DefaultRouter()
router.register("merged-contents", MergedContentView, basename="merged-content")

urlpatterns = [
    # path('process-first-json/', ProcessFirstJsonView.as_view(), name='process-first-json'),
    # path('process-second-json/', ProcessSecondJsonView.as_view(), name='process-second-json'),
    # path('merged-content/', MergedContentView, name='merged-content'),
path('statistics/', StatisticsView.as_view(), name='statistics'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += router.urls
