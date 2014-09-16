from django.db import models


class Member(models.Model):
    student_id = models.IntegerField(primary_key=True)
    #l_name = models.CharField(max_length=100) TODO: login the first name of each member
    #reg_date = models.DateTimeField('Registration date') TODO: log in the registration date of each member


class AccessCard(models.Model):
    # Django cannot handle primary keys made of multiple columns, let it generate a default one
    member = models.ForeignKey(Member)
    rfid = models.BigIntegerField(unique=True)