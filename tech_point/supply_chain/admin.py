from django.contrib import admin

from supply_chain import models

admin.site.register(models.Address)
admin.site.register(models.Supplier)
admin.site.register(models.SupplyChain)
admin.site.register(models.SupplyChainLink)
admin.site.register(models.Product)
