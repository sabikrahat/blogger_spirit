from django.db import models
from datetime import datetime
import os


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s-%s" % (timeNow, old_filename)
    return os.path.join('uploads/', filename)

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=1024)
    point = models.IntegerField(default=100)
    img = models.ImageField(upload_to=filepath, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_users'

    def isExists(self):
        if UserModel.objects.filter(email=self.email):
            return True
        return False

class PostModel(models.Model):
    publisherId = models.BigIntegerField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=3072)
    img = models.ImageField(upload_to=filepath, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_posts'

class TransferPoint(models.Model):
    senderEmail = models.CharField(max_length=40)
    receiverEmail = models.CharField(max_length=40)
    point = models.IntegerField(0)
    transfered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_transfer_point'
