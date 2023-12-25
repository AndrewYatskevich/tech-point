from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
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
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("auth/sign-up/", UserSignUp.as_view(), name="sign-up"),
    path("auth/sign-in/", obtain_auth_token, name="sign-in"),
    path("", include(router_v1.urls)),
]
