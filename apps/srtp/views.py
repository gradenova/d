from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from apps.srtp.models import ProjectCollectIssue,TeacherProjectApply,SignUpStudent,SignUPGroup,ProjectManageIssue,SubmitFile
from apps.user.models import Student,Teacher,UserProfile
from django.conf import settings
import datetime,os
import re
from django.db.models import Q
from functools import wraps
# Create your views here.


class ProjectCollectIssueView(View):
    """
    管理员发布项目征集通告
    """
    def get(self,request):
        collectedItems = TeacherProjectApply.objects.all()
        return render(request,'srtp_publishProjectCollect.html',context={'collectedItems':collectedItems})

    def post(self,request):

        title = request.POST.get('title')
        files = request.FILES.get('fileUpload')      # 得到文件对象
        content = request.POST.get('content')
        deadline = request.POST.get('deadline')
        today = datetime.datetime.today()
        PCI = ProjectCollectIssue( )
        PCI.title = title
        PCI.content = content
        PCI.deadline = deadline
        PCI.to_teacher = True
        if files:
            file_dir = 'media'+ '/%d/%d/%d/' % (today.year, today.month, today.day)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + str(files)
            PCI.Issue_file=file_path
            f = open(file_path,'wb+')
            for chunk in files.chunks():
                f.write(chunk)
            f.close()
        else:
            pass
        PCI.save()
        collectedItems = TeacherProjectApply.objects.all()
        return render(request,'srtp_publishProjectCollect.html',context={'collectedItems':collectedItems})


class SrtpCollectInfoView(View):
    """
    教师看到Srtp项目征集公告
    """
    def get(self,request):                                #获取为教师发布的最后一条通知
        srtp_collect = ProjectCollectIssue.objects.filter(to_teacher=True)
        if srtp_collect.exists():
            srtp_collect = srtp_collect.latest('id')
            file_path = srtp_collect.Issue_file
            result = re.split('/',str(file_path))                #正则获取文档名称
            file_name = result[-1]
        else:
            file_name =''
        return render(request,'srtp_collectProject.html',context={'srtp_collect':srtp_collect,'file_name':file_name})

    def post(self,request):
        title = request.POST.get('title')
        amountPeople = request.POST.get('amountPeople')
        guide_teacher = request.POST.get('teacher')
        info = request.POST.get('intro')
        fileUpload = request.FILES.get('fileUpload')
        file_dir = 'media/' + str(request.user.username)+'/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + str(fileUpload)
        TPA = TeacherProjectApply()
        TPA.title = title
        TPA.amountPeople = amountPeople
        TPA.info = info
        TPA.guide_teacher = guide_teacher
        TPA.fileUpload = file_path
        TPA.teacher_belong = request.user
        TPA.save()
        f = open(file_path,'wb+')
        for chunk in fileUpload.chunks():
            f.write(chunk)
        f.close()
        srtp_collect = ProjectCollectIssue.objects.filter(to_teacher=True).latest('id')
        file_path = srtp_collect.Issue_file
        result = re.split('/',str(file_path))                       #正则获取文档名称
        file_name = result[-1]
        return render(request,'srtp_collectProject.html',context={'srtp_collect':srtp_collect,'file_name':file_name})

class CollectProjectDetailView(View):
    """
    管理员查看教师申报项目的具体详情
    """
    def get(self,request):
        itemID = request.GET['itemID']
        TPA = TeacherProjectApply.objects.get(id=itemID)
        file_name = re.split('/',str(TPA.fileUpload))[-1]
        return render(request,'srtp_collectedProjectDetail.html',context={'collectedProject':TPA,'file_name':file_name})

class DeleteTeaProjectView(View):
    """
    管理员删除教师申报的项目
    """
    def post(self,request):
        itemID = int(request.POST.get('id',''))
        TPA = TeacherProjectApply.objects.get(id = itemID)
        TPA.delete()
        file_path ='/'+str(TPA.fileUpload)
        if os.path.exist(file_path):
            os.remove(file_path)
        return HttpResponse('{"status":"success"}', content_type='application/json')




class SrtpProjectPubilshView(View):
    """
    srtp项目公布，管理员在这里给学生发布具体的申报信息。
    """
    def get(self,request):
        projects = TeacherProjectApply.objects.all()     #这块筛选通过审核的老师的项目
        return render(request,'srtp_publishProject.html',context={'projects':projects})

    def post(self,request):
        title = request.POST.get('title','')
        deadline = request.POST.get('deadline','')
        content  = request.POST.get('content','')
        files = request.FILES.get('fileUpload','')
        today = datetime.datetime.today()
        PCI = ProjectCollectIssue( )
        PCI.title=title
        PCI.content=content
        PCI.deadline=deadline
        PCI.to_student=True
        if files:
            file_dir = 'media'+ '/%d/%d/%d/' % (today.year, today.month, today.day)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + str(files)
            PCI.Issue_file=file_path
            f = open(file_path, 'wb+')
            for chunk in files.chunks():
                f.write(chunk)
            f.close()
        else:
            pass
        PCI.save()
        projects = TeacherProjectApply.objects.all()       # 这块筛选通过审核的老师的项目
        return render(request,'srtp_publishProject.html',context={'projects':projects})


class SrtpProjectSignupView(View):
    """
    学生查看报名通知并在这里进行报名
    """
    def get(self,request):
        srtp_announce = ProjectCollectIssue.objects.filter(to_student= True)
        if srtp_announce.exists():
            srtp_announce = srtp_announce.latest('id')
            file_name = re.split('/',str(srtp_announce.Issue_file))[-1]
        else:
            file_name = ''
        srtp_projects = TeacherProjectApply.objects.all()
        print(srtp_projects)
        return render(request,'srtp_view.html',context={'srtp_announce':srtp_announce,'srtp_projects':srtp_projects,'file_name':file_name})

class SrtpProjectDeatailView(View):
    """
    学生可以在这里查看详细的srtp的项目,并在这里进行报名
    """
    def get(self,request):
        projectID = request.GET['projectID']
        project = TeacherProjectApply.objects.get(id = projectID )
        return  render(request,'srtp_projectSighUp.html',context={'project':project})


class SrtpSignupInfoView(View):
    """
    这里保存学生输入的报名信息,包括报名成员的信息
    """
    def post(self,request):
        projectID = int(request.POST.get('projectID',''))
        numberOfpeople = int(request.POST.get('amountOfMember',1))
        project = TeacherProjectApply.objects.get(id = projectID )
        sug = SignUPGroup.objects.filter(TPA_belong = project)
        if not sug.exists():
            SUG = SignUPGroup.objects.create(TPA_belong = project,apply_people_id= request.user.id)
        else:
            SUG = SignUPGroup.objects.get(TPA_belong= project)
        SUG.amountNumber = numberOfpeople
        SUG.apply_people = request.user
        for i in range(0,numberOfpeople):
            Class = request.POST.get('projectMember[{}][class]'.format(str(i)),'')
            college = request.POST.get('projectMember[{}][college]'.format(str(i)),'')
            realname = request.POST.get('projectMember[{}][name]'.format(str(i)),'')
            stuID = request.POST.get('projectMember[{}][stuID]'.format(str(i)),'')
            StudentInfo = UserProfile.objects.filter(username = stuID )
            if not StudentInfo.exists():                                   #学生身份验证设计，可以放在最后来进行
                return HttpResponse('{"status":"fail"}', content_type='application/json')
            SUS = SignUpStudent.objects.create(Class= Class,college= college,realname= realname,stuID =stuID,project_belong =SUG)
            SUS.save()
        SUG.save()
        return HttpResponse('{"status":"success"}',content_type='application/json')

class SrtpSignupFileView(View):
    """
    学生主要在这里提交自己组的报名材料
    """
    def post(self,request):
        files = request.FILES.get('fileUpload')
        projectID = request.POST.get('projectID','')
        # project = TeacherProjectApply.objects.get(id = projectID )
        sug = SignUPGroup.objects.filter(TPA_belong_id = projectID)
        if not sug.exists():
            sug = SignUPGroup.objects.create(TPA_belong_id = projectID,apply_people_id= request.user.id)
            sug.save()
        SUG = SignUPGroup.objects.get(TPA_belong_id = projectID )
        file_dir = 'media/' + str(SUG.id) + '组项目的报名材料/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + str(files)
        SUG.signup_file = file_path
        SUG.save()
        f = open(file_path, 'wb+')
        for chunk in files.chunks():
            f.write(chunk)
        f.close()
        return  HttpResponseRedirect("/srtp/srtp_view/")

class VerifyProjectTeacherView(View):
    """
    教师看到学生项目申报列表进行项目审核
    """
    def get(self,request):
        TPA = TeacherProjectApply.objects.filter(teacher_belong_id=request.user.id)
        TPA_ID = TPA.values_list('id')      #获取这个老师所有的项目
        TPA_length = len(TPA_ID)
        project_own = [ ]
        for i in range(0,TPA_length):
            SUG = SignUPGroup.objects.filter(TPA_belong_id=TPA_ID[i])
            if SUG.exists():
                project_own.extend(SUG)
        return render(request,'srtp_verifyProjectList.html',context={'verifyItems':project_own})


class VerifyItemView(View):
    """
    教师和管理员在这里对每个项目作出具体的审核
    """
    def post(self,request):
        verify_state = request.POST.get('judge','')
        projectID = request.POST.get('projectID','')
        project = SignUPGroup.objects.get(id = projectID)
        if request.user.is_teacher == 1:
            if verify_state == 'true':
                project.verify_teacher = '通过'
            elif verify_state == 'false':
                project.verify_teacher='不通过'
        else:
            if verify_state == 'true':
                project.verify_admin = '通过'
            elif verify_state == 'false':
                project.verify_admin='不通过'
        project.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')

class VerifyProjectAdminView(View):
    """
    管理员看到学生的申请列表
    """
    def get(self,request):
        SUG = SignUPGroup.objects.filter(verify_teacher__isnull=False)
        return render(request, 'srtp_verifyProjectListAdm.html', context={'verifyItems': SUG})

class ProcessManageAdminView(View):
    """
    管理员进程管理
    """
    def get(self,request):
        PMI = ProjectManageIssue.objects.all().order_by('publishTime')
        return render(request,'srtp_processManage.html',context={'publishedTaskItems':PMI})
class SubmitNewProcessTaskView(View):
    """
    管理员发布新任务
    """
    def post(self,request):
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        deadline = request.POST.get('deadline','')
        kind =request.POST.get('kind','')
        PMI =ProjectManageIssue()
        PMI.title = title
        PMI.deadline =deadline
        PMI.content = content
        PMI.kind = kind
        PMI.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')

class ChangeProcessTaskView(View):
    """
    管理员修改自己发的通知
    """
    def get(self,request):
        IssueID = request.GET['itemID']
        PMI = ProjectManageIssue.objects.get(id = IssueID)
        return render(request,'srtp_processTaskModify.html',context = {'item':PMI})

    def post(self,request):
        title = request.POST.get('title','')
        deadline = request.POST.get('deadline','')
        content = request.POST.get('content','')
        itemID =request.POST.get('itemID',1)
        PMI = ProjectManageIssue.objects.get(id=itemID)
        PMI.title =title
        PMI.content =content
        PMI.deadline =deadline
        PMI.save()
        return render(request, 'srtp_processTaskModify.html', context={'item': PMI})


class ReportProcessTaskView(View):
    """
    教师在这里查看管理员发布的中期任务
    """
    def get(self,request):
        PMI =ProjectManageIssue.objects.all().order_by('publishTime')
        return render(request,'srtp_processCheck.html',context={'processCheckItems':PMI})

class SubmitProcessTaskTeaView(View):
    """
    教师在这里提交具体的每一项中期验收任务
    """
    def get(self,request):
        IssueID = request.GET['itemID']
        PMI = ProjectManageIssue.objects.get(id = IssueID)
        TPA = TeacherProjectApply.objects.get(teacher_belong_id = request.user.id )
        TPA_ID = TPA.id
        SUG =SignUPGroup.objects.filter(TPA_belong_id = TPA_ID )
        return render(request, 'srtp_submitProcessCheck.html', context={'processCheckItem': PMI,'verifyItems':SUG})

class SubmitProccessCheckView(View):
    """
    教师提交每一个项目的中期材料
    """
    def post(self,request):
        kind = request.POST.get('itemKind','')
        TaskID= request.POST.get('TaskID','')
        itemID = int(request.POST.get('itemID',''))
        SUG = SignUPGroup.objects.get(id = itemID )
        process_file = request.FILES.get('fileUpload')
        if kind =='mid':
            SUG.medium_status = '已提交'
        elif kind =='finish':
            SUG.final_status = '已提交'
        SUG.save()
        file_dir = 'media/' + str(SUG.id) + '组项目的报名材料/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + str(process_file)
        f = open(file_path, 'wb+')
        for chunk in process_file.chunks():
            f.write(chunk)
        f.close()
        SF = SubmitFile()
        SF.project_file = file_path
        if kind == 'mid':
            SF.is_medium = True
        elif kind =='finish':
            SF.is_final =True
        SF.SUG_belong_id = itemID
        SF.save()
        return HttpResponseRedirect('/srtp/processCheck?itemID='+str(TaskID))

class StatisticProjectAdmView(View):
    """
    管理员数据统计
    """
    def get(self,request):
        SUG =SignUPGroup.objects.all()
        SUG_medium_pass =SUG.filter(medium_status='已提交')       #中期材料是否提交
        SUG_final_pass = SUG.filter(Q(medium_status='已提交')&Q(final_status='已提交'))   #项目是否结题
        amount_Number = len(SUG)     #总人数
        SUG_medium_Number = len(SUG_medium_pass)
        SUG_final_Number = len(SUG_final_pass)
        if not SUG.exists():
            SUG_medium_percent = "当前没有申报项目"
            SUG_final_percent = "当前没有申报项目"
        else:
            SUG_medium_percent = str( '%.2f %%' % (SUG_medium_Number/amount_Number*100))       #中期验收百分比
            SUG_final_percent =str('%.2f %%' % (SUG_final_Number/amount_Number*100))           #结题百分比
        globalStatistic = {'amountOfPresentProject':amount_Number,'middleExaminePassPercentage':SUG_medium_percent,'completedPercentage':SUG_final_percent}
        return render(request,'srtp_statisticList.html',context={'globalStatistic':globalStatistic,'allProjects':SUG})

class StatistcProjectDetailView(View):
    """
    管理员查看具体某个项目的数据统计
    """
    def get(self,request):
        itemID = request.GET['itemID']
        SUG = SignUPGroup.objects.get(id = itemID)
        if SUG.medium_status =='已提交' and SUG.final_status == '已提交':
            state = '已结题'
        elif SUG.medium_status =='已提交' and SUG.final_status !='已提交':
            state = '中期答辩通过'
        else:
            state = '中期答辩未通过'
        FileList = [ ]
        signup_file_path = SUG.signup_file
        fileobject = {'file_path':signup_file_path,'name':'项目申报材料'}
        FileList.append(fileobject)
        medium_SF = SubmitFile.objects.filter(Q(SUG_belong_id=itemID) & Q(is_medium=True))
        if medium_SF.exists():
            medium_file_path = medium_SF[0].project_file
            fileobject={'file_path':medium_file_path,'name':'中期验收材料'}
            FileList.append(fileobject)
        final_SF  =  SubmitFile.objects.filter(Q(SUG_belong_id=itemID) & Q(is_final=True))
        if final_SF.exists():
            final_file_path = final_SF[0].project_file
            fileobject = {'file_path':final_file_path,'name':'结题验收材料'}
            FileList.append(fileobject)
        return  render(request,'srtp_statisticProjectDetail.html',context={'project':SUG,'state':state,'FileList':FileList})


def permission_forbidden(http_exception=403,next_url='/'):
    """
    Usage:
    @permission_forbidden(403)
    def test(request):
        return HttpResposne('hello world')

    when decorated by permission_forbidden,if the user is not staff,
    it will raise one PerissionDenied exception

    :param http_exception:
    :return:the return value of decorated function
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request,**kwargs):
            if http_exception == 401:         #访问用户是管理员
                if request.user.is_staff:
                    rv = func(request,**kwargs)
                    return rv
                else:
                    return HttpResponseNotFound()    #如果是未登录用户直接返回notfound
            elif http_exception == 402:              #访问用户是教师
                if not request.user.is_authenticated:
                    return HttpResponseRedirect(next_url)
                elif request.user.is_teacher == True:
                    rv = func(request, **kwargs)
                    return rv
                elif request.user.is_student == True:
                    return HttpResponseNotFound( )
                elif request.user.is_teacher == False and request.user.is_student == False:
                    return HttpResponseNotFound()
            elif http_exception == 403:          #访问的用户是学生
                if not request.user.is_authenticated:
                    return HttpResponseRedirect(next_url)
                elif request.user.is_student == True:
                    rv = func(request, **kwargs)
                    return rv
                elif request.user.is_student == True:
                    return HttpResponseNotFound( )
                elif request.user.is_teacher == False and request.user.is_student == False:
                    return HttpResponseNotFound()
            rv = func(request,**kwargs)
            return rv
        return wrapper
    return decorator



