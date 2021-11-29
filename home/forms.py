from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MAX_LENGTH_LONG, MAX_LENGTH_MED

class SignUpForm(UserCreationForm):
    """
    Sign up form for students
    """
    GENDER_CHOICES = (
        (True, 'Nam'),
        (False, 'Nữ')
    )
    last_name = forms.CharField(max_length=MAX_LENGTH_MED, label='Họ và tên đệm', required=True)
    first_name = forms.CharField(max_length=MAX_LENGTH_MED, label='Tên', required=True)
    birthday = forms.DateField(label='Ngày sinh', required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, label='Giới tính')
    email = forms.EmailField(max_length=MAX_LENGTH_LONG, label='Email', required=True)
    profession = forms.CharField(max_length=MAX_LENGTH_LONG, label='Nghề nghiệp', required=True)
    department = forms.CharField(max_length=MAX_LENGTH_LONG, label='Đơn vị công tác', required=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profession', 'department')

class TeacherSignUpForm(SignUpForm):
    """
    Sign-up form for teachers
    """
    bio = forms.CharField(widget=forms.Textarea, label='Giới thiệu bản thân', required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'profession', 'department', 'bio')