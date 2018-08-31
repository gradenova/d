from django.conf.urls import url
from apps.teaching import views
from apps.srtp.views import permission_forbidden

urlpatterns = [
    url(r'^informationPublish/$',permission_forbidden(http_exception=401)(views.InformationPublishView.as_view()),name = 'informationPublish'),  #管理员在这里发布征集项目的通告

    url(r'^readInfo/$',views.InformationPublishDetailView.as_view(),name = 'readInfo'), #管理员或教师在这里查看历史发布信息的详情

    url(r'^deleteInfo/$',permission_forbidden(http_exception=401)(views.DeleteInfoView.as_view()),name = 'deleteInfo'),          #管理员在这里删除发布的信息

    url(r'^ProjectSelect/$',permission_forbidden(http_exception=401)(views.ProjectSelectView.as_view()),name = 'ProjectSelect'),   #管理员在这里进行项目评选

    url(r'^informationList/$', permission_forbidden(http_exception=402)(views.TeacherInformationListView.as_view()), name='informationList'),  #教师在这里查看管理员发布的具体通知

    url(r'^applyProject/$', permission_forbidden(http_exception=402)(views.ProjectApplyView.as_view()), name='applyProject'),         #教师在这里申请项目

    url(r'^myProjectList/$', permission_forbidden(http_exception=402)(views.MyProjectListView.as_view()), name='myProjectList'),     #教师在这里查看自己项目的列表

    url(r'^readProjectDetail/$', permission_forbidden(http_exception=402)(views.MyProjectDetailView.as_view()), name='readProjectDetail'),   #教师在这里查看项目的具体详情

    url(r'^updateProjectProcess/$', permission_forbidden(http_exception=402)(views.UpdateProjectProcessView.as_view()), name='updateProjectProcess'),  #教师在这里更新项目进度

    url(r'^verifyItemAdm/$',permission_forbidden(http_exception=401)(views.VerifyItemAdmView.as_view()),name = 'verifyItemAdm'),            #进入管理员审核具体的项目

    url(r'^teachingJudgeAdm/$',permission_forbidden(http_exception=401)(views.TeachingJudgeAdmView.as_view()),name = 'teachingJudgeAdm'),  #管理员在项目申报阶段审核项目

    url(r'^processCheckAdm/$',permission_forbidden(http_exception=401)(views.ProcessCheckAdmView.as_view()),name = 'processCheckAdm'), #管理员项目进度审核页面

    url(r'^readProjectDetailAdm/$',permission_forbidden(http_exception=401)(views.ReadProjectDetailAdmView.as_view()),name ='ReadProjectDetailAdm'),  #管理员在这里查看中期项目的具体详情

    url(r'^verifyProcessApplication/$',permission_forbidden(http_exception=401)(views.verifyProcessApplicationView.as_view()),name = 'verifyProcessApplication'),#管理员在这里进行项目的审核

    url(r'^projectDetailAdm/$',permission_forbidden(http_exception=401)(views.ProjectDetailAdmView.as_view()),name = 'projectDetailAdm'),#管理员在这里进行所有项目的查看

    url(r'^readApplication/$',permission_forbidden(http_exception=401)(views.ReadApplicationView.as_view()),name ='readApplication'),   #管理员在这里查看具体的项目详情

    url(r'^updateProjectFundRecord/$',permission_forbidden(http_exception=402)(views.UpdateProjectFundRecordView.as_view()),name = 'updateProjectFundRecord'),  #教师在这里更新项目经费使用记录

    url(r'^updateProjectAchievementRecord/$',permission_forbidden(http_exception=402)(views.UpdateProjectAchievementRecordView.as_view()),name= 'updateProjectAchievementRecord'),  #教师在这里更新项目成果


]

# 说明，permission_forbidden为访问控制装饰器，
# 当用户发出确定请求时，都会调用装饰器确定用户身份，
# 当身份正确时，才能够进入到特定的views里面，
# 实现访问控制，参数http_exception  401为管理员，402为教师，403为学生