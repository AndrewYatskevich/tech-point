from django_filters.filterset import CharFilter, FilterSet, NumberFilter

from supply_chain.models import SupplyChainLink


class SupplyChainLinkFilter(FilterSet):
    country = CharFilter(field_name="supplier__address__country")
    product = NumberFilter(field_name="products__id")

    class Meta:
        model = SupplyChainLink
        fields = ("country", "product")
