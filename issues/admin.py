from django.contrib import admin

from operations.decorators import short_description

from issues.filters import (
    PipelineFilter,
    RepositoryFilter,
)
from issues.models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'number',
        'repository',
        'title',
        'creater',
        'assignee',
        'created_at',
        'closed_at',
        'labels',
        'body',
    ]
    list_filter = [
        PipelineFilter,
        RepositoryFilter,
    ]
    list_display = [
        'number',
        'repository',
        'pipeline',
        'title',
        'estimate_display',
        'created_at',
    ]
    readonly_fields = [
        'id',
        'number',
        'repository',
        'title',
        'creater',
        'assignee',
        'created_at',
        'closed_at',
        'labels',
        'body',
    ]

    @short_description('Estimate')
    def estimate_display(self, obj):
        return obj.estimate if obj.estimate != 0 else '-'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
