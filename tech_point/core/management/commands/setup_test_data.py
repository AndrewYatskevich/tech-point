import random

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from supply_chain import factories
from supply_chain.models import SupplierType


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        output = input(
            "This command will delete all exist data.\n"
            "Do you want to continue? Type yes/no: "
        )
        if output.lower() != "yes":
            return "Generating test data cancelled"

        call_command("flush", "--no-input")

        chain_drafts = tuple(
            tuple(
                SupplierType.values[i]
                for i in sorted(
                    random.sample(range(5), k=random.randint(1, 5))
                )
            )
            for _ in range(5)
        )
        addresses = [factories.AddressFactory() for _ in range(10)]
        products = [factories.ProductFactory() for _ in range(10)]

        for chain_draft in chain_drafts:
            supply_chain = factories.SupplyChainFactory()
            parent = None
            for i, link in enumerate(chain_draft):
                supplier = factories.SupplierFactory(
                    address=random.choice(addresses), type=link
                )
                parent = factories.SupplyChainLinkFactory(
                    supply_chain=supply_chain,
                    supplier=supplier,
                    parent=parent,
                    level=i,
                    products=random.sample(
                        products, k=random.randint(0, len(products))
                    ),
                )
