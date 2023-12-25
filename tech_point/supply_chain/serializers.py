from rest_framework import serializers

from supply_chain.models import Product, Supplier, SupplyChain, SupplyChainLink


class SupplierSerializer(serializers.ModelSerializer):
    address = serializers.SlugRelatedField(
        slug_field="full_address", read_only=True
    )

    class Meta:
        model = Supplier
        fields = "__all__"


class SupplyChainLinkSerializer(serializers.ModelSerializer):
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = SupplyChainLink
        fields = (
            "id",
            "supply_chain",
            "level",
            "debt",
            "supplier",
            "parent",
            "products",
        )
        read_only_fields = ("level", "debt", "parent")
        extra_kwargs = {
            "supply_chain": {"write_only": True},
        }

    def create(self, validated_data):
        parent = validated_data["supply_chain"].last_link
        validated_data["parent"] = parent
        validated_data["level"] = parent.level + 1 if parent else 0
        return super().create(validated_data)


class SupplyChainSerializer(serializers.ModelSerializer):
    links = serializers.SerializerMethodField()

    class Meta:
        model = SupplyChain
        fields = ("id", "created_at", "links")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "model", "release_date")
