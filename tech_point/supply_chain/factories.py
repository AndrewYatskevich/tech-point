import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from supply_chain import models


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = models.Address

    country = factory.Faker("country")
    city = factory.Faker("city")
    street = factory.Faker("street_address")
    house_number = factory.Faker("pyint", min_value=1, max_value=10000)


class SupplyChainFactory(DjangoModelFactory):
    class Meta:
        model = models.SupplyChain


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = models.Supplier

    name = factory.Faker("company")
    email = factory.Faker("email")
    address = factory.SubFactory(AddressFactory)
    type = FuzzyChoice(models.SupplierType.values)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = models.Product

    name = factory.Faker("word", part_of_speech="noun")
    model = factory.Faker("ssn")
    release_date = factory.Faker("date")

    @factory.post_generation
    def suppliers(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.suppliers.add(*extracted)


class SupplyChainLinkFactory(DjangoModelFactory):
    class Meta:
        model = models.SupplyChainLink

    supply_chain = factory.SubFactory(SupplyChainFactory)
    supplier = factory.SubFactory(SupplierFactory)
    parent = factory.SubFactory(
        "supply_chain.factories.SupplyChainLinkFactory"
    )
    level = factory.Faker("pyint", min_value=0, max_value=4)
    debt = factory.Faker("pyint", min_value=0)

    @factory.post_generation
    def products(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        self.products.add(*extracted)
