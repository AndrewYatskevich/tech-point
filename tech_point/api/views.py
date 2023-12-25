from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from api.filters import SupplyChainLinkFilter
from api.permissions import IsActiveEmployee
from supply_chain.models import Product, SupplyChain, SupplyChainLink
from supply_chain.serializers import (
    ProductSerializer,
    SupplyChainLinkSerializer,
    SupplyChainSerializer,
)
from users.serializers import UserSerializer

User = get_user_model()


class UserSignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        serializer.save(
            password=make_password(serializer.validated_data.get("password"))
        )


class SupplyChainViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = (
        SupplyChain.objects.prefetch_related("links", "links__products")
        .select_related("links__supplier", "links__supplier__address")
        .all()
    )
    serializer_class = SupplyChainSerializer
    permission_classes = (IsAdminUser,)

    @action(methods=("get",), detail=True, url_path="links")
    def get_chain_links(self, request, pk):
        links = (
            SupplyChainLink.objects.prefetch_related("products")
            .select_related("supplier", "supplier__address")
            .filter(supply_chain=pk)
        )
        if "country" in request.query_params:
            links = links.filter(
                supplier__address__country=request.query_params["country"]
            )
        if "product" in request.query_params:
            links = links.filter(products=request.query_params["product"])
        serializer = SupplyChainLinkSerializer(links, many=True)
        return Response(serializer.data)


class SupplyChainLinkViewSet(ModelViewSet):
    queryset = SupplyChainLink.objects.prefetch_related(
        "products"
    ).select_related("supplier", "supplier__address")
    serializer_class = SupplyChainLinkSerializer
    permission_classes = (IsActiveEmployee,)
    filterset_class = SupplyChainLinkFilter

    def perform_create(self, serializer):
        serializer.save(supplier=self.request.user.workplace)


class ProductViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
