from django.contrib import admin

from api.models import GithubRequest


@admin.register(GithubRequest)
class GithubRequestAdmin(admin.ModelAdmin):
    fields = [
        'time',
        'event',
        'handled',
        'method',
        'body',
    ]
    list_display = [
        'time',
        'event',
        'issue',
        'handled',
        'method',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
