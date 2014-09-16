import datetime

from django.db import models

class Member(models.Model):
    student_id = models.CharField('Student number', primary_key=True, max_length=8)
    f_name = models.CharField('First name', max_length=50)
    l_name = models.CharField('Last name', max_length=50)
    reg_date = models.DateField('Registration date', default=datetime.datetime.today())

    def __str__(self):
        return self.student_id


class AccessCard(models.Model):
    # Django cannot handle primary keys made of multiple columns, let it generate a default one
    member = models.ForeignKey(Member)
    rfid = models.CharField(unique=True, max_length=12)

    def __str__(self):
        return self.rfid