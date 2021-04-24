from django.conf.urls import url
from . import views

app_name = 'user'

urlpatterns = [
    url(r'^create/', views.CreateUserView.as_view(), name='create'),
    url(r'^token/', views.CreateTokenView.as_view(), name='token'),
    url(r'^me/', views.ManageUserView.as_view(), name='me')
]
