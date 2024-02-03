# views.py
from dateutil import parser
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from api.social_media.models import AuthorSocialMediaContent, Author, SocialMediaPlatform
from api.social_media.serializers.social_media_serializers import AuthorSocialMediaContentSerializer, \
    AuthorSocialMediaContentMediaSerializer, AuthorSerializer


class SaveSocialMediaDataView(generics.ListCreateAPIView):
    queryset = AuthorSocialMediaContent.objects.all()
    serializer_class = AuthorSocialMediaContentSerializer
    authentication_classes = []  # No authentication
    permission_classes = []  # No permission checks

    def create(self, request, *args, **kwargs):
        data_list = request.data
        for data in data_list:
            user_name = data.get('user_name')
            url = data.get('content')
            post_date = data.get('post_date')
            is_video = data.get('is_video', False)
            parsed_created_at = parser.isoparse(post_date)
            # Format the parsed timestamps
            formatted_created_at = parsed_created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            # Search for Author based on user_name
            author, created = Author.objects.get_or_create(username=user_name)
            instagram = SocialMediaPlatform.objects.get(name='instagram')

            # Save post_date data to creation_info_timestamp field
            author_social_media_content_data = {
                'author': author.id,
                'creation_info_timestamp': formatted_created_at,
                'origin_url': url,
                'origin_platform': instagram.id
                # Add other necessary fields...
            }

            # Save data in AuthorSocialMediaContent
            serializer = self.serializer_class(data=author_social_media_content_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            content_instance = serializer.save()

            # Save data in AuthorSocialMediaContentMedia
            media_type = 'VIDEO' if is_video else 'PHOTO'
            media_data = {
                'author': author.id,
                'media_url': url,
                'media_type': media_type,
                'content': content_instance.id
            }

            media_serializer = AuthorSocialMediaContentMediaSerializer(data=media_data)
            media_serializer.is_valid(raise_exception=True)
            media_serializer.save()

            # Return the created data
        response_data = {
            "success": True
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Return a list of JSON objects
        response_data = [
            {
                'author': AuthorSerializer(content.author).data,
                'media_content': content,
            }
            for content in serializer.data
        ]

        return Response(response_data)

