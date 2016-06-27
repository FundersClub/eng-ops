from django.contrib import admin

from repositories.models import Repository


class RepositoryFilter(admin.SimpleListFilter):
    title = 'repository'
    parameter_name = 'repository'

    def lookups(self, request, model_admin):
        return [
            (repository.name, repository.name) for repository in Repository.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(repository__name=self.value())
