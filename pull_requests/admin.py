from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from operations.decorators import short_description

from pull_requests.models import (
    PullRequest,
)

@admin.register(PullRequest)
class PullRequestAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'number',
        'repository',
        'title',
        'user',
        'assignees',
        'created_at',
        'merged_at',
        'closed_at',
        'body',
    ]
    list_display = [
        'number',
        'repository',
        'title',
        'created_at',
        'closed_at',
    ]
    readonly_fields = [
        'assignees',
        'body',
        'closed_at',
        'created_at',
        'id',
        'merged_at',
        'number',
        'repository',
        'title',
        'user',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
