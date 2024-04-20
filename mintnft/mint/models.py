from django.db import models

# Create your models here.
class Mint(models.Model):
    student_name = models.CharField(max_length=200)
    student_cgpa = models.DecimalField(max_digits = 5, decimal_places = 2)
    student_wallet = models.CharField(max_length=200)
    certificate_url = models.URLField(max_length=1000)
