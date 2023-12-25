from django.contrib import admin

from supply_chain import models


class SupplyChainLinkInline(admin.TabularInline):
    model = models.SupplyChainLink
    readonly_fields = ("parent", "level")
    extra = 0


class SupplyChainAdmin(admin.ModelAdmin):
    inlines = [SupplyChainLinkInline]

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        if instances:
            parent = form.instance.last_link
            for instance in instances:
                if not instance.parent:
                    instance.parent = parent
                    instance.level = parent.level + 1 if parent else 0
                    parent = instance
        formset.save()


class SupplyChainLinkAdmin(admin.ModelAdmin):
    actions = ["clear_debt"]
    readonly_fields = ("parent", "level")
    list_display = ["id", "supply_chain", "level", "supplier", "parent"]
    list_display_links = ["id", "supply_chain", "supplier", "parent"]
    list_filter = ["supplier__address__city"]

    def save_form(self, request, form, change):
        instance = form.save(commit=False)
        if not instance.parent:
            parent = instance.supply_chain.last_link
            instance.parent = parent
            instance.level = parent.level + 1 if parent else 0
        return instance

    @admin.action
    def clear_debt(self, request, queryset):
        queryset.update(debt=0)


admin.site.register(models.Address)
admin.site.register(models.Supplier)
admin.site.register(models.SupplyChain, SupplyChainAdmin)
admin.site.register(models.SupplyChainLink, SupplyChainLinkAdmin)
admin.site.register(models.Product)
