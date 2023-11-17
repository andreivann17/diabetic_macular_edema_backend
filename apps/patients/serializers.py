from rest_framework import serializers
from .models import Patient, BloodType, Gender

class BloodTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodType
        fields = '__all__'

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    blood_type = serializers.StringRelatedField()
    gender = serializers.StringRelatedField()
    email = serializers.CharField(source='user.email', read_only=True)
    
    all_genders = serializers.SerializerMethodField()
    all_blood_types = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'first_name', 'last_name', 'birth_date', 'gender', 'blood_type', 'email', 'active', 'created_at', 'updated_at', 'all_genders', 'all_blood_types',"img"]

    def get_all_genders(self, obj):
        return GenderSerializer(Gender.objects.all(), many=True).data

    def get_all_blood_types(self, obj):
        return BloodTypeSerializer(BloodType.objects.all(), many=True).data
