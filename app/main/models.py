from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length = 30, unique=True )
    description = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'course'