# grant_app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

# DRF uchun router
router = DefaultRouter()
router.register(r'academic-years', api_views.AcademicYearViewSet)
router.register(r'grant-applications', api_views.GrantApplicationViewSet, basename='grant-application')
router.register(r'appeals', api_views.AppealViewSet, basename='appeal')

urlpatterns = [
    # Asosiy sahifalar
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('', views.home_view, name='home'),

    # Grantlar bilan ishlash uchun yangi sahifalar
    path('grants/', views.application_list_view, name='grant_application_list'),
    path('grants/apply/', views.application_create_view, name='grant_application_create'),
    path('grants/<int:pk>/', views.application_detail_view, name='grant_application_detail'),
    path('grants/<int:application_pk>/appeal/', views.appeal_create_view, name='appeal_create'),

    # REST API uchun yo'llar
    path('api/', include(router.urls)),
]
# auth_app/urls.py (router'ga qo'shimcha)

from . import api_views


router.register(r'notifications', api_views.NotificationViewSet, basename='notification')

