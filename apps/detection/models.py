from django.db import models
from django.contrib.auth.models import User
from ..patients.models import Patient

class Detections(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    prediction_details = models.TextField()
    img = models.ImageField(upload_to="detection/", blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        db_table = "detections"

class Diseases(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True)
    reference = models.CharField(max_length=500, null=True)
    class Meta:
        db_table = "diseases"


class DetectionsPredictions(models.Model):
    detection = models.ForeignKey(Detections, on_delete=models.CASCADE)
    disease = models.ForeignKey(Diseases, on_delete=models.CASCADE,null=True)  # Modificado aquí
    img = models.ImageField(upload_to="detection_prediction/",blank=True,null=True)
    prediction_probability = models.FloatField(max_length=10,null=True)

    def __str__(self):
        return self.disease.name  # Retornar el name del disease relacionado
    class Meta:
        db_table = "detections_predictions"

class DetectionsPredictionsDescription(models.Model):
    name = models.CharField(max_length=100,null=True)
    detections_predictions = models.ForeignKey(DetectionsPredictions, on_delete=models.CASCADE,null=True)  # Modificado aquí
    class Meta:
        db_table = "detections_predictions_description"

