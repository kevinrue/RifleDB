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
    rfid = models.CharField(primary_key=True, max_length=10)
    reg_date = models.DateField('Registration date', default=datetime.datetime.today())

    def __str__(self):
        return self.rfid


class LoggingEvent(models.Model):
    # Django cannot handle primary keys made of multiple columns, let it generate a default one
    rfid = models.CharField(max_length=10)
    check_in = models.DateTimeField('Check in', default=datetime.datetime.today())
    check_out = models.DateTimeField('Check out', default=None, blank=True, null=True)

    def __str__(self):
        return "%s from %s to %s" % (self.rfid, self.check_in, self.check_out)