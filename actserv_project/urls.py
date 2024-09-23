from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from actserv import views

# Register viewsets with the router
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'transactions', views.TransactionViewSet)

# Wire up API routes using DefaultRouter and also provide browsable API login URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),  # Register all router URLs
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
