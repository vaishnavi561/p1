from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from datetime import date
from .models import FamilyProfile, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class FamilyProfileSerializer(serializers.ModelSerializer):
    question_count = serializers.IntegerField(read_only=True, default=0)
    # P2-07: Compute age dynamically at read time from date_of_birth
    age = serializers.SerializerMethodField()

    class Meta:
        model = FamilyProfile
        fields = [
            'id', 
            'name', 
            'relation', 
            'date_of_birth', 
            'age', 
            'height', 
            'weight', 
            'a1c', 
            'bp_systolic', 
            'bp_diastolic', 
            'conditions', 
            'deleted_at',
            'created_at'
        ]
        read_only_fields = ['id', 'user', 'deleted_at', 'created_at']

    def get_age(self, obj):
        """Compute age dynamically from date_of_birth."""
        if not obj.date_of_birth:
            return None
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))


class ChatQuerySerializer(serializers.Serializer):
    member_id = serializers.IntegerField(required=True)
    question = serializers.CharField(required=True, allow_blank=False)
    model = serializers.CharField(required=False, default='Ollama')
    api_key = serializers.CharField(required=False, allow_blank=True)