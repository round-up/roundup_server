from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from additionals import SUCCESS_TO_EXCEED


class UserExtendManager(BaseUserManager):
    def create_user(self, email, password=None, **others):
        user = self.model(email=email, password=password, **others)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def check_password(self, data):
        email = data['email']
        password = data['password']
        user = self.get_by_natural_key(email)
        if user == None:
            return False
        return user.check_password(password)

    def create_user_by_view(self, data):
        from copy import deepcopy
        print type(data)
        d = dict(deepcopy(data))
        email = d['email']
        password = d['password']
        del d['email']
        del d['password']
        return self.create_user(email, password, **d)

    def create_superuser(self):
        return None


class GroupManager(models.Manager):
    def filter_group_by_leader(self, leader_email):
        user_inst = UserExtend.objects.model(email=leader_email)
        group_inst = Group.objects.filter(group_leader_email=user_inst)
        return group_inst


class GroupUserLevelManager(models.Manager):
    def get_all_user_level(self, group_id):
        group_inst = Group.objects.model(id=group_id)
        level_list = GroupUserLevel.objects.filter(group_id=group_inst)
        return level_list


class GroupUserManager(models.Manager):
    def get_all_users_in_group(self, group_id):
        group_inst = Group.objects.model(id=group_id)
        group_user_list = GroupUsers.objects.filter(group_id=group_inst)
        return group_user_list

    def delete_by_useremail(self, user_email):
        user_inst = UserExtend.objects.model(email=user_email)
        try:
            GroupUsers.objects.filter(user_email=user_inst).delete()
        except Exception:
            return None
        return SUCCESS_TO_EXCEED



class UserExtend(AbstractBaseUser):
    email = models.EmailField(
        max_length=255, unique=True, primary_key=True
    )
    user_name = models.CharField(max_length=100)
    user_birth = models.DateField()
    user_gender = models.BooleanField(default=False)
    user_profile_image = models.TextField(blank=True)
    user_cover = models.TextField(blank=True)
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
        return self.user_name


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
    group_leader_email = models.ForeignKey(UserExtend, unique=False)
    # belong_id = models.ForeignKey(GroupBelong)
    # category_id = models.ForeignKey(Category)
    # group_leader_email = models.CharField(max_length=100)
    group_belong = models.CharField(max_length=100)
    group_category = models.CharField(max_length=100)
    group_name = models.CharField(max_length=100)
    group_description = models.TextField()
    group_start_date = models.DateField(auto_now=True)
    group_place = models.CharField(max_length=100)
    group_logo = models.TextField(blank=True)
    group_cover = models.TextField(blank=True)
    group_recruit_state = models.BooleanField(default=False)

    objects = GroupManager()

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
    #level_desc = models.TextField()
    #level_perm = models.IntegerField()
    objects = GroupUserLevelManager()


class GroupUsers(models.Model):
    group_id = models.ForeignKey(Group)
    user_email = models.ForeignKey(UserExtend)
    group_user_level = models.IntegerField(default=0)
    group_gisoo = models.IntegerField(default=1)
    # level_assined

    objects = GroupUserManager()

    class Meta:
        unique_together = ('group_id', 'user_email', )


class GroupBulletins(models.Model):
    group_id = models.ForeignKey(Group)
    user_email = models.ForeignKey(UserExtend)
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