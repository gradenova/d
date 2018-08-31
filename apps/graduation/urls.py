"""teaching_assistant_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from apps.graduation import views
from apps.srtp.views import permission_forbidden


urlpatterns = [
    url(r'^student/$', permission_forbidden(http_exception=403)(views.GraduationStudentView.as_view()), name='graduation_student'),   #学生界面的路由映射

    url(r'^admin/GradtuationScheduleWatch/$', permission_forbidden(http_exception=401)(views.GraduationAdminView.as_view()), name='graduation_admin'),         #管理员界面的路由映射

    url(r'^teacher/$', permission_forbidden(http_exception=402)(views.GraduationTeacherView.as_view()), name='graduation_teacher'),    #教师界面的路由映射

    url(r'^teacher/verifyProjectOtherTeacher', permission_forbidden(http_exception=402)(views.GraduationTeacherOtherView.as_view()), name='graduation_teacher_other'), #评审教师界面的路由映射

    url(r'^teacher/verifyProjectTutor', permission_forbidden(http_exception=402)(views.GraduationTeacherTutorView.as_view()), name='graduation_teacher_tutor'),  #指导教师界面的路由映射

    url(r'^admin/readProjectDetailAdm', permission_forbidden(http_exception=401)(views.GraduationAdminWatchView.as_view()), name='graduation_admin_watch'),  #管理员查看特定学生信息的路由映射

    url(r'^admin/dateSetting/', permission_forbidden(http_exception=401)(views.GraduationAdminDateSetView.as_view()), name='graduation_admin_dateSet'),  #管理员管理毕设进度

    url(r'download/', views.DownloadFile, name='download'),  #下载文件的路由
]