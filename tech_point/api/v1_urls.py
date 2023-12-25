from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import (
    ProductViewSet,
    SupplyChainLinkViewSet,
    SupplyChainViewSet,
    UserSignUp,
)

router_v1 = DefaultRouter()

router_v1.register(r"supply-chains", SupplyChainViewSet)
router_v1.register(r"supply-chain-links", SupplyChainLinkViewSet)
router_v1.register(r"products", ProductViewSet)

urlpatterns = [
    path("auth/sign-up/", UserSignUp.as_view(), name="sign-up"),
    path("auth/sign-in/", obtain_auth_token, name="sign-in"),
    path("", include(router_v1.urls)),
]
