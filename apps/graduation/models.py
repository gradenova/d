from django.db import models
from apps.user.models import Student,Teacher

# Create your models here.
class GraduationPaper(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)  #学生

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='teacher')      #指导教师

    assesser = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, related_name='asserser')    #评审教师

    title = models.CharField(default='无题目', max_length=20)          #题目

    SelectionReport = models.FileField(null=True)                      #选题报告

    TaskReport = models.FileField(null=True)                           #任务报告

    MidtermReport = models.FileField(null=True)                        #中期报告

    GraduationReport = models.FileField(null=True)                     #毕业设计报告

    SelectionReportFormTea = models.FileField(null=True)               #选题报告审核表(教师)

    TaskReportFormTea = models.FileField(null=True)                    #任务报告审核表(教师)

    MidtermReportFormTea = models.FileField(null=True)                 #中期报告审核表(教师)

    GraduationPaperFormTea = models.FileField(null=True)               #毕业设计报告审核表(教师)

    GraduationPaperFormAss = models.FileField(null=True)               #毕业设计报告审核表(评审人)

    SelectionReportPass = models.CharField(default='', max_length=3)   #选题报告是否通过

    TaskReportPass = models.CharField(default='', max_length=3)        #任务报告是否通过

    MidtermReportPass = models.CharField(default='', max_length=3)     #中期报告是否通过

    GraduationPaperPass = models.CharField(default='', max_length=3)   #毕业设计报告是否通过

    class Media:
        db_table = 'GraduationPaper'

class GraduationReportTime(models.Model):
    DeclareBeginTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                              #申报开始时间

    DeclareEndTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                                #申报截止时间

    TaskBeginTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                                 #任务报告提交开始时间

    TaskEndTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                                   #任务报告提交截止时间

    MidtermBeginTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                              #中期报告提交开始时间

    MidtermEndTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                                #中期报告提交截止时间

    GraduatinoBeginTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                           #毕业设计报告提交开始时间

    GraduationEndTime = models.DateField(auto_now=False, auto_now_add=False, default='2050-01-01')                             #毕业设计报告提交截止时间

    class Media:
        db_table = 'GraduationReportTime'