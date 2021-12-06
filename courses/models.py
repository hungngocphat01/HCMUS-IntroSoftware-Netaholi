from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

MAX_LENGTH_LONG = 100
MAX_LENGTH_MED = 50


class Course(models.Model):
    STATUS_CHOICES = (
        ('opening', 'Đang mở để đăng ký'),
        ('inprogress', 'Đang tiến hành'),
        ('ended', 'Đã kết thúc')
    )

    name = models.CharField(verbose_name='Tên khóa học', max_length=MAX_LENGTH_LONG)
    ctype = models.CharField(verbose_name='Loại khóa học', max_length=MAX_LENGTH_MED)
    start_date = models.DateField(verbose_name='Ngày bắt đầu', auto_now_add=True)
    status = models.CharField(verbose_name='Trạng thái khóa học', choices=STATUS_CHOICES, max_length=MAX_LENGTH_MED)
    tuition_fee = models.FloatField(verbose_name='Học phí')
    description = models.TextField(verbose_name='Mô tả khóa học')
    schedule = models.TextField(verbose_name='Lịch trình')
    image_url = models.URLField(verbose_name='Link ảnh minh họa', null=True)

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='Người dùng')
    course = models.OneToOneField(Course, on_delete=models.CASCADE, verbose_name='Khóa học')
    content = models.TextField(verbose_name='Nội dung')
    star = models.SmallIntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)],
        verbose_name='Điểm'
    )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")

    def __str__(self):
        return self.course.name + '_' + self.user.username


class Material(models.Model):
    TYPE_CHOICES = (('assignment', 'Bài tập'), ('document', 'Tài liệu'))
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.course.name + '_' + self.title

