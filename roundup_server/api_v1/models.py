from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.forms.models import model_to_dict
from additionals import SUCCESS_TO_EXCEED, FAILED_TO_EXCEED


class UserExtendManager(BaseUserManager):
    def create_user(self, email, password=None, **others):
        user = self.model(email=email, password=password, **others)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def check_password(self, data):
        email = data['email']
        password = data['password']
        user = UserExtend.objects.get(email=email)
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
    def filter_group_by_leader(self, email):
        user_inst = UserExtend.objects.get(email=email)
        group_inst = Group.objects.filter(group_leader_email=user_inst)
        return group_inst

    def filter_group_by_group_user(self, email):
        groupuser_inst = GroupUsers.objects.filter(email=email)
        group_inst = Group.objects.filter(id=groupuser_inst)
        return group_inst

class GroupUserLevelManager(models.Manager):
    def get_all_user_level(self, group_id):
        group_inst = Group.objects.get(id=group_id)
        level_list = GroupUserLevel.objects.filter(group_id=group_inst)
        return level_list


class GroupUserManager(models.Manager):
    def add_group_user(self, group_id, email):
        group_inst = Group.objects.get(id=group_id)
        user_inst = UserExtend.objects.get(email=email)
        try:
            new_group_user = GroupUsers(group_id=group_inst, email=user_inst)
            new_group_user.save()
        except Exception, e:
            print e.message
            return None
        return SUCCESS_TO_EXCEED

    def get_all_users_in_group(self, group_id):
        group_inst = Group.objects.model(id=group_id)
        group_user_list = GroupUsers.objects.filter(group_id=group_inst)
        return group_user_list

    def delete_by_useremail(self, email):
        user_inst = UserExtend.objects.model(email=email)
        try:
            GroupUsers.objects.filter(email=user_inst).delete()
        except Exception:
            return None
        return SUCCESS_TO_EXCEED


class GroupFeedsManager(models.Manager):

    # def add_new_feed(self, email):
    #

    def create(self, data):
        try:
            group_id = data['group_id']
            email = data['email']

            group_inst = Group.objects.get(id=group_id)
            print email
            user_inst = UserExtend.objects.get(email=email)

            del data['group_id']
            del data['email']

            image_list = None
            if 'image_list' in data:
                image_list = data['image_list']
                del data['image_list']

            model = GroupFeeds.objects.model(group_id=group_inst, email=user_inst, **data)
            model.save()

            #add images
            if image_list is not None:
                feed_id = model.__dict__['id']
                FeedImage.objects.add_images(feed_id, image_list)
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED

    def get_home_feeds(self, email):
        group_user_inst = GroupUsers.objects.filter(email=email)
        result = {'session':[], 'normal':[]}
        for item in group_user_inst:
            d = model_to_dict(item)
            group_id = d['group_id']
            result['session'].extend(self.get_session_feeds(group_id))
            result['normal'].extend(self.get_hot_feeds(group_id))

        # leader add

        group_inst_list = Group.objects.filter(group_leader_email=email)
        for group_inst in group_inst_list:
            d = model_to_dict(group_inst)
            group_id = d['id']
            result['session'].extend(self.get_session_feeds(group_id))
            result['normal'].extend(self.get_hot_feeds(group_id))
        return result

    def get_feeds(self, group_id, feed_type=None, k=2):
        group_inst = Group.objects.get(id=group_id)
        if feed_type is None:
            query = GroupFeeds.objects.filter(group_id=group_inst)
        else:
            query = GroupFeeds.objects.filter(group_id=group_inst, feed_type=feed_type)

        result = [model_to_dict(x) for x in query[:k]]
        for item in result:
            item['image_list'] = self.add_image_list(item)
            item['comment_list'] = FeedComment.objects.get_comments_by_feed_id(item['id'])
            item['like_list'] = FeedLike.objects.get_likes_by_feed_id(item['id'])
            item['feed_date'] = item['feed_date'].strftime('')
        return result

    def add_image_list(self, feed_data):
        feed_id = feed_data['id']
        return map(model_to_dict, FeedImage.objects.filter(feed_id=feed_id))

    def add_comment_list(self, feed_data):
        feed_id = feed_data['id']
        result = map(model_to_dict, FeedComment.objects.filter(feed_id=feed_id))
        for item in result:
            item['comment_date'] = item['comment_date'].strftime('%Y-%m-%d %H:%m:%S')
        return result

    def add_like_list(self, feed_data):
        feed_id = feed_data['id']
        result = map(model_to_dict, FeedLike.objects.filter(feed_id=feed_id))
        for item in result:
            item['like_date'] = item['like_date'].strftime('%Y-%m-%d %H:%m:%S')
        return result

    def get_session_feeds(self, group_id, k=2):
        return self.get_feeds(group_id, feed_type='session', k=k)

    def get_hot_feeds(self, group_id, k=2):
        return self.get_feeds(group_id, feed_type='normal', k=k)


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

class UnitedGroupManager(models.Manager):
    def create_united_group(self, data, group_id):
        try:
            model = UnitedGroup.objects.create(**data)
            united_group_id = model.pk
            mid_result = UnitedGroupsBridge.objects.join_united_group(group_id, united_group_id)
            if mid_result == FAILED_TO_EXCEED:
                return FAILED_TO_EXCEED
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED

    def get_united_groups(self, group_id):
        try:
            result = {}
            u_inst = UnitedGroupsBridge.objects.get(group_id=group_id)
            u_group = UnitedGroup.objects.get(id=u_inst.__dict__['united_group_id'])
            u_name = u_group.__dict__['united_group_title']
            result['united_group_title'] = u_name
            result['group_list'] = []
            filtered_obj = UnitedGroupsBridge.objects.filter(united_group_id=u_inst.__dict__['united_group_id'])

            for inst in filtered_obj:
                group_inst = Group.objects.get(id=inst.__dict__['group_id_id'])
                group_id = group_inst.__dict__['id']
                group_name = group_inst.__dict__['group_name']
                group_logo = group_inst.__dict__['group_logo']
                result['group_list'].append({'id':group_id, 'group_name':group_name, 'group_logo':group_logo})
            return result
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED


class UnitedGroup(models.Model):
    united_group_title = models.CharField(max_length=100)
    united_group_description = models.TextField()
    united_group_starting_date = models.DateField(auto_now=True)
    united_group_recruit_state = models.BooleanField(default=False)

    objects = UnitedGroupManager()

    class Meta:
        ordering = ('united_group_starting_date', 'united_group_title',)

    def __unicode__(self):
        return self.united_group_title


class UnitedGroupsBridgeManager(models.Manager):
    def join_united_group(self, group_id, united_group_id):
        try:
            group_inst = Group.objects.get(id=group_id)
            united_group_inst = UnitedGroup.objects.get(id=united_group_id)
            model=UnitedGroupsBridge.objects.model(group_id=group_inst, united_group=united_group_inst)
            model.save()
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED


class UnitedGroupsBridge(models.Model):
    group_id = models.ForeignKey(Group)
    united_group = models.ForeignKey(UnitedGroup)

    objects = UnitedGroupsBridgeManager()

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
    email = models.ForeignKey(UserExtend)
    group_user_level = models.IntegerField(default=0)
    group_gisoo = models.IntegerField(default=1)
    # level_assined

    objects = GroupUserManager()

    class Meta:
        unique_together = ('group_id', 'email', )


class GroupFeeds(models.Model):
    group_id = models.ForeignKey(Group)
    email = models.ForeignKey(UserExtend)
    feed_type = models.CharField(max_length=10)
    feed_title = models.CharField(max_length=100)
    feed_date = models.DateTimeField()#auto_now=True)
    feed_content = models.TextField(blank=True)
    feed_access_modifier = models.IntegerField(default=1)
    feed_tags = models.TextField(blank=True)

    objects = GroupFeedsManager()

    class Meta:
        ordering = ('feed_date',)


class FeedCommentManager(models.Manager):
    def get_comments_by_feed_id(self, feed_id):
        try:
            comment_list = FeedComment.objects.filter(feed_id=feed_id)
            comment_list = map(model_to_dict, comment_list)
            for comment_index in range(len(comment_list)):
                comment_list[comment_index]['comment_date'] = comment_list[comment_index]['comment_date'].strftime('%Y-%m-%d %H:%m:%S')
            return comment_list
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED

    def add_comment(self, data):
        try:
            print data
            feed_id = data['feed_id']
            email = data['email']
            feed_inst = GroupFeeds.objects.get(id=feed_id)
            user_inst = UserExtend.objects.get(email=email)

            del data['feed_id']
            del data['email']

            model = FeedComment.objects.model(feed_id=feed_inst, email=user_inst, **data)
            model.save()
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED


# Feed Additionals : comments, like, multi-saved images
class FeedComment(models.Model):
    feed_id = models.ForeignKey(GroupFeeds)
    email = models.ForeignKey(UserExtend)
    comment_title = models.CharField(max_length=100)
    comment_content = models.TextField(blank=True, default='You should put the content')
    comment_date = models.DateTimeField()

    objects = FeedCommentManager()

    class Meta:
        ordering = ('comment_date',)


class FeedLikeManager(models.Manager):
    def get_likes_by_feed_id(self, feed_id):
        try:
            like_list_temp = FeedLike.objects.filter(feed_id=feed_id)
            like_list = []
            for idx in range(len(like_list_temp)):
                temp = like_list_temp[idx].__dict__
                del temp['_state']
                like_list.append(temp)
            print like_list
            for idx in range(len(like_list)):
                like_list[idx]['like_date'] = like_list[idx]['like_date'].strftime('%Y-%m-%d %H:%m:%S')
            return like_list
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED

    def get_like_count(self, feed_id):
        try:
            like_list = FeedLike.objects.filter(feed_id=feed_id)
            return {'result': len(like_list)}
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED

    def add_like(self, data):
        try:
            feed_id = data['feed_id']
            email = data['email']
            feed_inst = GroupFeeds.objects.get(id=feed_id)
            user_inst = UserExtend.objects.get(email=email)

            del data['feed_id']
            del data['email']

            model = FeedLike.objects.model(feed_id=feed_inst, email=user_inst, **data)
            model.save()
        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED

class FeedLike(models.Model):
    feed_id = models.ForeignKey(GroupFeeds)
    email = models.ForeignKey(UserExtend)
    like_date = models.DateTimeField(auto_now=True)

    objects = FeedLikeManager()

    class Meta:
        ordering = ('like_date',)


class FeedImageManager(models.Manager):
    def get_images_by_feed_id(self, feed_id):
        image_list = FeedImage.objects.filter(feed_id=feed_id)
        return map(model_to_dict, image_list)

    def add_images(self, feed_id, image_list):
        try:
            feed_inst = GroupFeeds.objects.get(id=feed_id)

            for img_data in image_list:
                model = FeedImage.objects.model(feed_id=feed_inst, feed_image=img_data)
                model.save()

        except Exception, e:
            print e.message
            return FAILED_TO_EXCEED
        return SUCCESS_TO_EXCEED


class FeedImage(models.Model):
    feed_id = models.ForeignKey(GroupFeeds)
    feed_image = models.TextField(blank=True)

    objects = FeedImageManager()


class GroupSchedules(models.Model):
    bulletin_id = models.ForeignKey(GroupFeeds)
    schedule_start_date = models.DateTimeField(auto_now=True)
    schedule_end_date = models.DateTimeField(auto_now=True)
    schedule_place = models.CharField(max_length=100)


class GroupUserFollowing(models.Model):
    email = models.ForeignKey(UserExtend)
    group_id = models.ForeignKey(Group)

    class Meta:
        unique_together = ('email', 'group_id', )