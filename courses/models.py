import base64
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
# from django.db.models.signals impor

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
    cover_image = models.ImageField(verbose_name='Ảnh minh họa', null=True)
    cover_image_binary = models.BinaryField(null=True)

    def __str__(self):
        return self.name

    def is_enrolled(self, username):
        if Course.objects.filter(id=self.id, coursestudents__student__username=username).exists():
            return True
        elif Course.objects.filter(id=self.id, courseteachers__teacher__username=username).exists():
            return True
        return False

    def enroll_student(self, username):
        if self.is_enrolled(username) or self.status == 'ended':
            return False
        else:
            student = User.objects.get(username=username)
            self.coursestudents_set.create(student=student)
            return True

    def get_base64_image(self):
        return base64.b64encode(self.cover_image_binary.tobytes()).decode('utf-8')


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


class CourseTeachers(models.Model):
    ROLE_CHOICES = (
        ('lecturer', 'Giảng viên'),
        ('ta', 'Trợ giảng')
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Giảng viên')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Khóa học')
    role = models.CharField(max_length=100, verbose_name='Vai trò')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Ngày tham gia khóa học')

    class Meta:
        unique_together = ("teacher", "course")


class CourseStudents(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Học viên')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Khóa học')
    date_joined = models.DateField(auto_now_add=True, verbose_name='Ngày tham gia khóa học')
    score = models.FloatField(
        verbose_name='Điểm tổng kết',
        validators=[MaxValueValidator(10), MinValueValidator(0)],
        null=True
    )

    class Meta:
        unique_together = ("student", "course")
