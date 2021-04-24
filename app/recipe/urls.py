from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('tags', views.TagViewSet,)
router.register('ingredients', views.IngredientViewSets,
                basename='ingredients')
# ? https://www.django-rest-framework.org/api-guide/routers/#usage
# the above link gives details of basenmae

app_name = 'recipe'

urlpatterns = [
    url('', include(router.urls)),
]
