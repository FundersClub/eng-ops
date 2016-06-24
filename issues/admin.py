from django.contrib import admin

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
    list_display = [
        'number',
        'repository',
        'title',
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

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
