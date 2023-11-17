from rest_framework import serializers
from .models import Detections

class DetectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detections
        fields = ['id', 'prediction_result', 'user', 'prediction_details', 'img', 'datetime','active']
