#-*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth import authenticate,login
from django.contrib import auth
from apps.user.forms import LoginForm
from apps.user.models import UserProfile,Teacher,Student,Notice
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.http import StreamingHttpResponse  #下载文件时需要
from apps.srtp.models import ProjectCollectIssue,TeacherProjectApply,ProjectManageIssue
from apps.teaching.models import TeachingInfoNotification
import re
from django.db.models import F
from apps.coursArrange.models import Course,CourseArrange
from templates import *
# Create your views here.

class IndexView(View):
    """
    首页面
    """
    def get(self,request):
        PCI = ProjectCollectIssue.objects.all()              #这些信息是教师和学生都可以看到的信息
        PMI = ProjectManageIssue.objects.all()               #这些是给教师发布的中期验收的信息
        PCI_teacher =PCI.filter(to_teacher=True)
        PCI_student =PCI.filter(to_student=True)
        TIN = TeachingInfoNotification.objects.all()         #这些信息只有教师能够看到
        Info = []
        Notices = Notice.objects.all().order_by('-publishTime')
        if request.user.is_authenticated and request.user.is_teacher==False and request.user.is_student==False:
            Info.extend(PCI)
            Info.extend(TIN)
            userIdentity = 'admin'
            return render(request,'index.html',context={'extendTemplate':'baseAdm.html','generalInformations':Info,'userIdentity':userIdentity,'Notices':Notices})
        elif request.user.is_authenticated and request.user.is_teacher==True:     #教师
            Info.extend(PCI_teacher)
            Info.extend(PMI)
            Info.extend(TIN)
            userIdentity = 'Teacher'
            return render(request,'index.html',context={'extendTemplate':'baseTea.html','generalInformations':Info,'userIdentity':userIdentity,'Notices':Notices})
        elif request.user.is_authenticated and request.user.is_student==True:      #学生
            Info.extend(PCI_student)
            userIdentity = 'Student'
            return render(request, 'index.html', context={'extendTemplate':'baseStu.html','generalInformations':Info,'userIdentity':userIdentity,'Notices':Notices})
        elif ~request.user.is_authenticated:                                      #未登录用户看不到各个项目的通知,但可以看到管理员发布的简短通知
            return render(request,'index.html',context={'extendTemplate':'__base__.html','generalInformations':Info,'Notices':Notices})


class UserLoginView(View):
    """
    用户登录,可以实现多用户身份的登录
    """
    def post(self,request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            identity = request.POST.get('identity','')
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            if identity=='admin':        #管理员登录
                user = authenticate(username = user_name,password = pass_word)
                if user is not None:
                    login(request,user)
                    return HttpResponse('{"status":"success","url":"/"}',content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"用户名或者密码错误"}',content_type='application/json')
            elif identity=='teacher':   #教师登录
                user = authenticate(username = user_name,password = pass_word)
                if user is not None and user.is_teacher:
                    login(request,user)
                    return HttpResponse('{"status":"success","url":"/"}',content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"用户名或者密码错误"}',content_type='application/json')
            elif identity=='student':   #学生登录
                user = authenticate(username = user_name,password = pass_word)
                if user is not None and user.is_student:
                    login(request, user)
                    return HttpResponse('{"status":"success","url":"/"}', content_type='application/json')
                else:
                    return HttpResponse('{"status":"fail","msg":"用户名或者密码错误"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"用户名或者密码格式不正确"}',content_type='application/json')


# class TeacherInfoView(View):
#     """
#     教师信息展示及添加
#     """
#     def get(self,request):
#         return render(request,'infoManage_entryTeacher.html')
class AddUser_TeacherView(View):
    """
    管理员用户添加教师账号,及展示当前用户信息
    """
    def get(self,request):
        teacherList = Teacher.objects.all()
        return render(request,'infoManage_entryTeacher.html',context={'teacherList':teacherList})
    def post(self,request):
        teacher_username = request.POST.get('teaID','')
        teacher_password = teacher_username
        teacher_realname = request.POST.get('teaName','')
        teacher_college= request.POST.get('teaCollege','')
        userprofile = UserProfile()
        userprofile.username = teacher_username
        userprofile.password = make_password(teacher_password)
        userprofile.is_teacher = True
        userprofile.save()
        teacher = Teacher(contract=userprofile, realname=teacher_realname,college=teacher_college)
        teacher.save()
        teacherList = Teacher.objects.all()
        return render(request,'infoManage_entryTeacher.html',context={'teacherList':teacherList,})


class AddUser_StudentView(View):
    """
    管理员用户添加学生账号
    """
    def get(self,request):
        studentList = Student.objects.all()
        return render(request,'infoManage_entryStudent.html',context={'studentList':studentList})
    def post(self,request):
            student_username = request.POST.get('stuID','')
            student_password = student_username
            student_realname = request.POST.get('stuName','')
            student_classname = request.POST.get('stuClass','')
            student_college = request.POST.get('stuCollege', '')
            userprofile = UserProfile()
            userprofile.username = student_username
            userprofile.password = make_password(student_password)
            userprofile.is_student = True
            userprofile.save()
            student = Student(contract = userprofile,realname = student_realname,classname = student_classname,college= student_college)
            student.save()
            studentList = Student.objects.all()
            return render(request, 'infoManage_entryStudent.html', context={'studentList': studentList})

class DeleteUser_TeacherView(View):
    """
    教师用户删除
    """
    def get(self,request):
        DeleteID=request.GET['teaID']
        print(DeleteID)
        Delete_teacher = UserProfile.objects.get(username = DeleteID)
        Delete_teacher.delete()
        teacherList = Teacher.objects.all()
        return render(request,'infoManage_entryTeacher.html',context={'teacherList':teacherList})

class DeleteUser_StudentView(View):
    """
    学生用户删除
    """

    def get(self,request):
        DeleteID=request.GET['stuID']
        Delete_student = UserProfile.objects.get(username = DeleteID)
        Delete_student.delete()
        studentList = Student.objects.all()
        return render(request,'infoManage_entryStudent.html',context={'studentList':studentList})




class UserLogoutView(View):
    """
    用户注销
    """
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect("/")


class courseArrangeView(View):
    """
    教师排课
    """
    def get(self,request):


        return render(request,'courseArrange_Teacher.html')

    def post(self,request):
        return HttpResponse('{"status":"fail","msg":"保存未能成功"}',content_type='application/json')
    # def post(self,request):
    #


def file_download(request):
    """
    文件下载函数功能
    """
    file_path = request.path
    file_path = str(file_path).lstrip('/')
    def file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = file_path
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response

class ReadInformationsView(View):
    """
    首页直接读取通知
    """
    def get(self,request):
        noticeType =  request.GET['noticeType']
        noticeID = request.GET['noticeID']
        if noticeType == 'srtp':                #读取srtp通知
            PCI = ProjectCollectIssue.objects.get(id=noticeID)
            srtp_announce =PCI
            file_name = re.split('/', str(PCI.Issue_file))[-1]
            if request.user.is_teacher:         #当前用户是老师
               return render(request,'srtp_collectProject.html',context={'srtp_collect':PCI,'file_name':file_name})
            elif request.user.is_student:
               srtp_projects = TeacherProjectApply.objects.all()
               return render(request,'srtp_view.html',context={'srtp_announce':srtp_announce,'srtp_projects':srtp_projects,'file_name':file_name})
            else:
                return render(request, 'srtp_collectProject.html',context={'srtp_collect': PCI, 'file_name': file_name})
        elif noticeType =='srtp_process':      #中期任务
            PMI = ProjectManageIssue.objects.all().order_by('publishTime')
            return render(request, 'srtp_processCheck.html', context={'processCheckItems': PMI})
        elif noticeType =='teaching':
            TIN = TeachingInfoNotification.objects.get(id=noticeID)
            file_name = re.split('/', str(TIN.fileUpload))[-1]
            if request.user.is_staff:
                extendTemplate = 'baseAdm.html'
            elif request.user.is_teacher:
                extendTemplate = 'baseTea.html'
            return render(request, 'teaching_informationDetail.html', context={'info': TIN, 'file_name': file_name, 'extendTemplate': extendTemplate})

class PublishNoticeView(View):
    """
    管理员在首页快速发布通知
    """
    def post(self,request):
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        Note =Notice()
        Note.title = title
        Note.content = content
        Note.save()
        return HttpResponseRedirect('/')



class ReadNoticeView(View):
    """
    在这里快速查看管理员发布的简短通知,可以是教师、管理员和学生
    """
    def get(self,request):
        noticeID = request.GET['noticeID']
        Note = Notice.objects.get(id = noticeID)
        if request.user.is_student:
            extendTemplate = 'baseStu.html'
        elif request.user.is_teacher:
            extendTemplate = 'baseTea.html'
        elif request.user.is_staff:
            extendTemplate = 'baseAdm.html'
        return render(request,'index_read.html',context={'notice':Note,'extendTemplate':extendTemplate})


class CourseListAdmView(View):
    """
    管理员查看课程信息
    """
    def get(self,request):
        courseInfoList = Course.objects.all().annotate(
            sid=F('number'),
            theoryHours=F('thyHours')
        )
        courseArrangeList = CourseArrange.objects.all().annotate(
            sid=F('course__number'),
            teacherID=F('teacher__contract__username'),
            teacherName=F('teacher__realname'),
            name=F('course__name'),
            theoryHours=F('course__thyHours'),
            labHours=F('course__labHours')
        ).values(
            'sid', 'teacherID', 'teacherName', 'name', 'theoryHours', 'labHours', 'classes'
        ).distinct()
        return render(request,'infoManageCourse.html',context={'courseInfoList':courseInfoList})











