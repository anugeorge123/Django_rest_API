from django.conf.urls import url, include
from rest_framework import routers
from accounts import views

router = routers.DefaultRouter()
router.register(r'^country', views.CountryView, basename='country')
router.register(r'^state', views.StateView, basename='state')
router.register(r'^city', views.CityView, basename='city')
router.register(r'^signup', views.SignupView, basename='signup')
router.register(r'^login', views.LoginView, basename='login')
router.register(r'^changepassword', views.ChangePasswordView, basename='changepassword')
router.register(r'^resetpassword', views.PasswordResetView, basename='resetpassword')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^password-reset-confirm/', views.PasswordResetConfirmView.as_view()),
]