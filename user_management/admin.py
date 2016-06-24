from django.contrib import admin

from user_management.models import GithubUser


@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'login',
    ]
    list_display = [
        'id',
        'login',
    ]
    readonly_fields = [
        'id',
        'login',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
