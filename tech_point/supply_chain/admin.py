from django.contrib import admin

from supply_chain import models


class SupplyChainLinkInline(admin.TabularInline):
    model = models.SupplyChainLink
    extra = 0


class SupplyChainAdmin(admin.ModelAdmin):
    inlines = [SupplyChainLinkInline]


class SupplyChainLinkAdmin(admin.ModelAdmin):
    actions = ["clear_debt"]
    list_display = ["id", "supply_chain", "level", "supplier", "parent"]
    list_display_links = ["id", "supply_chain", "supplier", "parent"]
    list_filter = ["supplier__address__city"]

    @admin.action
    def clear_debt(self, request, queryset):
        queryset.update(debt=0)


admin.site.register(models.Address)
admin.site.register(models.Supplier)
admin.site.register(models.SupplyChain, SupplyChainAdmin)
admin.site.register(models.SupplyChainLink, SupplyChainLinkAdmin)
admin.site.register(models.Product)
