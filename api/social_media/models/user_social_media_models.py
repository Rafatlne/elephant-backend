from django.db import models


class SocialMediaPlatform(models.Model):
    INSTAGRAM = 'Instagram'
    TIKTOK = 'TikTok'

    PLATFORM_CHOICES = [
        (INSTAGRAM, 'Instagram'),
        (TIKTOK, 'TikTok'),
    ]

    name = models.CharField(max_length=255, choices=PLATFORM_CHOICES)


class Author(models.Model):
    username = models.CharField(max_length=255)
    unique_id = models.IntegerField()
    unique_uuid = models.CharField(max_length=36)
    origin_unique_id = models.CharField(max_length=255)


class AuthorSocialPlatform(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="social_media_platforms"
    )
    name = models.CharField(max_length=255)
    platform = models.ForeignKey(
        SocialMediaPlatform,
        on_delete=models.CASCADE,
        related_name="author_social_platforms",
    )
    profile_text = models.TextField()
    avatar_url = models.URLField()
    followers_id = models.IntegerField()
    followers_count = models.IntegerField()


class AuthorSocialMediaContent(models.Model):
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="social_media_contents"
    )
    unique_id = models.IntegerField()
    unique_uuid = models.CharField(max_length=36)
    origin_unique_id = models.CharField(max_length=255)
    creation_info_created_at = models.DateTimeField()
    creation_info_timestamp = models.DateTimeField()
    main_text = models.TextField()
    token_count = models.IntegerField()
    char_count = models.IntegerField()
    tag_count = models.IntegerField()
    origin_platform = models.ForeignKey(
        SocialMediaPlatform,
        on_delete=models.CASCADE,
        related_name="content_origin_platforms",
    )
    origin_url = models.URLField()


class AuthorSocialMediaContentMedia(models.Model):
    media_url = models.URLField()
    media_type = models.CharField(max_length=50)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="media_contents"
    )
    content = models.ForeignKey(
        AuthorSocialMediaContent, on_delete=models.CASCADE, related_name="media_content"
    )


class AuthorSocialMediaStats(models.Model):
    likes_id = models.IntegerField()
    likes_count = models.IntegerField()
    views_id = models.IntegerField()
    views_count = models.IntegerField()
    comments_id = models.IntegerField()
    comments_count = models.IntegerField()
    content = models.ForeignKey(
        AuthorSocialMediaContent, on_delete=models.CASCADE, related_name="content_stats"
    )
