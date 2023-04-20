from django.db import models

# Create your models here.


class ReplyWakeUp(models.Model):
    text = models.TextField()
    