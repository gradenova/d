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
from apps.coursArrange import views
from apps.srtp.views import permission_forbidden

urlpatterns = [
    url(r'^$', views.courseList_TeacherView.as_view(), name='course'),   #查看该名教师的课程信息

    url(r'^courseChange/$', permission_forbidden(http_exception=401)(views.CourseAdminView.as_view()), name='courseAdminView'),  #管理员排课界面

    url(r'^courseChange/courseInfoDelete', permission_forbidden(http_exception=401)(views.delectCourseInfoView.as_view()), name='courseInfoDelete'),  #管理员删除课程信息

    url(r'^courseChange/courseArrangeDelete', permission_forbidden(http_exception=401)(views.deleteCourseArrangeView.as_view()), name='courseDelete_Teacher'), #管理员删除教师的课程信息

    url(r'^courseDemand', permission_forbidden(http_exception=402)(views.addCourseDemandView.as_view()), name='coureDemand_Teacher'),  # 为指定课程添加排课需求

    url(r'courseHandArrange', permission_forbidden(http_exception=401)(views.CourseHandArrangeView.as_view()), name='HanCourseArrange'),  #管理员手工排课

    url(r'courseListTeacher/', permission_forbidden(http_exception=401)(views.CourseArrangeListTeacherView.as_view()), name='CourseListTeacher'),  #管理员查看所有教师的课程信息

    url(r'^releaseAllCourseArrange/', permission_forbidden(http_exception=401)(views.ReleaseAllCourseArrangeView.as_view()), name='ReleaseAllCourseArrange'),  #管理员发布排课最终结果
]