from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):

    #is_admin = models.BooleanField(default=False)

    is_teacher = models.BooleanField(default=False)

    is_student = models.BooleanField(default=False)

class Teacher(models.Model):

    contract = models.OneToOneField(UserProfile,on_delete=models.CASCADE, primary_key=True)

    realname = models.CharField(max_length=30, default=u'佚名大侠', verbose_name=u'姓名')  #教师的真实姓名

    college = models.CharField(max_length=20, default='', verbose_name=u'学院')  #教师的所属学院


class Student(models.Model):
    contract = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)

    realname = models.CharField(max_length=30, default=u'佚名大侠', verbose_name=u'姓名')

    classname=models.CharField(max_length=10,default='',verbose_name=u'班级名称')

    college=models.CharField(max_length=20,default='',verbose_name=u'学院')

class Notice(models.Model):

    title = models.CharField(max_length=50,default='',verbose_name=u'标题')

    content = models.TextField(max_length=1000,default='',verbose_name=u'发布内容')

    publishTime = models.DateTimeField(auto_now_add=True,verbose_name=u'发布时间',null=True, blank=True)















# class teacher_
# # class FileProfile(models.Model):
# #     username=models.CharField('')
#
#
#
# class teacher_requirement(models.Model):
#

# class teacher_course_table(models.Model):
#