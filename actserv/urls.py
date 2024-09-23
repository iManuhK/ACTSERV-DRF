from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, TransactionViewSet, UserViewSet, UserTransactionSummaryViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'users', UserViewSet, basename='user')
router.register(r'admin/users/transaction-summary', UserTransactionSummaryViewSet, basename='user-transaction-summary')

urlpatterns = [
    path('', include(router.urls)),
]
