from django.contrib import admin

from operations.decorators import short_description

from user_management.models import GithubUser


@admin.register(GithubUser)
class GithubUserAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'logins',
        'slack_username',
    ]
    list_display = [
        'id',
        'logins_display',
        'slack_username',
    ]
    readonly_fields = [
        'id',
    ]

    @short_description('Logins')
    def logins_display(self, obj):
        return ', '.join(obj.logins)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
