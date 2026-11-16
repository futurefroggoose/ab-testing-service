from django.contrib import admin
from .models import Experiment, Variant, StatisticalResult


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 2


class StatisticalResultInline(admin.StackedInline):
    model = StatisticalResult
    can_delete = False
    readonly_fields = ('calculated_at',)


@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'baseline_conversion', 'mde', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'description')
    inlines = [VariantInline, StatisticalResultInline]


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ('name', 'experiment', 'visitors', 'conversions', 'is_control')
    list_filter = ('is_control',)
    search_fields = ('name', 'experiment__name')


@admin.register(StatisticalResult)
class StatisticalResultAdmin(admin.ModelAdmin):
    list_display = ('experiment', 'p_value', 'is_significant', 'sample_size_per_variant', 'calculated_at')
    list_filter = ('is_significant',)


from django.contrib import admin

# Register your models here.
