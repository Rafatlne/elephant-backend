from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


SchemaView = get_schema_view(
    openapi.Info(
        title=settings.API_BROWSER_HEADER,
        default_version="v1",
        description="API Schema endpoint to generate swagger api documentation",
        terms_of_service="Ashik Rafat",
        contact=openapi.Contact(email="dev.rafath@gmail.com"),
        license=openapi.License(name="All rights reserved."),
    ),
    public=True,
    permission_classes=[AllowAny],
)


def ready(request):
    return HttpResponse("ready")


router = DefaultRouter()

urlpatterns = [
    path("-/ready", ready),
    path("api/admin/", admin.site.urls),
    path("api/social-media/", include("api.social_media.urls")),
    path("api/user/", include("api.user.urls")),
    path("api", include(router.urls)),
    path('api/django-rq/', include('django_rq.urls')),
]

if settings.DJANGO_ENV != "production":
    urlpatterns += [
        re_path(
            r"^api(?P<format>\.json|\.yaml)/$",
            SchemaView.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "api/swagger",
            SchemaView.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
