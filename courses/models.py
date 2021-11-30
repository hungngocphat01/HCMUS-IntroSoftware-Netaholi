from django.db import models

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