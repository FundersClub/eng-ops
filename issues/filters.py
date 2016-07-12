from django.contrib import admin

from pipelines.models import Pipeline
from repositories.models import Repository


class PipelineFilter(admin.SimpleListFilter):
    title = 'pipeline'
    parameter_name = 'pipeline'

    def lookups(self, request, model_admin):
        return [
            (pipeline.name, pipeline.name) for pipeline in Pipeline.objects.all()
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(pipeline__name=self.value())


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


class RequestsFilter(admin.SimpleListFilter):
    title = 'requests'
    parameter_name = 'requests'

    def lookups(self, request, model_admin):
        return [
            ('yes', 'Yes'),
            ('no', 'No'),
        ]

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset

        return queryset.filter(requests__isnull=self.value() == 'no')
