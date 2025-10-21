import datetime
from rest_framework import serializers
from appointments.models import *

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_detail = DoctorSerializer(read_only=True, source="doctor")
    patient_detail = PatientSerializer(read_only=True, source="patient")
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all(), write_only=True)
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)
    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "patient",
            "doctor_detail",
            "patient_detail",
            "date",
            "at_time",
            "details",
        ]

    def validate(self, data):
        apm_datetime = datetime.datetime.combine(data['date'], data['at_time'])
        if apm_datetime < datetime.datetime.now():
            raise serializers.ValidationError("The appointment date or time must be in the future.")
        return data