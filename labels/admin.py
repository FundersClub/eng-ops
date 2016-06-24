from django.contrib import admin

from labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'repositories',
    ]
    list_display = [
        'name',
        'repository_display',
    ]
    readonly_fields = [
        'name',
        'repositories',
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def repository_display(self, obj):
        return ', '.join(
            repo.name for repo in obj.repositories.all()
        )
