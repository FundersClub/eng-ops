from django.contrib import admin

from operations.decorators import is_boolean

from repositories.models import Repository


@admin.register(Repository)
class RepositoryAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'name',
        'private',
    ]
    list_display = [
        'name',
        'public',
    ]
    readonly_fields = [
        'id',
        'name',
        'private',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @is_boolean
    def public(self, obj):
        return not obj.private
