import datetime

from django.db import models
from django.utils import timezone

# Create your models here.



class C_result(models.Model):
    user_id = models.IntegerField(default=0)
    claim = models.CharField(max_length=400, default="")
    title = models.CharField(max_length=400, default="")
    evidence1 = models.CharField(max_length=400, default="")
    evidence2 = models.CharField(max_length=400, default="")
    evidence3 = models.CharField(max_length=400, default="")
    evidence4 = models.CharField(max_length=400, default="")
    evidence5 = models.CharField(max_length=400, default="")
    T_F = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    finish = models.IntegerField(default=0)


class V_result(models.Model):
    user_id = models.IntegerField(default=0)
    claim_id = models.IntegerField(default=0)
    variation1 = models.CharField(max_length=400, default="")
    T_F1 = models.CharField(max_length=200, default="X")
    variation2 = models.CharField(max_length=400, default="")
    T_F2 = models.CharField(max_length=200, default="X")
    variation3 = models.CharField(max_length=400, default="")
    T_F3 = models.CharField(max_length=200, default="X")
    variation4 = models.CharField(max_length=400, default="")
    T_F4 = models.CharField(max_length=200, default="X")
    variation5 = models.CharField(max_length=400, default="")
    T_F5 = models.CharField(max_length=200, default="X")
    pub_date = models.DateTimeField(default=timezone.now)

