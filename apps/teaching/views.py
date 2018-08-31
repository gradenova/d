from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseNotFound
from apps.teaching.models import TeachingInfoNotification,TeachingProjectApply,SubmitFile
import os,re,datetime
from django.db.models import Q

class InformationPublishView(View):
    """
    管理员在这里发布教研教改项目的通知
    """
    def get(self,request):
        TIN =TeachingInfoNotification.objects.all()
        return render(request,'teaching_publishInformation.html',context={'publishedInfomationList':TIN})
    def post(self,request):
        category = request.POST.get('category','')
        title = request.POST.get('title','')
        content = request.POST.get('content','')
        fileUpload = request.FILES.get('fileUpload')
        TIN =TeachingInfoNotification()
        TIN.category = category
        TIN.content = content
        TIN.title = title
        if fileUpload:
            file_dir = 'media/teaching/'+str(category)+'类项目的通知/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + str(fileUpload)
            f = open(file_path, 'wb+')
            for chunk in fileUpload.chunks():
                f.write(chunk)
            f.close()
            TIN.fileUpload =file_path
        else:
            pass
        TIN.save()
        return HttpResponseRedirect('/teaching/informationPublish/')

class InformationPublishDetailView(View):
    """
    管理员和教师在这里查看历史信息的详细内容，其中根据请求的人不同会渲染不同的父类模板
    """
    def get(self,request):
        itemID = request.GET['itemID']
        TIN =TeachingInfoNotification.objects.get(id = itemID)
        file_name = re.split('/', str(TIN.fileUpload))[-1]
        if request.user.is_staff:
            extendTemplate = 'baseAdm.html'
        elif request.user.is_teacher:
            extendTemplate = 'baseTea.html'
        return render(request,'teaching_informationDetail.html',context={'info':TIN,'file_name':file_name,'extendTemplate':extendTemplate})

class DeleteInfoView(View):
    """
    管理员删除发布的历史信息
    """
    def get(self,request):
        itemID = request.GET['itemID']
        TeachingInfoNotification.objects.get(id = itemID).delete()
        return HttpResponseRedirect('/teaching/informationPublish/')


class TeacherInformationListView(View):
    """
    进入教师信息中心
    """
    def get(self, request):
        TIN = TeachingInfoNotification.objects.all()
        return render(request, 'teaching_informationListTea.html',context={'publishedInfomationList':TIN})

class ProjectApplyView(View):
    """
    进入教师申请教学项目页面
    """
    def get(self, request):
        return render(request, 'teaching_applyProject.html')
    def post(self, request):
        title = request.POST.get('title')
        fileUpload = request.FILES.get('fileUpload')
        category = request.POST.get('category')
        applicant = request.POST.get('applicant')
        funds = request.POST.get('funds')
        intro = request.POST.get('intro')
        TPA = TeachingProjectApply()
        TPA.title = title
        TPA.category = category
        TPA.applicant = applicant
        TPA.belongTea = request.user
        TPA.funds = funds
        TPA.intro = intro
        TPA.process = '项目申请'
        TPA.save()
        if fileUpload:
            file_dir = 'media/teaching/'+str(request.user.username)+'老师申请的项目/'
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            file_path = file_dir + str(fileUpload)
            SF =SubmitFile()
            SF.project_file = file_path
            SF.file_name= re.split('/', str(file_path))[-1]
            SF.is_apply = True
            SF.TPA_belong =TPA
            SF.save()
            f = open(file_path, 'wb+')
            for chunk in fileUpload.chunks():
                f.write(chunk)
            f.close()
        else:
            pass
        project = TeachingProjectApply.objects.filter(belongTea_id=request.user.id)
        return render(request, 'teaching_myProjectList.html', context={'projects': project})

class ProjectSelectView(View):
    """
    管理员在这里进入项目评选的页面
    """
    def get(self,request):
        TPA = TeachingProjectApply.objects.filter(apply_status__isnull=True)
        TPA_verified = TeachingProjectApply.objects.filter(apply_status__isnull=False)
        for item in TPA:
            if item.submitfile_set.filter(is_apply= True).exists():
                item.extra_file= item.submitfile_set.filter(is_apply= True)[0].project_file
                item.save()
            else:                      #如果有申请文件的话，就获取文件
                pass
        for item in TPA_verified:
            if item.submitfile_set.filter(is_apply= True):
                item.extra_file = item.submitfile_set.filter(is_apply= True)[0].project_file
                item.save()
            else:
                pass
        return render(request,'teaching_verifyProjectListAdm.html',context={'verifyItems':TPA,'verifiedItems':TPA_verified })

class VerifyItemAdmView(View):
    """
    管理员在这里审核某个具体的项目,初步设置为申报阶段的项目审核
    """
    def get(self,request):
        itemID = request.GET['itemID']
        TPA =TeachingProjectApply.objects.get(id = itemID)
        verifyTask = {}
        verifyTask['type'] ='项目申请'
        file_path = TPA.submitfile_set.get(is_apply=True).project_file
        file_name = re.split('/', str(file_path))[-1]
        files ={'file_path':file_path,'file_name':file_name}
        return  render(request,'teaching_verifySingleProjectAdm.html',context={'verifyTask':verifyTask,'project':TPA,'files':files})

class TeachingJudgeAdmView(View):
    """
    管理员在这里发出项目申报评审的结果
    """
    def post(self,request):
        type = request.POST.get('type','')
        optionsRadios = request.POST.get('optionsRadios', '')
        projectID = int(request.POST.get('projectID', ''))
        TPA = TeachingProjectApply.objects.get(id=projectID)
        today = datetime.datetime.today()
        if type=='项目申请':
            if optionsRadios == 'pass':
                TPA.apply_status ='已通过'
                TPA.process = '项目申请已通过'
            elif optionsRadios == 'fail':
                TPA.apply_status = '未通过'
                TPA.process = '项目申请未通过'
            TPA.apply_verify_time = today
            TPA.save()
            return HttpResponse('{"status":"success","url":"/teaching/ProjectSelect/"}', content_type='application/json')
        elif type =='中期检查':
            if optionsRadios == 'pass':
                TPA.medium_status ='已通过'
                TPA.process = '中期检查已通过'
            elif optionsRadios == 'fail':
                TPA.medium_status = '未通过'
                TPA.process = '中期检查未通过'
            TPA.medium_verify_time = today
            TPA.save()
            return HttpResponse('{"status":"success","url":"/teaching/processCheckAdm/"}', content_type='application/json')
        elif type =='结题验收':
            if optionsRadios == 'pass':
                TPA.final_status ='已通过'
                TPA.process = '项目已结题'
            elif optionsRadios == 'fail':
                TPA.final_status = '未通过'
                TPA.process ='结题验收未通过'
            TPA.final_verify_time = today
            TPA.save()
            return HttpResponse('{"status":"success","url":"/teaching/processCheckAdm/"}', content_type='application/json')

class MyProjectListView(View):
    """
    从导航栏进入教师的项目列表页
    """
    def get(self, request):
        project = TeachingProjectApply.objects.filter(belongTea_id=request.user.id)
        return render(request, 'teaching_myProjectList.html', context={'projects': project})

class MyProjectDetailView(View):
    """
    教师从项目列表进入项目的详情页
    """
    def get(self, request):
        pro_id = request.GET['itemID']
        project = TeachingProjectApply.objects.get(id=pro_id)
        return render(request,'teaching_myProjectDetail.html',context={'project': project})

class UpdateProjectProcessView(View):
    """
    更新项目进度
    从项目详情页进入项目进度
    """
    def get(self, request):
        pro_id = request.GET['itemID']
        project = TeachingProjectApply.objects.get(id=pro_id)
        task = request.GET['type']
        processTask = {}
        if task == 'mid':
            processTask['title'] = '中期检查'
            processTask['content'] = '请提交中期检查材料'
        else:
            processTask['title'] = '结题验收'
            processTask['content'] = ' 请提交结题验收材料'

        return render(request, 'teaching_processCheck.html', context={'item': project, 'processTask': processTask})
    def post(self,request):
        pro_id =int(request.POST.get('projectID',''))
        files = request.FILES.get('fileUpload')
        Type = request.POST.get('submit_type','')
        file_dir = 'media/teaching/' + str(pro_id) + '项目的文件/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        file_path = file_dir + str(files)
        SF = SubmitFile()
        SF.project_file =file_path
        SF.file_name = re.split('/', str(file_path))[-1]
        SF.TPA_belong_id = pro_id
        if Type == '中期检查':
            SF.is_medium=True
        elif Type =='结题验收':
            SF.is_final =True
        f = open(file_path, 'wb+')
        for chunk in files.chunks():
            f.write(chunk)
        f.close()
        SF.save()
        return HttpResponseRedirect('/teaching/readProjectDetail/?itemID='+str(pro_id))

class ProcessCheckAdmView(View):
    """
    管理员进行进度审核的页面
    """
    def get(self,request):
        TPA = TeachingProjectApply.objects.filter(Q(apply_status='已通过')&(Q(medium_status__isnull=True)|Q(medium_status='未通过')))
        TPA_result_medium = [ ]
        for item in TPA:
            if item.submitfile_set.filter(is_medium=True).exists():
                TPA_result_medium.append(item)
        TPA_medium = TeachingProjectApply.objects.filter(Q(apply_status='已通过')&Q(medium_status='已通过')&(Q(final_status__isnull=True)|Q(final_status='未通过')))
        TPA_result_final = []
        for item in TPA_medium:
            if item.submitfile_set.filter(is_final=True).exists():
                TPA_result_final.append(item)
        return render(request,'teaching_processManageListAdm.html',context={'midAppliedProjects':TPA_result_medium,'finAppliedProjects':TPA_result_final})

class ReadProjectDetailAdmView(View):
    """
    管理员在这里进行中期审核项目的查看
    """
    def get(self,request):
        itemID = request.GET['itemID']
        type = request.GET['type']
        TPA =TeachingProjectApply.objects.get(id = itemID)
        project_file ={ }
        if type =='mid':
            SF = TPA.submitfile_set.get(is_medium=True)
        elif type =='fin':
            SF = TPA.submitfile_set.get(is_final=True)
        project_file['file_path']=SF.project_file
        project_file['file_name']=SF.file_name
        return render(request,'teaching_projectDetailAdm.html',context={'project':TPA,'project_file':project_file})

class verifyProcessApplicationView(View):
    """
    管理员这这里根据具体的参数进行中期或者结题项目的审核
    """
    def get(self,request):
        pro_id = request.GET['itemID']
        project = TeachingProjectApply.objects.get(id=pro_id)
        task = request.GET['type']
        verifyTask = {}
        files = {}
        if task == 'mid':
            verifyTask['type'] = '中期检查'
            files['file_path'] = project.submitfile_set.get(is_medium=True).project_file
            files['file_name'] = re.split('/', str(files['file_path']))[-1]
        elif task=='fin':
            verifyTask['type'] = '结题验收'
            files['file_path'] = project.submitfile_set.get(is_final=True).project_file
            files['file_name'] = re.split('/', str(files['file_path']))[-1]
        return render(request,'teaching_verifySingleProjectAdm.html',context={'verifyTask':verifyTask,'project':project,'files':files})

class ProjectDetailAdmView(View):
    """
    管理员在这里查看所有的项目
    """
    def get(self,request):
        TPA =TeachingProjectApply.objects.all()
        return render(request,'teaching_detailManageListAdm.html',context={'AppliedProjects':TPA})

class ReadApplicationView(View):
    """
    管理员通过项目详情进入上一级页面，通过点击查看，查看具体的项目信息
    """
    def get(self,request):
        itemID = request.GET['itemID']
        TPA = TeachingProjectApply.objects.get(id = itemID)
        download_item = [ ]
        if TPA.submitfile_set.filter(is_apply=True).exists():
            item = {}
            item['file_path'] = TPA.submitfile_set.filter(is_apply=True)[0].project_file
            item['file_name'] = '项目申请文件'        #re.split('/', str(item['file_path']))[-1]
            download_item.append(item)
        if TPA.submitfile_set.filter(is_medium=True).exists():
            item = {}
            item['file_path'] = TPA.submitfile_set.filter(is_medium=True)[0].project_file
            item['file_name'] = '中期检查文件'        #re.split('/', str(item['file_path']))[-1]
            download_item.append(item)
        if TPA.submitfile_set.filter(is_final=True).exists():
            item = {}
            item['file_path'] = TPA.submitfile_set.filter(is_final=True)[0].project_file
            item['file_name'] = '结题验收文件'        #re.split('/', str(item['file_path']))[-1]
            download_item.append(item)
        return render(request,'teaching_detailSingleProjectAdm.html',context={'project':TPA,'download_item':download_item})

class UpdateProjectFundRecordView(View):
    """
    教师在这里更新项目经费使用情况记录
    """
    def post(self,request):
        funds_record = request.POST.get('funds_record','')
        itemID = int(request.POST.get('projectID',''))
        TPA =TeachingProjectApply.objects.get(id = itemID)
        TPA.funds_record = funds_record
        TPA.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')

class UpdateProjectAchievementRecordView(View):
    """
    教师在这里更新项目成果
    """
    def post(self,request):
        achievements_record = request.POST.get('achievements_record','')
        itemID = int(request.POST.get('projectID',''))
        TPA =TeachingProjectApply.objects.get(id = itemID)
        TPA.achievements_record = achievements_record
        TPA.save()
        return  HttpResponse('{"status":"success"}', content_type='application/json')











