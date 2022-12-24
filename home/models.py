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
    phone = models.CharField(max_length=15)
    balance = models.CharField(max_length=10)
    img = models.ImageField(upload_to=filepath, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'app_users'

    def isExists(self):
        if UserModel.objects.filter(email=self.email):
            return True
        return False

# class PostModel(models.Model):
#     publisherID = models.OneToOneField(UserModel, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.CharField(max_length=3072)
#     img = models.ImageField(upload_to=filepath, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = 'app_posts'