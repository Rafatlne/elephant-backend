from dateutil import parser
from django.db import transaction
from django.utils import timezone
from django_rq import get_queue

from api.async_services.services.author_api_execution import execute_author_api
from api.social_media.models import (
    Author,
    AuthorSocialPlatform,
    AuthorSocialMediaContent,
    AuthorSocialMediaContentMedia,
    AuthorSocialMediaStats,
    SocialMediaPlatform,
)
from datetime import datetime


def process_author_social_content_json_entries(json_entries):
    results = []
    with transaction.atomic():
        for json_data in json_entries:
            # Extract data from JSON
            author_data = json_data["author"]
            content_data = json_data
            platform_data = json_data["origin_details"]

            # Get or create Author
            author, created = Author.objects.get_or_create(
                unique_id=author_data["id"],
                defaults={
                    "username": author_data["username"],
                    "unique_id": author_data["id"],
                },
            )

            # Get or create AuthorSocialPlatform
            platform, created = SocialMediaPlatform.objects.get_or_create(
                name=platform_data["origin_platform"]
            )
            created_at_string = content_data['creation_info']['created_at']
            timestamp_string = content_data['creation_info']['timestamp']
            parsed_created_at = parser.isoparse(created_at_string)
            parsed_timestamp = parser.isoparse(timestamp_string)
            # Format the parsed timestamps
            formatted_created_at = parsed_created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            formatted_timestamp = parsed_timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            # Create or update AuthorSocialMediaContent
            content, created = AuthorSocialMediaContent.objects.update_or_create(
                author=author,
                unique_id=content_data["unique_id"],
                defaults={
                    "unique_uuid": content_data["unique_uuid"],
                    "origin_unique_id": content_data["origin_unique_id"],
                    "creation_info_created_at": formatted_created_at,
                    "creation_info_timestamp": formatted_timestamp,
                    "main_text": content_data["context"]["main_text"],
                    "token_count": content_data["context"]["token_count"],
                    "char_count": content_data["context"]["char_count"],
                    "tag_count": content_data["context"]["tag_count"],
                    "origin_platform": platform,
                    "origin_url": content_data["origin_details"]["origin_url"],
                },
            )

            # Create or update AuthorSocialMediaContentMedia
            media, created = AuthorSocialMediaContentMedia.objects.update_or_create(
                author=author,
                media_url=content_data["media"]["urls"][0],
                defaults={
                    "media_type": content_data["media"]["media_type"],
                    "content": content,
                },
            )

            # Create or update AuthorSocialMediaStats
            stats, created = AuthorSocialMediaStats.objects.update_or_create(
                content=content,
                defaults={
                    "likes_id": content_data["stats"]["digg_counts"]["likes"]["id"],
                    "likes_count": content_data["stats"]["digg_counts"]["likes"][
                        "count"
                    ],
                    "views_id": content_data["stats"]["digg_counts"]["views"]["id"],
                    "views_count": content_data["stats"]["digg_counts"]["views"][
                        "count"
                    ],
                    "comments_id": content_data["stats"]["digg_counts"]["comments"][
                        "id"
                    ],
                    "comments_count": content_data["stats"]["digg_counts"]["comments"][
                        "count"
                    ],
                },
            )

            # Append results for each entry
            results.append(
                {
                    "author_created": created,
                    "platform_created": created,
                    "content_created": created,
                    "media_created": created,
                    "stats_created": created,
                }
            )

        return results


def process_author_json(json_data):
    # Extract data from JSON
    author_data = json_data[0]
    platform_data = author_data["info"]

    # Get or update Author
    author, created = Author.objects.get_or_create(
        unique_id=author_data["unique_id"],
        defaults={
            "username": author_data["username"],
            "unique_uuid": author_data["unique_uuid"],
            "origin_unique_id": author_data["origin_unique_id"],
        },
    )

    if not created:
        # Update existing Author data if needed
        author.username = author_data["username"]
        # Add other fields to update as needed
        author.save()

    # Get or update AuthorSocialPlatform
    platform, created = SocialMediaPlatform.objects.get_or_create(
        name=platform_data["platform"]
    )
    author_platform, created = AuthorSocialPlatform.objects.get_or_create(
        author=author,
        name=platform_data["name"],
        platform=platform,
        defaults={
            "profile_text": author_data["texts"]["profile_text"],
            "avatar_url": author_data["avatar"]["urls"][0],
            "followers_id": author_data["stats"]["digg_count"]["followers"]["id"],
            "followers_count": author_data["stats"]["digg_count"]["followers"][
                "count"
            ],
        },
    )

    if not created:
        # Update existing AuthorSocialPlatform data if needed
        author_platform.profile_text = author_data["texts"]["profile_text"]
        # Add other fields to update as needed
        author_platform.save()

    # Return any relevant data or status if needed
    return {
        "author_created_or_updated": not created,
        "platform_created_or_updated": not created,
    }
