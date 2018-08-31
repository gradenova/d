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
from django.contrib import admin
from django.conf.urls import url,include
from apps.user import views
from apps.srtp.views import permission_forbidden
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^srtp/', include('apps.srtp.urls')),

    url(r'^teaching/',include('apps.teaching.urls')),

    url(r'^course/', include('apps.coursArrange.urls')),  # 有关课程的路由映射

    url(r'^graduation/', include('apps.graduation.urls')),  # 有关毕业设计管理的路由映射

    url(r'^$',views.IndexView.as_view(),name='index'),

    url(r'^login/$',views.UserLoginView.as_view(),name='login'),

    url(r'^logout/$',views.UserLogoutView.as_view(), name='logout'),

    url(r'^course_arrange/$',views.courseArrangeView.as_view(),name='courseArrange'),

    url(r'^addTeacher/$',permission_forbidden(http_exception=401)(views.AddUser_TeacherView.as_view()),name='teacherInfo'),

    url(r'^addStudent/$',permission_forbidden(http_exception=401)(views.AddUser_StudentView.as_view()),name='studentInfo'),

    url(r'^addCourse/$',permission_forbidden(http_exception=401)(views.CourseListAdmView.as_view()),name = 'addCrouse'),

    url(r'^delete/deleteTea',permission_forbidden(http_exception=401)(views.DeleteUser_TeacherView.as_view()),name='deleteTeacher'),

    url(r'^delete/deleteStu',permission_forbidden(http_exception=401)(views.DeleteUser_StudentView.as_view()),name='deleteStudent'),

    url(r'^media',views.file_download,name='file_download'),

    url(r'^generalInformations/$',views.ReadInformationsView.as_view(),name='readInformation'),  #在首页查看信息

    url(r'^publishNotice/$',views.PublishNoticeView.as_view(),name = 'publishNotice'),  #管理员在首页直接发布通知

    url(r'readNotice/$',views. ReadNoticeView.as_view(),name = 'ReadNotice'),     #查看具体的通知










]
