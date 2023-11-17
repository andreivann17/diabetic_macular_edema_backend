from rest_framework import serializers

# Primero, definamos un serializer para manejar los datos del paciente
class PatientDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    patient_id = serializers.CharField()
    image = serializers.ImageField()  # Asume que la imagen se envía como un archivo

    def create(self, validated_data):
        # Usamos los datos validados para crear la imagen DICOM
        # Asegúrate de implementar la lógica para convertir la imagen a DICOM
        dicom_image = create_dicom_image(validated_data['name'], validated_data['patient_id'], validated_data['image'])

        # Aquí puedes convertir tu imagen DICOM a base64
        # Pero necesitarías implementar esta función
        dicom_image_base64 = convert_dicom_to_base64(dicom_image)
        return dicom_image_base64