from django.contrib import admin


class AbstractAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
