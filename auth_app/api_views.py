from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
from .permissions import *
from .services.hemis_api_service import HemisAPIClient, APIClientException
from .utils import map_api_data_to_student_model_defaults

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username va password kiritilishi shart."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            api_client = HemisAPIClient()
            api_token, _ = api_client.login(username, password)
            student_info_from_api = api_client.get_account_me(api_token_override=api_token)
            
            with transaction.atomic():
                student_defaults = map_api_data_to_student_model_defaults(student_info_from_api, username)
                student, _ = Student.objects.update_or_create(username=username, defaults=student_defaults)
            
            return Response({"error": "API token logikasi hali to'liq sozlanmagan."}, status=status.HTTP_501_NOT_IMPLEMENTED)

        except APIClientException:
            return Response({"error": "Login yoki parol xato."}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": f"Tizimda kutilmagan xatolik: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# grant_app/api_views.py

from rest_framework import viewsets, permissions
from .models import GrantApplication, Appeal, AcademicYear
from .serializers import GrantApplicationSerializer, AppealSerializer, AcademicYearSerializer

class AcademicYearViewSet(viewsets.ReadOnlyModelViewSet):
    """O'quv yillarini ko'rish uchun API."""
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [permissions.IsAuthenticated]

class GrantApplicationViewSet(viewsets.ModelViewSet):
    """
    Talabaning grant arizalarini boshqarish uchun API.
    Faqat o'ziga tegishli arizalarni ko'ra oladi.
    """
    serializer_class = GrantApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        # request.user bu yerda Django'ning standart User modeli bo'lishi mumkin.
        # Bizning tizimda `request.current_student` ishlatiladi.
        # Bu qismni API uchun alohida autentifikatsiya klassi bilan to'g'rilash kerak.
        student = getattr(self.request, 'current_student', None)
        if student:
            return GrantApplication.objects.filter(student=student)
        return GrantApplication.objects.none()

    def perform_create(self, serializer):
        student = getattr(self.request, 'current_student', None)
        if student:
            serializer.save(student=student)
        else:
            raise serializers.ValidationError("Autentifikatsiyadan o'tgan talaba topilmadi.")

class AppealViewSet(viewsets.ReadOnlyModelViewSet):
    """Apellyatsiyalarni ko'rish uchun API."""
    serializer_class = AppealSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        student = getattr(self.request, 'current_student', None)
        if student:
            return Appeal.objects.filter(application__student=student)
        return Appeal.objects.none()
    

# auth_app/api_views.py (faylga qo'shimcha)

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Foydalanuvchining bildirishnomalarini boshqarish uchun API.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        """Faqat autentifikatsiyadan o'tgan foydalanuvchining bildirishnomalarini qaytaradi."""
        return self.request.user.notifications.all()

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request, *args, **kwargs):
        """Barcha o'qilmagan bildirishnomalarni o'qilgan deb belgilaydi."""
        request.user.notifications.filter(read=False).update(read=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, id=None):
        """Bitta bildirishnomani o'qilgan deb belgilaydi."""
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)