from django.conf.urls import url

from apps.srtp import views
from apps.srtp.views import permission_forbidden
# from .views import file_download
urlpatterns = [

    url(r'^releaseProjectCollect/$',permission_forbidden(http_exception=401)(views.ProjectCollectIssueView.as_view()),name='releaseProjectCollect'),
    #管理员进入到发布srtp项目征集通告页面
    url(r'^submitCollectSrtp/$',permission_forbidden(http_exception=402)(views.SrtpCollectInfoView.as_view()),name='SrtpCollectInfo'),
    #教师查看项目征集的通告，并申报项目
    url(r'^checkCollectedItem/$',permission_forbidden(http_exception=401)(views.CollectProjectDetailView.as_view()),name='CollectProjectDetail'),
    #管理员查看教师申报项目的具体详情
    url(r'^deleteCollectedProject/$',permission_forbidden(http_exception=401)(views.DeleteTeaProjectView.as_view()),name = 'deleteCollectedProject'),
    #管理员删除教师申报的项目
    url(r'^submitPublishProject/$',permission_forbidden(http_exception=401)(views.SrtpProjectPubilshView.as_view()),name = 'PublishProject'),
    #管理员进行srtp项目公布，并在这里给学生发布具体的申报信息。
    url(r'^srtp_view/$',permission_forbidden(http_exception=403)(views.SrtpProjectSignupView.as_view()),name = 'SrtpProjectSignup'),
    #学生查看报名通知并在这里进行报名
    url(r'^viewSingleProject/$',permission_forbidden(http_exception=403)(views.SrtpProjectDeatailView.as_view()),name = 'SrtpProjectDeatail'),
    #学生可以在这里查看详细的srtp的项目
    url(r'^submitSrtpSignUp_Info/$',permission_forbidden(http_exception=403)(views.SrtpSignupInfoView.as_view()),name = 'SrtpSignUp_Info'),
    #学生在这里保存输入的报名信息,包括报名成员的信息
    url(r'^submitSrtpSignUpFile_Info/$',permission_forbidden(http_exception=403)(views.SrtpSignupFileView.as_view()),name = 'SrtpSignUp_File'),
    #学生主要在这里提交自己组的报名材料
    url(r'^verifyProjectTea/$',permission_forbidden(http_exception=402)(views.VerifyProjectTeacherView.as_view()),name = 'verifyProjectTea'),
    #教师查看申请项目表
    url(r'^verifyItem/$',views.VerifyItemView.as_view(),name ='verifyItem'),
    #教师或者管理员审核单个项目，不做访问控制
    url(r'^verifyProjectAdm/$',permission_forbidden(http_exception=401)(views.VerifyProjectAdminView.as_view()),name = 'verifyProjectAdm'),
    #管理员查看申请项目表
    url(r'^ProcessManageAdm/$',permission_forbidden(http_exception=401)(views.ProcessManageAdminView.as_view()),name = 'ProcessManageAdm'),
    #管理员进程管理,包括发布新任务
    url(r'^changeProcessTask/$',permission_forbidden(http_exception=401)(views.ChangeProcessTaskView.as_view()),name ='changeProcessTask'),
    #管理员修改已经发布的任务
    url(r'^submitNewProcessTask/$',permission_forbidden(http_exception=401)(views.SubmitNewProcessTaskView.as_view()),name = 'submitNewProcessTask'),
    #管理员发布新任务
    url(r'^processreportTea/$',permission_forbidden(http_exception=402)(views.ReportProcessTaskView.as_view()),name = 'processreportTea'),
    #教师在这里看到管理员下发的中期任务通知
    url(r'^processCheck/$',permission_forbidden(http_exception=402)(views.SubmitProcessTaskTeaView.as_view()),name = 'processCheck'),
    #教师在这里对每一个中期任务做提交
    url(r'^submitProcessCheck/$',permission_forbidden(http_exception=402)(views.SubmitProccessCheckView.as_view()),name = 'submitProcessCheck'),
    #教师在这里对每一个项目提交中期材料
    url(r'^statisticProjectAdm/$',permission_forbidden(http_exception=401)(views.StatisticProjectAdmView.as_view()),name = 'statisticProjectAdm'),
    #管理员在这里进行数据统计
    url(r'^statisticProjectDetail',permission_forbidden(http_exception=401)(views.StatistcProjectDetailView.as_view()),name = 'statisticProjectDetail'),
    #管理员在这里查看具体的某个项目的数据统计


# 说明，permission_forbidden为访问控制装饰器，
# 当用户发出确定请求时，都会调用装饰器确定用户身份，
# 当身份正确时，才能够进入到特定的views里面，
# 实现访问控制，参数http_exception  401为管理员，402为教师，403为学生










]