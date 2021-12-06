from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import widgets
from .models import MAX_LENGTH_LONG, MAX_LENGTH_MED, Course, Material


class CourseDetailsForm(forms.ModelForm):
    """
    Form for edit or create a new course
    """
    class Meta:
        model = Course
        fields = '__all__'


class MaterialForm(forms.ModelForm):
    """
    Form for edit or create a new course material
    """
    class Meta:
        model = Material
        fields = ('title', 'content', 'type')

