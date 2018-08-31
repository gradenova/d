from django.db import models
from apps.user.models import Teacher,UserProfile

# Create your models here.

class ProjectCollectIssue(models.Model):      #管理员发布的项目征集通告,给教师和给学生

    title = models.CharField(max_length=100, default='', verbose_name=u'标题')

    deadline = models.DateField(null=True, blank=True, verbose_name=u'截止时间')

    content = models.TextField(max_length=500, default='', verbose_name=u'发布内容')

    Issue_file = models.FileField(upload_to='Issue_file/%Y/%m', default='')

    to_teacher = models.BooleanField(default=False)

    to_student = models.BooleanField(default=False)

    noticeType = models.CharField(max_length= 10,default='srtp',verbose_name=u'通知类型')



class ProjectManageIssue(models.Model):       #管理员发布的给教师的进程汇报的通告

    title = models.CharField(max_length= 100,default='', verbose_name=u'标题')

    deadline = models.DateField(null=True, blank=True, verbose_name=u'截止时间')

    content = models.TextField(max_length=500, default='', verbose_name=u'发布内容')

    publishTime = models.DateField(auto_now_add=True,verbose_name=u'发布时间')

    kind = models.CharField(max_length = 5,default='',verbose_name=u'通告属性')

    noticeType = models.CharField(max_length= 20,default='srtp_process',verbose_name=u'通知类型')



class TeacherProjectApply(models.Model):     #教师用户申请的项目

    title = models.CharField(max_length=100, default='', verbose_name=u'标题')

    amountPeople = models.IntegerField(default=1, verbose_name=u'项目总人数')

    guide_teacher = models.CharField(max_length=10,default='',verbose_name=u'指导老师')

    info = models.TextField(max_length=500, default='', verbose_name=u'简介')

    fileUpload = models.FileField(upload_to='fileUpload/%Y/%m', default='')

    teacher_belong = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name=u'发布教师')

    # pass_status = models.BooleanField(default= True)      #申请项目的管理员审核是否通过

class SignUPGroup(models.Model):            #每个组申请的项目

    amountNumber = models.IntegerField(default=1, verbose_name=u'项目总人数')

    signup_file =  models.FileField(upload_to='signup_file/%Y/%m', default='')    #报名材料

    TPA_belong = models.ForeignKey(TeacherProjectApply,on_delete=models.CASCADE,verbose_name=u'报名的项目')

    apply_people = models.ForeignKey(UserProfile ,on_delete = models.CASCADE,verbose_name=u'申请人')

    verify_teacher = models.CharField(max_length=10,default='',verbose_name=u'教师审核意见')

    verify_admin = models.CharField(max_length=10, default='', verbose_name=u'管理员审核意见')

    medium_status = models.CharField(max_length=10,default='',verbose_name=u'中期文件提交状态')

    final_status = models.CharField(max_length=10, default='', verbose_name=u'结题文件提交状态')


class SubmitFile(models.Model):                                       #项目的提交材料

    SUG_belong = models.ForeignKey(SignUPGroup,on_delete = models.CASCADE,verbose_name=u'所属组')

    project_file = models.FileField(upload_to='medium_file/%Y/%m', default='')     #材料

    is_medium = models.BooleanField(default=False)

    is_final = models.BooleanField(default=False)








    # have_verified_teacher = models.BooleanField(default= False)  #教师是否已经审核过
    #
    # verify_admin = models.BooleanField(default= False)           #管理员审核意见
    #
    # have_verified_admin = models.BooleanField(default=False)     #管理员是否审核过



class SignUpStudent(models.Model):

    stuID = models.CharField(max_length=20,default='',verbose_name=u'学号')

    Class = models.CharField(max_length=10,default='',verbose_name=u'班级')

    college = models.CharField(max_length=20,default='',verbose_name=u'学院')

    realname = models.CharField(max_length=10,default='',verbose_name=u'真实姓名')

    project_belong = models.ForeignKey(SignUPGroup,on_delete=models.CASCADE,verbose_name=u'所属的报名组')
















