from django.db import models
import django.contrib.auth.models
from typing import List
import minsta

class Post(models.Model):
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE)
    file_path = models.FilePathField()
    comment = models.TextField()
    cafe = models.ForeignKey('Cafe', related_name='posts', on_delete=models.CASCADE) 
    posted_at = models.DateField(auto_now=True)

    @classmethod
    def list(cls):
        return cls.objects.order_by('-id').all()

    @classmethod
    def list_orderby_cafe(cls):
        return cls.objects.order_by('-cafe').all()

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.filter(user=user)

    @classmethod
    def get_latest3_photos(cls, cafe_id):
        return cls.objects.filter(cafe_id=cafe_id)[:3]



    @classmethod
    def create(cls, user, file_path, comment, cafe):
        # 左がcreateの引数名,右が引数に与えたい値
        # createはキーワード引数でないといけない。理由は、file_pathが第一引数でないと指定していない以上Djangoは特定できないから
        Post.objects.create(user=user, file_path=file_path, comment=comment, cafe_id=cafe)


class ProvisionalUser(models.Model):
    register_uuid = models.TextField() # TODO:uniqueにする
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now=True)


    @classmethod
    def create(cls, register_uuid, email):
        ProvisionalUser.objects.create(register_uuid=register_uuid, email=email)

    @classmethod
    def get_by_uuid(cls, register_uuid):
        return cls.objects.get(register_uuid=register_uuid)

    @classmethod
    def get_older_than(cls, datetime)-> List['ProvisionalUser']:
        return cls.objects.filter(created_at__lte=datetime)


class ForgetPasswordUser(models.Model):
    user_id = models.ForeignKey(django.contrib.auth.models.User, on_delete=models.CASCADE) #TODO: uniqueにする
    register_uuid = models.TextField() # TODO:uniqueにする
    email = models.EmailField() 
    created_at = models.DateTimeField(auto_now=True) # auto_now=True, 

    @classmethod
    def create(cls, register_uuid, email, user_id):
        ForgetPasswordUser.objects.create(register_uuid=register_uuid, email=email, user_id=user_id)

    @classmethod
    def get_by_uuid(cls, register_uuid):
        return cls.objects.get(register_uuid=register_uuid)

    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.objects.get(user_id=user_id)

    @classmethod
    def get_older_than(cls, datetime)-> List['ForgetPasswordUser']:
        return cls.objects.filter(created_at__lte=datetime)
    

class Cafe(models.Model):
    location = models.TextField(blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    cafe_name = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    hp = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    work_time = models.TextField(blank=True)
    area = models.TextField(blank=True)
    

    @classmethod
    def get_by_id(cls, id):
        return cls.objects.get(id=id)

    @classmethod
    def list(cls):
        return cls.objects.order_by('-id').all()


    @classmethod
    def get_cafe_id(cls):
        return cls.objects.order_by('-id').values('id')

    
    
    @classmethod
    def cafe_name_list(cls,id):
        return cls.objects.order_by('-id').filter(id=id).values('id', 'cafe_name')

    
class ProvisionalRegistrationCafe(models.Model):
    location = models.TextField(blank=True)
    cafe_name = models.TextField(blank=True)
    comment = models.TextField(blank=True)
    hp = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    work_time = models.TextField(blank=True)
    area = models.TextField(blank=True)
 





        
        
