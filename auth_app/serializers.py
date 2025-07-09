# grant_app/serializers.py

from rest_framework import serializers
from .models import *

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ('api_user_hash',) # Hash kabi maxfiy ma'lumotlarni chiqarib tashlash

class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = '__all__'

class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ('id', 'document_type', 'description', 'file', 'uploaded_at')

class SocialActivityEvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialActivityEvaluation
        exclude = ('application', 'evaluator') # Bog'liq obyektlarni qisqartirish

class GrantApplicationSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    academic_year = serializers.StringRelatedField(read_only=True)
    documents = ApplicationDocumentSerializer(many=True, read_only=True)
    social_evaluation = SocialActivityEvaluationSerializer(read_only=True)

    class Meta:
        model = GrantApplication
        fields = '__all__'

class AppealSerializer(serializers.ModelSerializer):
    application = GrantApplicationSerializer(read_only=True)

    class Meta:
        model = Appeal
        fields = '__all__'


# auth_app/serializers.py (faylga qo'shimcha)

from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    target = serializers.StringRelatedField()
    
    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'target', 'description', 'read', 'timestamp')