from django.db import models
from apps.user.models import Teacher

# Create your models here.

class Course(models.Model):
    number = models.IntegerField(default=0)              #课程编号

    name = models.CharField(max_length=15)               #课程名字

    thyHours = models.IntegerField(default=0)            #课程理论课学时

    labHours = models.IntegerField(default=0)            #课程实验课学时

    class Meta:
        db_table = 'Course'

class ClassRoom(models.Model):
    building = models.CharField(max_length=3, null=True)           #楼宇

    number = models.IntegerField(default=0)              #教室编号

    useage = models.CharField(max_length=4, null=True)              #用途

    class Meta:
        db_table = 'ClassRoom'

class CourseArrange(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  #课程

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) #教师

    classes = models.CharField(null=True, max_length=15)           #上课班级

    laborthy = models.BooleanField(default=False)                  #是否为该门课的实验课，默认不是

    watch = models.BooleanField(default=False)                     #是否允许教师查看，默认不允许

    place = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True)  #地点

    week = models.IntegerField(default=0)                           #第几周

    day = models.IntegerField(default=0)                            #星期几

    number = models.IntegerField(default=0)                         #第几节

    class Meta:
        db_table = 'CourseArrange'


class CourseOtherDemand(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  #课程

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) #教师

    classes = models.CharField(null=True, max_length=15) #上课班级

    demand = models.CharField(max_length=50,default='')            #其它需求

    class Meta:
        db_table  = 'CourseOtherDemand'
