from django.db import models
from django.contrib.auth.models import User


MAX_LENGTH_LONG = 100
MAX_LENGTH_MED = 50

class UserProfile(models.Model):
    GENDER_CHOICES = (
        (True, 'Nam'),
        (False, 'Nữ')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='Ngày sinh')
    gender = models.BooleanField(verbose_name='Giới tính', choices=GENDER_CHOICES)
    is_teacher = models.BooleanField()
    profession = models.CharField(verbose_name='Nghề nghiệp', max_length=MAX_LENGTH_MED)
    department = models.CharField(verbose_name='Nơi công tác', max_length=MAX_LENGTH_LONG)

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name

class Course(models.Model):
    STATUS_CHOICES = (
        ('opening', 'Đang mở để đăng ký'),
        ('inprogress', 'Đang tiến hành'),
        ('ended', 'Đã kết thúc')
    )

    name = models.CharField(verbose_name='Tên khóa học', max_length=MAX_LENGTH_LONG)
    ctype = models.CharField(verbose_name='Loại khóa học', max_length=MAX_LENGTH_MED)
    start_date = models.DateField(verbose_name='Ngày bắt đầu')
    status = models.CharField(verbose_name='Trạng thái khóa học', choices=STATUS_CHOICES, max_length=MAX_LENGTH_MED)
    tuition_fee = models.FloatField(verbose_name='Học phí')
    description = models.TextField(verbose_name='Mô tả khóa học')
    schedule = models.TextField(verbose_name='Lịch trình')

    def __str__(self):
        return self.name