from django.shortcuts import render
from django.views import View
import os
import time
from datetime import date
from .models import GraduationPaper
from .models import GraduationReportTime
from apps.user.models import Teacher,Student
from django.http import HttpResponse
import json
from django.db.models import F
from django.http import StreamingHttpResponse,FileResponse
from datetime import datetime
from django.utils.http import urlquote
from django.http import HttpResponseRedirect
# Create your views here.

class GraduationAdminDateSetView(View):
    def get(self, request):
        if(len(GraduationReportTime.objects.all())==0):
            graduationtime = GraduationReportTime()
            graduationtime.save()
            graduationtime = GraduationReportTime.objects.all()
            graduationtime = graduationtime[0]
        else:
            graduationtime = GraduationReportTime.objects.all()
            graduationtime = graduationtime[0]
        return render(request, 'graduation_projectDateSetting.html', {'graduationtime': graduationtime})
    def post(self, request):
        submitData = request.POST.get('submitData')
        type = request.POST.get('type')
        # 必须同时输入开始时间与结束时间
        Get1 = submitData[10]
        if Get1.isdigit():  #开始时间非空
            print('哈')
            startDate = submitData[10:20]
            Get2 = len(submitData)
            if Get2 < 38:
                data = {'status': 'fail', 'msg': '结束时间不能为空'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                finishDate = submitData[32:42]
                if list(finishDate) < list(startDate):
                    data = {'status': 'fail', 'msg': '结束时间不能早于开始时间'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    pass
        else:
            data = {'status': 'fail', 'msg': '开始时间不能为空'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        Table = GraduationReportTime.objects.get(id=1)
        if type == 'select':
            Table.DeclareBeginTime = startDate
            Table.DeclareEndTime = finishDate
            Table.save()
        elif type == 'mission':
            Table.TaskBeginTime=startDate
            Table.TaskEndTime=finishDate
            Table.save()
        elif type == 'mid':
            Table.MidtermBeginTime=startDate
            Table.MidtermEndTime=finishDate
            Table.save()
        elif type == 'graduation':
            Table.GraduatinoBeginTime=startDate
            Table.GraduationEndTime=finishDate
            Table.save()
        data = {'status': 'success', 'msg': '保存成功'}
        return HttpResponse(json.dumps(data), content_type='application/json')

class GraduationAdminView(View):
    '''
    管理员查看所有学生的毕设信息
    '''
    def get(self, request):
        projectList = GraduationPaper.objects.all().annotate(
            studentID=F('student__contract__username'),
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            projectID=F('id')
        )
        for temp in projectList:
            if temp.SelectionReport == '':
                temp.state = '未开始'
            elif temp.SelectionReportFormTea == '':
                temp.state = '选题报告已提交'
            elif temp.TaskReport == '':
                temp.state = '选题报告已审核'
            elif temp.TaskReportFormTea == '':
                temp.state = '任务报告已提交'
            elif temp.MidtermReport == '':
                temp.state = '任务报告已审核'
            elif temp.MidtermReportFormTea == '':
                temp.state = '中期报告已提交'
            elif temp.GraduationReport == '':
                temp.state = '中期报告已审核'
            elif temp.GraduationPaperFormTea == '' and temp.GraduationPaperFormAss == '':
                temp.state = '毕业设计报告已提交'
            elif temp.GraduationPaperFormTea != '' or temp.GraduationPaperFormAss:
                if temp.GraduationPaperFormTea and temp.GraduationPaperFormAss == '':
                    temp.state = '指导老师已提交审核报告'
                elif temp.GraduationPaperFormAss != '' and temp.GraduationPaperFormTea == '':
                    temp.state = '评审老师已提交审核报告'
                else:
                    temp.state = '指导老师与评审老师已提交审核报告'
        return render(request, 'graduation_projectListAdm.html', {'projectList': projectList})

class GraduationAdminWatchView(View):
    '''
    管理员查看特定学生的毕设信息
    '''
    def get(self, request):
        projectID = request.GET.get('itemID')
        project = GraduationPaper.objects.filter(id=projectID).annotate(
            studentID=F('student__contract__username'),
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            teacherName=F('teacher__realname'),
            assesserName=F('assesser__realname')
        )
        project = project[0]
        project.SelectionName = str(project.SelectionReport).split('/')[-1]
        project.TaskName = str(project.TaskReport).split('/')[-1]
        project.MidtermName = str(project.MidtermReport).split('/')[-1]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.SelectionBackName = str(project.SelectionReportFormTea).split('/')[-1]
        project.TaskBackName = str(project.TaskReportFormTea).split('/')[-1]
        project.MidtermBackName = str(project.MidtermReportFormTea).split('/')[-1]
        project.GraduationTeaName = str(project.GraduationPaperFormTea).split('/')[-1]
        project.GraduationAssName = str(project.GraduationPaperFormAss).split('/')[-1]
        return render(request, 'graduation_projectDetailAdm.html', {'project': project})

class GraduationStudentView(View):
    '''
    学生查看自己的毕设信息
    '''
    def get(self, request):
        if(len(GraduationPaper.objects.filter(student__contract__username=request.user.username))==0):  #数据库中还未有该名学生的记录
            graduationpaper = GraduationPaper()
            graduationpaper.student = Student.objects.get(contract__username=request.user.username)
            graduationpaper.save()
        project = GraduationPaper.objects.filter(student__contract__username=request.user.username).annotate(
            teacherID=F('teacher__contract__username'),
            assesserID=F('assesser__contract__username'),
            teacherName=F('teacher__realname'),
            assesserName=F('assesser__realname')
        )
        Time = GraduationReportTime.objects.all()
        Time = Time[0]
        project = project[0]
        project.SelectionName = str(project.SelectionReport).split('/')[-1]
        project.TaskName = str(project.TaskReport).split('/')[-1]
        project.MidtermName = str(project.MidtermReport).split('/')[-1]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.SelectionBackName = str(project.SelectionReportFormTea).split('/')[-1]
        project.TaskBackName = str(project.TaskReportFormTea).split('/')[-1]
        project.MidtermBackName = str(project.MidtermReportFormTea).split('/')[-1]
        project.GraduationTeaName = str(project.GraduationPaperFormTea).split('/')[-1]
        project.GraduationAssName = str(project.GraduationPaperFormAss).split('/')[-1]
        if (date.today() >= Time.DeclareBeginTime) & (date.today() <= Time.DeclareEndTime):
            project.DeclareShow = True
        else:
            project.DeclareShow = False
        if (date.today() >= Time.TaskBeginTime) & (date.today() <= Time.TaskEndTime):
            project.TaskShow = True
        else:
            project.TaskShow = False
        if (date.today() >= Time.MidtermBeginTime) & (date.today() <= Time.MidtermEndTime):
            project.MidtermShow = True
        else:
            project.MidtermShow = False
        if (date.today() >= Time.GraduatinoBeginTime) & (date.today() <= Time.GraduationEndTime):
            project.GraduationShow = True
        else:
            project.GraduationShow = False
        return render(request, 'graduation_projectDetailStu.html', {'project': project})
    '''
    学生提交毕设的相关文件及信息
    '''
    def post(self, request):
        type = request.POST.get('type')
        fileSelectItem = request.FILES.get('fileSelectItem')
        fileMission = request.FILES.get('fileMission')
        fileMid = request.FILES.get('fileMid')
        fileGraduate = request.FILES.get('fileGraduate')
        data = {'status': 'success', 'data': '保存成功'}
        if(type):
            submitdata = request.POST.get('submitData')
            if(type=='title'):
                GraduationPaper.objects.filter(student__contract__username=request.user.username).update(title=submitdata)
            elif(type=='myteacher' or type=='otherteacher'):
                if(len(Teacher.objects.filter(contract__username=submitdata))==0):     #数据库中不存在该名教师的记录
                    data['status'] = 'fail'
                    data['data'] = '教师信息或评审教师信息有误'
                else:
                    if(type=='myteacher'):    #更新指导老师
                        result = GraduationPaper.objects.filter(student__contract__username=request.user.username).values('assesser__contract__username')
                        if(len(result) != 0):
                            result = result[0]
                            if(result['assesser__contract__username'] == submitdata):
                                data['status'] = 'fail'
                                data['data'] = '指导老师与评审老师不可以是同一个人'
                            else:
                                GraduationPaper.objects.filter(
                                    student__contract__username=request.user.username).update(
                                    teacher=Teacher.objects.get(contract__username=submitdata))
                        else:
                            GraduationPaper.objects.filter(
                                student__contract__username=request.user.username).update(
                                teacher=Teacher.objects.get(contract__username=submitdata))
                    else:                     #更新评审老师
                        result = GraduationPaper.objects.filter(student__contract__username=request.user.username).values('teacher__contract__username')
                        if(len(result) != 0):
                            result = result[0]
                            if(result['teacher__contract__username'] == submitdata):
                                data['status'] = 'fail'
                                data['data'] = '指导老师与评审老师不可以是同一个人'
                            else:
                                GraduationPaper.objects.filter(
                                    student__contract__username=request.user.username).update(
                                    assesser=Teacher.objects.get(contract__username=submitdata))
                        else:
                            GraduationPaper.objects.filter(
                                student__contract__username=request.user.username).update(
                                assesser=Teacher.objects.get(contract__username=submitdata))
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif(fileSelectItem):    #选题报告
            file_dir = 'graduation/' + str(request.user.username) + '/TitleReport/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileSelectItem)
            GraduationPaper.objects.filter(student__contract__username=request.user.username).update(SelectionReport=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileSelectItem.chunks():
                f.write(chunk)
            f.close()
        elif(fileMission):        #任务报告
            file_dir = 'graduation/' + str(request.user.username) + '/TaskReport/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileMission)
            GraduationPaper.objects.filter(student__contract__username=request.user.username).update(TaskReport=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileMission.chunks():
                f.write(chunk)
            f.close()
        elif(fileMid):             #中期报告
            file_dir = 'graduation/' + str(request.user.username) + '/MidtermReport/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileMid)
            GraduationPaper.objects.filter(student__contract__username=request.user.username).update(MidtermReport=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileMid.chunks():
                f.write(chunk)
            f.close()
        elif(fileGraduate):        #毕业设计报告
            file_dir = 'graduation/' + str(request.user.username) + '/GraduationPaper/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileGraduate)
            GraduationPaper.objects.filter(student__contract__username=request.user.username).update(GraduationReport=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileGraduate.chunks():
                f.write(chunk)
            f.close()
        #重新对数据库进行查询操作，返回前端
        project = GraduationPaper.objects.filter(student__contract__username=request.user.username).annotate(
            teacherID=F('teacher__contract__username'),
            assesserID=F('assesser__contract__username')
        )
        project = project[0]
        project.SelectionName = str(project.SelectionReport).split('/')[-1]
        project.TaskName = str(project.TaskReport).split('/')[-1]
        project.MidtermName = str(project.MidtermReport).split('/')[-1]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.SelectionBackName = str(project.SelectionReportFormTea).split('/')[-1]
        project.TaskBackName = str(project.TaskReportFormTea).split('/')[-1]
        project.MidtermBackName = str(project.MidtermReportFormTea).split('/')[-1]
        project.GraduationTeaName = str(project.GraduationPaperFormTea).split('/')[-1]
        project.GraduationAssName = str(project.GraduationPaperFormAss).split('/')[-1]
        Time = GraduationReportTime.objects.all()
        Time = Time[0]
        if (date.today() >= Time.DeclareBeginTime) & (date.today() <= Time.DeclareEndTime):
            project.DeclareShow = True
        else:
            project.DeclareShow = False
        if (date.today() >= Time.TaskBeginTime) & (date.today() <= Time.TaskEndTime):
            project.TaskShow = True
        else:
            project.TaskShow = False
        if (date.today() >= Time.MidtermBeginTime) & (date.today() <= Time.MidtermEndTime):
            project.MidtermShow = True
        else:
            project.MidtermShow = False
        if (date.today() >= Time.GraduatinoBeginTime) & (date.today() <= Time.GraduationEndTime):
            project.GraduationShow = True
        else:
            project.GraduationShow = False
        return render(request, 'graduation_projectDetailStu.html', {'project': project})

class GraduationTeacherView(View):
    '''
    教师查看自己作为指导教师及评审教师的学生毕设信息
    '''
    def get(self, request):
        teacherID = request.user.username
        projectList_tutor = GraduationPaper.objects.filter(teacher__contract__username=teacherID).annotate(
            studentID=F('student__contract__username'),
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            projectID=F('id')
        )
        for temp in projectList_tutor:
            print(temp.SelectionReportFormTea == '')
            if temp.SelectionReport == '':
                temp.state = '未开始'
            elif temp.SelectionReportFormTea == '':
                temp.state = '选题报告已提交'
            elif temp.TaskReport == '':
                temp.state = '选题报告已审核'
            elif temp.TaskReportFormTea == '':
                temp.state = '任务报告已提交'
            elif temp.MidtermReport == '':
                temp.state = '任务报告已审核'
            elif temp.MidtermReportFormTea == '':
                temp.state = '中期报告已提交'
            elif temp.GraduationReport == '':
                temp.state = '中期报告已审核'
            elif temp.GraduationPaperFormTea == '' and temp.GraduationPaperFormAss == '':
                temp.state = '毕业设计报告已提交'
            elif temp.GraduationPaperFormTea != '' or temp.GraduationPaperFormAss:
                if temp.GraduationPaperFormTea and temp.GraduationPaperFormAss == '':
                    temp.state = '指导老师已提交审核报告'
                elif temp.GraduationPaperFormAss != '' and temp.GraduationPaperFormTea == '':
                    temp.state = '评审老师已提交审核报告'
                else:
                    temp.state = '指导老师与评审老师已提交审核报告'
        projectList_otherTeacher = GraduationPaper.objects.filter(assesser__contract__username=teacherID).annotate(
            studentID=F('student__contract__username'),
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            projectID=F('id')
        )
        for temp in projectList_otherTeacher:
            if temp.GraduationPaperFormAss == '':
                temp.state = '未评阅'
            else:
                temp.state = '已评阅'
        return render(request, 'graduation_projectListTea.html', {'projectList_tutor': projectList_tutor, 'projectList_otherTeacher': projectList_otherTeacher})

class GraduationTeacherTutorView(View):
    '''
    教师查看自己作为指导教师的指定学生毕设信息
    '''
    def get(self, request):
        projectID = request.GET.get('itemID')
        project = GraduationPaper.objects.filter(id=projectID).annotate(
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            studentID=F('student__contract__username'),
            projectID=F('id')
        )
        project = project[0]
        project.SelectionName = str(project.SelectionReport).split('/')[-1]
        project.TaskName = str(project.TaskReport).split('/')[-1]
        project.MidtermName = str(project.MidtermReport).split('/')[-1]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.SelectionRemarkName = str(project.SelectionReportFormTea).split('/')[-1]
        project.TaskRemarkName = str(project.TaskReportFormTea).split('/')[-1]
        project.MidtermRemarkName = str(project.MidtermReportFormTea).split('/')[-1]
        project.GraduationRemarkTeaName = str(project.GraduationPaperFormTea).split('/')[-1]
        return render(request, 'graduation_projectDetailCheckTea.html', {'project': project})
    '''
    教师提交审核的相关信息及文件
    '''
    def post(self, request):
        projectID = request.GET.get('itemID')
        studentID = request.GET.get('studentID')
        result = request.POST.get('optionsRadios')
        fileSelectItem = request.FILES.get('fileSelectItem')
        fileMission = request.FILES.get('fileMission')
        fileMid = request.FILES.get('fileMid')
        fileGraduate = request.FILES.get('fileGraduate')
        if(fileSelectItem):
            if(result=='pass'):
                GraduationPaper.objects.filter(id=projectID).update(SelectionReportPass='通过')
            else:
                GraduationPaper.objects.filter(id=projectID).update(SelectionReportPass='未通过')
            file_dir = 'graduation/' + str(studentID) + '/SelectionRemark/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileSelectItem)
            GraduationPaper.objects.filter(id=projectID).update(SelectionReportFormTea=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileSelectItem.chunks():
                f.write(chunk)
            f.close()
        elif(fileMission):
            if(result=='pass'):
                GraduationPaper.objects.filter(id=projectID).update(TaskReportPass='通过')
            else:
                GraduationPaper.objects.filter(id=projectID).update(TaskReportPass='未通过')
            file_dir = 'graduation/' + str(studentID) + '/TaskRemark/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileMission)
            GraduationPaper.objects.filter(id=projectID).update(TaskReportFormTea=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileMission.chunks():
                f.write(chunk)
            f.close()
        elif(fileMid):
            if(result=='pass'):
                GraduationPaper.objects.filter(id=projectID).update(MidtermReportPass='通过')
            else:
                GraduationPaper.objects.filter(id=projectID).update(MidtermReportPass='未通过')
            file_dir = 'graduation/' + str(studentID) + '/MidtermRemark/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileMid)
            GraduationPaper.objects.filter(id=projectID).update(MidtermReportFormTea=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileMid.chunks():
                f.write(chunk)
            f.close()
        elif(fileGraduate):
            if(result=='pass'):
                GraduationPaper.objects.filter(id=projectID).update(GraduationPaperPass='通过')
            else:
                GraduationPaper.objects.filter(id=projectID).update(GraduationPaperPass='未通过')
            file_dir = 'graduation/' + str(studentID) + '/GraduationTeaRemark/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            else:
                file = os.listdir(file_dir)
                os.remove(file_dir + file[0])
            file_path = file_dir + str(fileGraduate)
            GraduationPaper.objects.filter(id=projectID).update(GraduationPaperFormTea=file_path)
            f = open(file_path, 'wb+')
            for chunk in fileGraduate.chunks():
                f.write(chunk)
            f.close()
        project = GraduationPaper.objects.filter(id=projectID).annotate(
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            studentID=F('student__contract__username'),
            projectID=F('id')
        )
        project = project[0]
        project.SelectionName = str(project.SelectionReport).split('/')[-1]
        project.TaskName = str(project.TaskReport).split('/')[-1]
        project.MidtermName = str(project.MidtermReport).split('/')[-1]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.SelectionRemarkName = str(project.SelectionReportFormTea).split('/')[-1]
        project.TaskRemarkName = str(project.TaskReportFormTea).split('/')[-1]
        project.MidtermRemarkName = str(project.MidtermReportFormTea).split('/')[-1]
        project.GraduationRemarkTeaName = str(project.GraduationPaperFormTea).split('/')[-1]
        return render(request, 'graduation_projectDetailCheckTea.html', {'project': project})

class GraduationTeacherOtherView(View):
    '''
    教师查看自己作为评审教师的指定学生毕设信息
    '''
    def get(self, request):
        projectID = request.GET.get('itemID')
        project = GraduationPaper.objects.filter(id=projectID).annotate(
            studentName=F('student__realname'),
            studentClass=F('student__classname'),
            studentID=F('student__contract__username')
        )
        project = project[0]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.GraduationRemarkAssName = str(project.GraduationPaperFormAss).split('/')[-1]
        return render(request, 'graduation_projectDetailVerifyTea.html', {'project': project})
    '''
    教师提交评审的相关信息及文件
    '''
    def post(self, request):
        studentID = request.GET.get('studentID')
        projectID = request.GET.get('projectID')
        remarkfile = request.FILES.get('fileUpload')
        file_dir = 'graduation/' + str(studentID) + 'GraduationRemarkAss'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        else:
            file = os.listdir(file_dir)
            os.remove(file_dir + file[0])
        file_path = file_dir + str(remarkfile)
        GraduationPaper.objects.filter(id=projectID).update(GraduationPaperFormAss=file_path)
        f = open(file_path, 'wb+')
        for chunk in remarkfile.chunks():
            f.write(chunk)
        f.close()
        project = GraduationPaper.objects.filter(id=projectID).annotate(
            studentName=F('stduent__realname'),
            studentClass=F('student__classname'),
            studentID=F('student__contract__username')
        )
        project = project[0]
        project.GraduationName = str(project.GraduationReport).split('/')[-1]
        project.GraduationRemarkAssName = str(project.GraduationPaperFormAss).split('/')[-1]
        return render(request, 'graduation_projectDetailVerifyTea.html', {'project', project})

#文件下载
def DownloadFile(request):
    file_path = request.path
    file_path = str(file_path).replace('/graduation/download/', '')
    def file_iterator(file_name, chunk_size=512):
        with open(file_name, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    the_file_name = file_path
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    # response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(the_file_name.split('/')[-1]))
    response['Content-Disposition'] = 'attachment;filename="%s"' % the_file_name.split('/')[-1]
    return response