from django.core.validators import MaxValueValidator
from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SupplierType(models.TextChoices):
    PLANT = "Plant"
    DISTRIBUTOR = "Distributor"
    DEALER_CENTER = "Dealer center"
    RETAIL_NETWORK = "Retail network"
    INDIVIDUAL_ENTREPRENEUR = "Individual entrepreneur"


class Address(models.Model):
    country = models.CharField()
    city = models.CharField()
    street = models.CharField()
    house_number = models.PositiveSmallIntegerField()


class SupplyChain(TimestampMixin):
    pass


class Supplier(TimestampMixin):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=200)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="suppliers"
    )
    type = models.CharField(choices=SupplierType.choices)


class Product(models.Model):
    name = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    release_date = models.DateField()
    suppliers = models.ManyToManyField(Supplier, related_name="products")


class SupplyChainLink(TimestampMixin):
    supply_chain = models.ForeignKey(
        SupplyChain, on_delete=models.CASCADE, related_name="links"
    )
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    parent = models.OneToOneField(
        "self", on_delete=models.PROTECT, null=True, related_name="child"
    )
    level = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(4),)
    )
    products = models.ManyToManyField(
        Product, related_name="supply_chain_links"
    )
    debt = models.PositiveIntegerField(default=0)
