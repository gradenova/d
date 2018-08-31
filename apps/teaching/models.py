from django.db import models
from apps.user.models import Teacher, UserProfile
# Create your models here.

class TeachingInfoNotification(models.Model):     #管理员发布的教研信息通知

    CATEGORY_CHOICE = (
        (u'reform', u'教改'),
        (u'textbook', u'教材'),
        (u'research', u'教研'),
        (u'else', u'其他'),
    )

    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE, verbose_name=u'项目分类')

    title = models.CharField(max_length= 100,default='',verbose_name=u'标题')

    content = models.TextField(max_length = 500,default='',verbose_name=u'内容')

    fileUpload = models.FileField(upload_to='fileUpload/%Y/%m', default='')

    publishTime = models.DateField(auto_now_add=True,verbose_name=u'发布时间',null=True, blank=True)

    noticeType = models.CharField(max_length=10,default='teaching',verbose_name=u'通知类型')



class TeachingProjectApply(models.Model):   # 教师申请的项目

    title = models.CharField(max_length=100, default='', verbose_name=u'题目')

    category = models.CharField(max_length=10, choices=(('reform', '教改'), ('research', '教研'), ('textbook', '教材'), ('other', '其他')), default='reform', verbose_name=u'项目类型')

    applicant = models.CharField(max_length=10, default='', verbose_name=u'申请人')

    belongTea = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default='', verbose_name=u'所属教师')

    funds = models.IntegerField(default=0, verbose_name=u'经费')

    intro = models.CharField(max_length=500, default='', verbose_name=u'简介')

    process = models.CharField(max_length=10, default='', verbose_name=u'项目进度')

    apply_time = models.DateField(auto_now_add=True,verbose_name=u'申请时间',null=True, blank=True)

    apply_status = models.CharField(max_length= 10,verbose_name=u'申报审核结果',null= True)

    medium_status = models.CharField(max_length= 10, verbose_name=u'中期审核结果', null=True)

    final_status = models.CharField(max_length= 10, verbose_name=u'结题审核结果', null=True)

    apply_verify_time = models.DateField(null=True, blank=True, verbose_name=u'申报审核时间')

    medium_verify_time =models.DateField(null=True, blank=True, verbose_name=u'中期审核时间')

    final_verify_time = models.DateField(null=True, blank=True, verbose_name=u'结题审核时间')

    extra_file = models.CharField(max_length= 100,default='',verbose_name=u'文件路径备用域')

    funds_record = models.TextField(max_length = 1000,default='',verbose_name=u'经费使用记录' )

    achievements_record = models.TextField(max_length=1000,default='',verbose_name=u'成果记录')



class SubmitFile(models.Model):                                 #教师教学教研项目的提交文件

    TPA_belong = models.ForeignKey(TeachingProjectApply,on_delete = models.CASCADE,verbose_name=u'所属项目')

    project_file = models.FileField(upload_to='project_file/%Y/%m', default='')                   #材料

    file_name = models.CharField(max_length= 50,default='',verbose_name=u'文件名')

    is_apply = models.BooleanField(default=False)

    is_medium = models.BooleanField(default=False)          #是否是中期文件

    is_final = models.BooleanField(default=False)           #是否是结题文件

# class FundsRecord(models.Model):    #项目使用经费记录
#
#     content = models.TextField(max_length=500,default='',verbose_name=u'使用经费具体记录')
#
#     TPA_belong = models.ForeignKey(TeachingProjectApply,on_delete = models.CASCADE,verbose_name=u'所属项目')
#
#     record_time = models.DateField(auto_now_add=True,verbose_name=u'提交时间',null=True, blank=True)
#
# class AchievementsRecord(models.Model):  #成果记录
#
#     content = models.TextField(max_length=500,default='',verbose_name=u'成果具体记录')
#
#     TPA_belong = models.ForeignKey(TeachingProjectApply,on_delete = models.CASCADE,verbose_name=u'所属项目')
#
#     record_time = models.DateField(auto_now_add=True,verbose_name=u'提交时间',null=True, blank=True)


