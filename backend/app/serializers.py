from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Users, AdminAccounts, Appointments, Treatments, Billing, MedicalHistory, WaitingList, Notifications, AuditLogs, Feedback, Schedules

from rest_framework import serializers
from .models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            'id',
            'email',          # main login field
            'password',
            'first_name',
            'last_name',
            'date_of_birth',
            'gender',
            'contact_number',
            'address',
            'emergency_contact',
            'created_at',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def validate_email(self, value):
        if "@" not in value:
            raise serializers.ValidationError("Wrong email format...")
        return value

    def create(self, validated_data):
        # Create user with email as identifier
        user = Users(
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            date_of_birth=validated_data.get('date_of_birth'),
            gender=validated_data.get('gender'),
            contact_number=validated_data.get('contact_number', ''),
            address=validated_data.get('address'),
            emergency_contact=validated_data.get('emergency_contact'),
        )
        # Hash the password properly
        user.set_password(validated_data['password'])
        user.save()
        return user


class AdminAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminAccounts
        fields = '__all__'

class AppointmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointments
        fields = '__all__'

class TreatmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatments
        fields = '__all__'

class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = '__all__'

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class WaitingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitingList
        fields = '__all__'

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

class AuditLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLogs
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class SchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = '__all__'
