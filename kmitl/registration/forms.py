import datetime
from django import forms
from django.core.validators import RegexValidator
from .models import *

class StudentForm(forms.Form):
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