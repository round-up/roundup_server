# model image link : https://drive.google.com/open?id=0B05vtPvZZCtedUh2VWo1bHMzUGs
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserExtendManager(BaseUserManager):
    def create_user(self, user_name, email,
                    user_birth, user_gender, user_profile_image,
                    user_cover, user_phone_number):
        user = self.model(email=email, user_name=user_name,
                          user_birth=user_birth, user_gender=user_gender,
                          user_profile_image=user_profile_image, user_cover=user_cover,
                          user_phone_number=user_phone_number)
        return user

    def create_superuser(self):
        return None


class UserExtend(AbstractBaseUser):
    email = models.EmailField(
        max_length=255, unique=True
    )
    user_name = models.CharField(max_length=100)
    user_birth = models.DateField()
    user_gender = models.BooleanField(default=False)
    user_profile_image = models.ImageField(width_field=100, height_field=100, blank=True)
    user_cover = models.ImageField(blank=True)
    user_phone_number = models.CharField(max_length=20)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserExtendManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'user_gender']

    class Meta:
        ordering = ('user_name',)

    def get_full_name(self):
        return self.user_name

    def get_short_name(self):
        return self.user_name

    def __unicode__(self):
        return self.username


class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.category_name


class GroupBelong(models.Model):
    belong_title = models.CharField(max_length=50)
    belong_content = models.TextField()

    def __unicode__(self):
        return self.belong_title


class Group(models.Model):
    group_leader_email = models.ForeignKey(User, unique=False)
    belong_id = models.ForeignKey(GroupBelong)
    category_id = models.ForeignKey(Category)
    group_name = models.CharField(max_length=100)
    group_description = models.TextField()
    group_start_date = models.DateField(auto_now=True)
    group_place = models.CharField(max_length=100)
    group_logo = models.ImageField(width_field=100, height_field=100)
    group_cover = models.ImageField()
    group_recruit_state = models.BooleanField(default=False)

    class Meta:
        ordering = ('group_start_date', 'group_name',)

    def __unicode__(self):
        return self.group_name


class UnitedGroup(models.Model):
    united_group_title = models.CharField(max_length=100)
    united_group_description = models.TextField()
    united_group_starting_date = models.DateField(auto_now=True)
    united_group_recruit_state = models.BooleanField(default=False)

    class Meta:
        ordering = ('united_group_starting_date', 'united_group_title',)

    def __unicode__(self):
        return self.united_group_title


class UnitedGroupsBridge(models.Model):
    group_id = models.ForeignKey(Group)
    united_group = models.ForeignKey(UnitedGroup)

    class Meta:
        unique_together = ('group_id', 'united_group', )


class GroupUserLevel(models.Model):
    group_id = models.ForeignKey(Group)
    level_title = models.CharField(max_length=100)
    level_desc = models.TextField()
    level_perm = models.IntegerField()


class GroupUsers(models.Model):
    group_id = models.ForeignKey(Group)
    user_email = models.ForeignKey(User)
    group_user_level_id = models.ForeignKey(GroupUserLevel)
    group_gisoo = models.IntegerField(default=1)
    # level_assined

    class Meta:
        unique_together = ('group_id', 'user_email', )


class GroupBulletins(models.Model):
    group_id = models.ForeignKey(Group)
    user_email = models.ForeignKey(User)
    bulletin_type = models.CharField(max_length=10)
    bulletin_title = models.CharField(max_length=100)
    bulletin_date = models.DateTimeField(auto_now=True)
    bulletin_content = models.TextField()
    bulletin_access_modifier = models.IntegerField(default=1)
    bulletin_attachment = models.FileField()
    bulletin_tags = models.TextField()

    class Meta:
        ordering = ('-bulletin_date',)


class GroupSchedules(models.Model):
    bulletin_id = models.ForeignKey(GroupBulletins)
    schedule_start_date = models.DateTimeField(auto_now=True)
    schedule_end_date = models.DateTimeField(auto_now=True)
    schedule_place = models.CharField(max_length=100)
