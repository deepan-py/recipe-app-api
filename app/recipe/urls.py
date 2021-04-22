from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet,)

app_name = 'recipe'

urlpatterns = [
    url('', include(router.urls)),
]
