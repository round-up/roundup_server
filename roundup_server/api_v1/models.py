from django.db import models


class Users(models.Model):
    user_email = models.CharField(max_length=100)
    user_passwd = models.CharField(max_length=16)
    user_name = models.CharField(max_length=50)
    user_birth = models.DateField()
    user_gender = models.BooleanField(default=False)
    user_profile_image = models.ImageField(width_field=100, height_field=100)
    user_curver = models.ImageField()
    user_phone_number = models.CharField(max_length=20)

    class Meta:
        ordering = ('user_name',)