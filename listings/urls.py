from django.urls import path, include
from .views import listingViewSet, BookingViewSet, InitiatePaymentView, VerifyPaymentView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#an object for the default router class,
router.register('listings', listingViewSet, basename= 'listing')
router.register ('bookings', BookingViewSet, basename= 'booking')

urlpatterns = [
    path('api/', include(router.urls)),   # 👈 include router-generated routes
    path('api/payments/initiate/', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('api/payments/verify/', VerifyPaymentView.as_view(), name='verify-payment'),
]