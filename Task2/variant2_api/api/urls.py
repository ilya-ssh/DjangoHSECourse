from rest_framework import routers
from .views import OrganizationViewSet, UserViewSet
router = routers.SimpleRouter()
router.register(r"organization", OrganizationViewSet)
router.register(r"user", UserViewSet)
urlpatterns = router.urls
