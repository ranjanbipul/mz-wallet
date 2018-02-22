from rest_framework import routers
from .views import *

routers = routers.DefaultRouter()
routers.register(r'accounts', AccountViewSet)
routers.register(r'transactions', TransactionViewSet)

urlpatterns = routers.urls
