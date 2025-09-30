import datetime
from django import forms
from django.forms import ModelForm, ValidationError, FileInput
from django.core.validators import RegexValidator
from .models import *

class StudentForm1(forms.Form):
    student_id = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all(),
        empty_label="Select an option",
        required=False,
        widget=forms.RadioSelect()
    )
    enrolled_sections = forms.ModelMultipleChoiceField(
        queryset=Section.objects.all(),
        required=False,
    )
    email = forms.EmailField()
    phone_number = forms.CharField(
                validators=[RegexValidator(r"^[0-9]+$", "Enter a valid phone number.")],
                required=False
            )
    address = forms.CharField(widget=forms.Textarea(), required=False)

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            "student_id", 
            "first_name", 
            "last_name", 
            "faculty", 
            "enrolled_sections",
        ]
        widgets = {
        }
    def clean(self):
        cleaned_data = super().clean()
        student_id = cleaned_data.get("student_id")
        first_name = cleaned_data.get("first_name")
        last_name = cleaned_data.get("last_name")
        faculty = cleaned_data.get("faculty")
        enrolled_sections = cleaned_data.get("enrolled_sections")

        return cleaned_data
class StudentProfileForm(ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            "email",
            "phone_number",
            "address",
            "image"
        ]
        widgets = {
            "image": FileInput(attrs={"class": "hidden"}),
        }
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        phone_number = cleaned_data.get("phone_number")
        address = cleaned_data.get("address")
        image = cleaned_data.get("image")

        if not email.endswith("@kmitl.ac.th"):
            raise forms.ValidationError("email จะต้องลงท้ายด้วย @kmitl.ac.th")

        return cleaned_data
    
class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = [
            "course_code",
            "course_name",
            "credits"
        ]
        widgets = {
        }
    def clean(self):
        cleaned_data = super().clean()
        course_code = cleaned_data.get("course_code")
        course_name = cleaned_data.get("course_name")
        credits = cleaned_data.get("lascreditst_name")

        return cleaned_data

class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = [
            "section_number",
            "semester",
            "professor",
            "day_of_week",
            "start_time",
            "end_time",
            "capacity",
        ]
        widgets = {
        }
    def clean(self):
        cleaned_data = super().clean()
        section_number = cleaned_data.get("section_number")
        professor = cleaned_data.get("professor")
        day_of_week = cleaned_data.get("day_of_week")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        capacity = cleaned_data.get("capacity")
        
        if start_time and end_time and end_time < start_time:
            raise ValidationError(
                    "End time must be after start time"
                )
        
        if capacity and capacity <= 20:
            raise ValidationError(
                    "capacity must more than 20"
                )

        return cleaned_data