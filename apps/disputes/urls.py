from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DisputeViewSet

router = DefaultRouter()
router.register(r'disputes', DisputeViewSet, basename='disputes')

urlpatterns = [
    path('', include(router.urls)),
    # Specific /api/orders/{id}/dispute endpoint could be mapped here or in OrderViewSet
    # But for strict REST, separate resource is fine.
]
