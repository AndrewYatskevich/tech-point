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
    country = models.CharField(db_index=True)
    city = models.CharField(db_index=True)
    street = models.CharField()
    house_number = models.PositiveSmallIntegerField()

    @property
    def full_address(self) -> str:
        return ", ".join(
            (self.country, self.city, self.street, str(self.house_number))
        )

    def __str__(self):
        address = self.full_address
        return address if len(address) < 50 else address[:50] + "..."


class Supplier(TimestampMixin):
    name = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=200, unique=True)
    address = models.ForeignKey(
        Address, on_delete=models.CASCADE, related_name="suppliers"
    )
    type = models.CharField(choices=SupplierType.choices)

    def __str__(self):
        return f"{self.name}({self.type})"


class SupplyChain(TimestampMixin):
    suppliers = models.ManyToManyField(
        Supplier, through="SupplyChainLink", related_name="supply_chains"
    )

    def __str__(self):
        return f"{self.__class__.__name__}({self.pk})"

    @property
    def last_link(self) -> "SupplyChainLink":
        return self.links.order_by("level").last()


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    model = models.CharField(max_length=50)
    release_date = models.DateField()

    def __str__(self):
        return f"{self.name}"


class SupplyChainLink(TimestampMixin):
    supply_chain = models.ForeignKey(
        SupplyChain, on_delete=models.CASCADE, related_name="links"
    )
    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name="links"
    )
    parent = models.OneToOneField(
        "self",
        on_delete=models.RESTRICT,
        related_name="child",
        blank=True,
        null=True,
    )
    level = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(4),)
    )
    products = models.ManyToManyField(
        Product, related_name="supply_chain_links"
    )
    debt = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = (
            models.CheckConstraint(
                check=models.Q(level__lte=4), name="level__lte__4"
            ),
            models.UniqueConstraint(
                fields=("supply_chain", "level"), name="unique_chain_level"
            ),
            models.UniqueConstraint(
                fields=("supply_chain", "supplier"),
                name="unique_chain_supplier",
            ),
            models.UniqueConstraint(
                fields=("supply_chain", "parent"), name="unique_chain_parent"
            ),
        )

    def __str__(self):
        return (
            f"{self.__class__.__name__}({self.id})"
            f"(SupplyChain({self.supply_chain.id}), level({self.level}))"
        )
