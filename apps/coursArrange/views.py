from django.shortcuts import render
from django.views import View
from .models import Course
from .models import CourseArrange
from django.http import HttpResponseRedirect
from .models import CourseOtherDemand
import random
from .models import ClassRoom
from apps.user.models import Teacher, UserProfile
from django.http import HttpResponse
from django.db.models import F
import json

# Create your views here.

class CourseArrangeListTeacherView(View):
    '''
    查看所有教师的课程信息
    '''
    def get(self, request):
        courseList = CourseArrange.objects.all().annotate(
            courseNumber=F('course__number'),
            courseName=F('course__name'),
            teacherNumber=F('teacher__contract__username'),
            teacherName=F('teacher__realname')
        ).values(
            'courseNumber',
            'courseName',
            'teacherNumber',
            'teacherName',
            'classes'
        ).distinct()
        return render(request, 'courseList_Admin.html',{'courseList': courseList})

class CourseHandArrangeView(View):
    '''
    管理员手工排课
    '''
    def get(self, request):
        courseID = request.GET.get('courseID')
        teacherID  = request.GET.get('teacherID')
        classes = request.GET.get('classes')
        course = CourseArrange.objects.filter(course__number=courseID,teacher__contract__username=teacherID,classes=classes).annotate(
            courseName=F('course__name'),
            courseID=F('course__number'),
            teacherName=F('teacher__realname'),
            teacherID=F('teacher__contract__username'),
            totalHours=F('course__thyHours')+F('course__labHours')
        ).values('courseName', 'courseID','teacherName','teacherID','classes','totalHours').distinct()
        course = course[0]
        demand = CourseOtherDemand.objects.filter(course__number=courseID,teacher__contract__username=teacherID,classes=classes).values('demand')
        course['otherDemand'] = demand[0]['demand']
        # 创建一个16的空矩阵
        # 获取理论课的排课安排
        classTimeList = CourseArrange.objects.filter(course__number=courseID, teacher__contract__username=teacherID, classes=classes, laborthy=False).annotate(
            building=F('place__building'),
            roomnumber=F('place__number')
            ).values('week', 'day', 'number', 'building', 'roomnumber')
        for temp in classTimeList:
            print(temp)
        # 获取实验课的排课安排
        LabClassTimeList = CourseArrange.objects.filter(course__number=courseID, teacher__contract__username=teacherID, classes=classes, laborthy=True).annotate(
            building=F('place__building'),
            roomnumber=F('place__number')
            ).values('week','day','number','building','roomnumber')
        print(LabClassTimeList)
        return render(request, 'courseArrangeManual_Admin.html', {'course': course, 'classTimeList': classTimeList, 'LabClassTimeList': LabClassTimeList})
    '''
    管理员提交手工排课结果
    '''
    def post(self, request):
        # request.POST.get('theoryCourseArrange[{}][{}][weekday]'.format(str(1),str(4)))
        teacherID = request.POST.get('teacherID')
        courseID = request.POST.get('courseID')
        classes = request.POST.get('courseClass')
        # 检查输入信息是否正确： 教室信息是否存在，学时加和是否对应，若不符合，均不能删除数据库原有的排课信息
        thysum = 0
        labsum = 0
        for i in range(0, 16):
            for j in range(0, 8):
                buildingThy = request.POST.get('theoryCourseArrange[{}][{}][building]'.format(str(i), str(j)))
                roomnumberThy = request.POST.get('theoryCourseArrange[{}][{}][classroom]'.format(str(i), str(j)))
                if buildingThy == '1':
                    buildingThy = '逸夫楼'
                elif buildingThy == '2':
                    buildingThy = '教学楼'
                else:
                    buildingThy = '机电楼'
                if roomnumberThy is None:
                    pass
                else:
                    thysum += 1
                    if len(ClassRoom.objects.filter(building=buildingThy, number=roomnumberThy)) == 0:
                        data = {'status': 'fail', 'msg': '理论课教室不存在，请检查后重新输入'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                buildingLab = request.POST.get('labCourseArrange[{}][{}][building]'.format(str(i), str(j)))
                roomnumberLab = request.POST.get('labCourseArrange[{}][{}][classroom]'.format(str(i), str(j)))
                if buildingLab == '1':
                    buildingLab = '逸夫楼'
                elif buildingLab == '2':
                    buildingLab = '教学楼'
                else:
                    buildingLab = '机电楼'
                if roomnumberLab is None:
                    pass
                else:
                    labsum += 1
                    if len(ClassRoom.objects.filter(building=buildingLab,number=roomnumberLab)) == 0:
                        data = {'status': 'fail', 'msg': '实验课教室不存在，请检查后重新输入'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
        thysum = thysum*2
        labsum = labsum*2
        # 检查学时加和是否对应
        SearchResult = Course.objects.filter(number=courseID).values('thyHours','labHours')
        thyHours = SearchResult[0]['thyHours']
        labHours = SearchResult[0]['labHours']
        if thyHours != thysum:
            data = {'status': 'fail', 'msg': '理论课学时总和不对应，请检查后重新输入'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        elif labHours != labsum:
            data = {'status': 'fail', 'msg': '实验课学时总和不对应，请检查后重新输入'}
            return HttpResponse(json.dumps(data), content_type='application/json')
        CourseArrange.objects.filter(course__number=courseID, teacher__contract__username=teacherID,classes=classes).delete()
        # 更新理论课的排课信息
        for i in range(0, 16):          # 16周
            for j in range(0, 8):       # 1周不超过8次课
                week = i + 1
                day = request.POST.get('theoryCourseArrange[{}][{}][weekday]'.format(str(i),str(j)))
                number = request.POST.get('theoryCourseArrange[{}][{}][time]'.format(str(i), str(j)))
                building = request.POST.get('theoryCourseArrange[{}][{}][building]'.format(str(i), str(j)))
                roomnumber = request.POST.get('theoryCourseArrange[{}][{}][classroom]'.format(str(i), str(j)))
                if building == '1':
                    building = '逸夫楼'
                elif building == '2':
                    building = '教学楼'
                else:
                    building = '机电楼'
                if day is None:
                    pass
                else:
                    coursearrange = CourseArrange()
                    coursearrange.classes = classes
                    coursearrange.teacher = Teacher.objects.get(contract__username=teacherID)
                    coursearrange.course = Course.objects.get(number=courseID)
                    coursearrange.week = week
                    coursearrange.day = day
                    coursearrange.number = number
                    coursearrange.place = ClassRoom.objects.get(building=building, number=roomnumber)
                    coursearrange.save()
        # 更新实验课的排课信息
        for i in range(0, 16):          # 16周
            for j in range(0, 8):       # 1周不超过8次课
                week = i + 1
                day = request.POST.get('labCourseArrange[{}][{}][weekday]'.format(str(i),str(j)))
                number = request.POST.get('labCourseArrange[{}][{}][time]'.format(str(i), str(j)))
                building = request.POST.get('labCourseArrange[{}][{}][building]'.format(str(i), str(j)))
                roomnumber = request.POST.get('labCourseArrange[{}][{}][classroom]'.format(str(i), str(j)))
                if building == '1':
                    building = '逸夫楼'
                elif building == '2':
                    building = '教学楼'
                else:
                    building = '机电楼'
                if day is None:
                    pass
                else:
                    coursearrange = CourseArrange()
                    coursearrange.classes = classes
                    coursearrange.teacher = Teacher.objects.get(contract__username=teacherID)
                    coursearrange.course = Course.objects.get(number=courseID)
                    coursearrange.week = week
                    coursearrange.day = day
                    coursearrange.number = number
                    coursearrange.laborthy = True
                    coursearrange.place = ClassRoom.objects.get(building=building, number=roomnumber)
                    coursearrange.save()
        data = {'status': 'success'}
        return HttpResponse(json.dumps(data), content_type='application/json')

class ReleaseAllCourseArrangeView(View):
    '''
    管理员发布排课结果
    '''
    def post(self, request):
        CourseArrange.objects.all().update(watch=True)
        return HttpResponse( {'status':'success'},content_type = 'application/json' )

class CourseAdminView(View):
    '''
    查看课程信息及排课信息
    '''
    def get(self, request):
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
        return render(request, 'infoManage_entryCourse.html', {'courseInfoList': courseInfoList, 'courseArrangeList': courseArrangeList})
    def post(self, request):
        kind = request.POST.get('theoryHours')
        if kind is None:
            # 教师信息
            teacherId = request.POST.get('teacherID', '')
            teacherName = request.POST.get('teacherName', '')
            # 班级信息
            className = request.POST.get('class', '')
            # 课程信息
            courseId = request.POST.get('ID', '')
            courseName = request.POST.get('name', '')
            # 验证教师信息(编号正确，身份正确，姓名正确)是否正确
            ifExitTeacher = len(Teacher.objects.filter(realname=teacherName, contract__username=teacherId))
            # 验证课程信息(编号正确，名字正确)是否对应，
            ifExitCourse = len(Course.objects.filter(number=courseId, name=courseName))
            # 验证该班级是否已经上过此课
            ifExitClass = len(CourseArrange.objects.filter(classes=className, course__number=courseId))
            if ifExitClass > 0:
                ifExitClass = 0
            elif ifExitClass == 0:
                ifExitClass = 1
            if ifExitTeacher & ifExitCourse & ifExitClass:
                coursearrange = CourseArrange()
                coursearrange.classes = className
                coursearrange.course = Course.objects.get(number=courseId)
                coursearrange.teacher = Teacher.objects.get(contract__username=teacherId)
                coursearrange.save()
                data = {'status': 'success', 'msg': '信息保存成功'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                if ifExitTeacher == 0:
                    data = {'status': 'fail', 'msg': '教师信息有误，请检查后再输入'}
                elif ifExitCourse == 0:
                        ata = {'status': 'fail', 'msg': '课程信息有误，请检查后再输入'}
                elif ifExitClass == 0:
                    data = {'status': 'fail', 'msg': '该班级已安排上此课，请检查后再输入'}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            course = Course()
            course.number = request.POST.get('ID')
            course.name = request.POST.get('name')
            course.thyHours = request.POST.get('theoryHours')
            course.labHours = request.POST.get('labHours')
            if len(Course.objects.filter(number=course.number)) == 1:
                data = {'status': 'fail', 'msg': '编号必须唯一'}
            elif len(Course.objects.filter(name=course.name, thyHours=course.thyHours, labHours=course.labHours)) == 1:
                data = {'status': 'fail', 'msg': '除了编号，其它信息均重复'}
            else:
                course.save()
                data = {'status': 'success', 'msg': '课程信息保存成功'}
            return HttpResponse(json.dumps(data), content_type='application/json')

class delectCourseInfoView(View):
    '''
    删除课程信息
    '''
    def get(self, request):
        courseID = request.GET.get('courseID')
        Course.objects.filter(number=courseID).delete()
        return HttpResponseRedirect('/course/courseChange/')

class deleteCourseArrangeView(View):
    """
    删除排课信息
    """
    def get(self, request):
        courseID = request.GET.get('courseID')
        teacherID  = request.GET.get('teacherID')
        className = request.GET.get('className')
        CourseArrange.objects.filter(course__number=courseID, teacher__contract__username=teacherID, classes=className).delete()
        return HttpResponseRedirect('/course/courseChange/')

class courseList_TeacherView(View):
    """
    显示该名教师的课程信息，两种情况，一种是已排好课的，一种是未排课的
    """
    def get(self, request):
        if CourseArrange.objects.filter(watch=1).count() != 0:
            #创建一个6*7的空矩阵：6表示1天6节课，7表示1周7天
            courseSchedule = [[' ' for i in range(7)] for j in range(6)]
            teacherID = request.user.username
            records = CourseArrange.objects.filter(teacher__contract__username=teacherID).values('place__building', 'place__number', 'day', 'number', 'classes', 'course__number').distinct()
            for record in records:
                results = CourseArrange.objects.filter(teacher__contract__username=teacherID, course__number=record['course__number'], place__building=record['place__building'], place__number=record['place__number'], day=record['day'], number=record['number'], classes=record['classes']).annotate(
                    name=F('course__name'), building=F('place__building'), roomnumber=F('place__number')
                ).values(
                    'building',
                    'roomnumber',
                    'week',
                    'day',
                    'number',
                    'name',
                    'laborthy'
                )
                #字符串形式：课程名(如果为实验课，标明为实验)，第几周至第几周(第几周)，地点，房间号,courseSchedule的行下标表示第几节，列下标表示星期几
                if results[0]['laborthy'] == True:
                    if len(results)==1:
                        courseSchedule[results[0]['number']-1][results[0]['day']-1] += results[0]['name'] + "(实验课),第" + str(results[0]['week']) + "周," + results[0]['building'] + "," + str(results[0]['roomnumber'])
                    else:
                        courseSchedule[results[0]['number']-1][results[0]['day']-1] += results[0]['name'] + '(实验课),第' + str(results[0]['week']) + "周至第" + str(results[len(results)-1]['week']) + "周" + results[0]['building'] + "," + str(results[0]['roomnumber'])
                else:
                    if len(results)==1:
                        courseSchedule[results[0]['number']-1][results[0]['day']-1] += results[0]['name'] + ",第" + str(results[0]['week']) + "周," + results[0]['building'] + "," + str(results[0]['roomnumber'])
                    else:
                        courseSchedule[results[0]['number']-1][results[0]['day']-1] += results[0]['name'] + ',第' + str(results[0]['week']) + "周至第" + str(results[len(results)-1]['week']) + "周" + results[0]['building'] + "," + str(results[0]['roomnumber'])
            return render(request, 'courseResult_Teacher.html', {'courseSchedule': courseSchedule})                       #返回排课结果
        else:
            teacherID = request.user.username
            courseList = CourseArrange.objects.filter(teacher__contract__username=teacherID).annotate(
                totalHours=F('course__thyHours') + F('course__labHours')).annotate(
                    sid=F('course__number'),
                    name=F('course__name'),
                    thyHours=F('course__thyHours'),
                    labHours=F('course__labHours')
                ).values(
                'sid',
                'name',
                'classes',
                'totalHours',
                'thyHours',
                'labHours'
            ).distinct()
            for temp in courseList:
                if temp['labHours'] > 0:
                    temp['labFlag'] = '是'
                else:
                    temp['labFlag'] = '否'
            return render(request, 'courseList_Teacher.html', {'courseList': courseList})  #返回未排课结果

class addCourseDemandView(View):
    """
    教师排课需求界面
    """
    def get(self, request):
        courseID = request.GET.get('courseID')
        print(courseID)
        courseClass = request.GET.get('courseClass')
        temp = Course.objects.get(number=courseID)
        course = {'sid': courseID, 'name': temp.name, 'thyHours': temp.thyHours, 'labHours': temp.labHours, 'totalHours': temp.thyHours + temp.labHours, 'courseClass': courseClass}
        return render(request, 'courseArrange_Teacher.html', {'course': course})
    '''
    教师添加排课需求
    '''
    def post(self, request):
        courseid = request.POST.get('course_id')
        courseClass = request.POST.get('course_class')
        teacherid = request.user.username
        course = Course.objects.get(number=courseid)
        teacher = Teacher.objects.get(contract__username=teacherid)
        thyWeekHours = request.POST.getlist('thyWeekHours')
        print(thyWeekHours)
        # 删除数据库中原来的记录
        CourseArrange.objects.filter(course__number=courseid, teacher__contract__username=teacherid, classes=courseClass).delete()
        CourseOtherDemand.objects.filter(course__number=courseid, teacher__contract__username=teacherid, classes=courseClass).delete()
        # 保存教师的其它特殊需求
        remarks = request.POST.get('remarks')
        courseotherdemand = CourseOtherDemand()
        courseotherdemand.course = course;
        courseotherdemand.teacher = teacher
        courseotherdemand.classes = courseClass
        courseotherdemand.demand = remarks
        courseotherdemand.save()
        unprefer_time = request.POST.getlist('unprefer_time')
        unprefer_building = request.POST.getlist('unprefer_building')
        # 生成排课表的算法(理论课)
        # 存储不想上课的时间点
        DislikeTime = [[None for i in range(5)] for j in range(5)]
        for temp in unprefer_time:
            day = int(temp[2])
            number = int(temp[0])
            DislikeTime[number-1][day-1] = 1
        # 删除原有的排课表
        CourseArrange.objects.filter(course__number=courseid, classes=courseClass, teacher__contract__username=teacherid).delete()
        # 确定周几的可选集
        if '6' in thyWeekHours:    #1周有3次课
            DayList = [[1, 3, 5]]
        elif '4' in thyWeekHours:  #1周有2次课
            DayList = [[1, 3], [1, 4], [1, 5], [2, 4], [2, 5], [3, 5]]
        elif '2' in thyWeekHours:  #1周有1次课
            DayList = [[1], [2], [3], [4], [5]]
        # 确定节数的可选集
        NumberList = [1, 2, 3, 4, 5]
        # 确定地点的可选集
        DislikeBuilding = []
        LocationList = []
        SearchResult = ClassRoom.objects.filter(useage='理论教学').values('id')
        for i in SearchResult:
            LocationList.append(i['id'])
        for temp in unprefer_building:
            if temp == '1':
                SearchResult = ClassRoom.objects.filter(building='逸夫楼').values('id')
                for temp in SearchResult:
                    DislikeBuilding.append(temp['id'])
                LocationList = list(set(LocationList).difference(set(DislikeBuilding)))
            elif temp == '2':
                SearchResult = ClassRoom.objects.filter(building='教学楼').values('id')
                for temp in SearchResult:
                    DislikeBuilding.append(temp['id'])
                LocationList = list(set(LocationList).difference(set(DislikeBuilding)))
            elif temp == '3':
                SearchResult = ClassRoom.objects.filter(building='机电楼').values('id')
                for temp in SearchResult:
                    DislikeBuilding.append(temp['id'])
                LocationList = list(set(LocationList).difference(set(DislikeBuilding)))
        # 随机选取星期几，第几节，在哪个地点，检查是否在周数内满足条件
        ChoseDay = None
        ChoseNumber = None
        ChoseLocation = None
        ChoseWeek = 0
        Mark = False
        while Mark == False :
            Mark = True
            ChoseDay = random.sample(DayList, 1)
            ChoseDay = ChoseDay[0]
            ChoseNumber = random.sample(NumberList, 1)
            ChoseNumber = ChoseNumber[0]
            ChoseLocation = random.sample(LocationList, 1)
            ChoseLocation = ChoseLocation[0]
            for weektemp in thyWeekHours:
                ChoseWeek += 1
                if weektemp != '0':
                    ClassCount = int(int(weektemp)/2)  #一周要上课的次数
                    for x in range(0, ClassCount):
                        ChoseDays = ChoseDay[x]
                        if len(CourseArrange.objects.filter(classes=courseClass, week=ChoseWeek, day=ChoseDays)) == 3:  #班级这周这天上课次数已经为3次
                            Mark = False
                            break;
                        elif len(CourseArrange.objects.filter(teacher__contract__username=teacherid, week=ChoseWeek, day=ChoseDays)) == 3: #教师这周这天上课次数已经为3次
                            Mark = False
                            break;
                        elif len(CourseArrange.objects.filter(week=ChoseWeek, day=ChoseDays, number=ChoseNumber, place__id=ChoseLocation)) != 0: #这周这星期这节这个地点有课
                            Mark = False
                            break;
                        elif DislikeTime[ChoseNumber-1][ChoseDays-1] == 1:                                                                         #这星期这节教师不想上课
                            Mark = False
                            break;
                else:
                    pass
        # 所选星期几，第几节，哪个地点，在规定的上课周内均符合条件,生成排课记录
        ChoseWeek = 0
        for weektemp in thyWeekHours:
            ChoseWeek += 1
            if weektemp != '0':
                ClassCount = int(int(weektemp) / 2)  # 一周要上课的次数
                for x in range(0, ClassCount):
                    ChoseDays = ChoseDay[x]
                    coursearrange = CourseArrange()
                    coursearrange.teacher = teacher
                    coursearrange.course = course
                    coursearrange.classes = courseClass
                    coursearrange.week = ChoseWeek
                    coursearrange.day = ChoseDays
                    coursearrange.number = ChoseNumber
                    coursearrange.place = ClassRoom.objects.get(id=ChoseLocation)
                    coursearrange.save()
        labFlag = request.POST.get('labFlag')
        # 实验课排课算法
        if labFlag == '1':
            labWeekHours = request.POST.getlist('labWeekHours')
            LocationList = []
            # 确定可选地点
            SearchResult = ClassRoom.objects.filter(useage='实验教学').values('id')
            for i in SearchResult:
                LocationList.append(i['id'])
            # 可选时间集为DayList
            # 可选节数集为NumberList
            # 随机选取星期几，第几节，在哪个地点，检查是否在周数内满足条件
            ChoseDay = None
            ChoseNumber = None
            ChoseLocation = None
            ChoseWeek = 0
            Mark = False
            while Mark == False:
                Mark = True
                ChoseDay = random.sample(DayList, 1)
                ChoseDay = ChoseDay[0]
                ChoseNumber = random.sample(NumberList, 1)
                ChoseNumber = ChoseNumber[0]
                ChoseLocation = random.sample(LocationList, 1)
                ChoseLocation = ChoseLocation[0]
                for weektemp in labWeekHours:
                    ChoseWeek += 1
                    if weektemp != '0':
                        ClassCount = int(int(weektemp) / 2)  # 一周要上课的次数
                        for x in range(0, ClassCount):
                            ChoseDays = ChoseDay[x]
                            if len(CourseArrange.objects.filter(classes=courseClass, week=ChoseWeek,day=ChoseDays)) == 3:  # 班级这周这天上课次数已经为3次
                                Mark = False
                                break;
                            elif len(CourseArrange.objects.filter(teacher__contract__username=teacherid,week=ChoseWeek,day=ChoseDays)) == 3:  # 教师这周这天上课次数已经为3次
                                Mark = False
                                break;
                            elif len(CourseArrange.objects.filter(week=ChoseWeek, day=ChoseDays, number=ChoseNumber,place__id=ChoseLocation)) != 0:  # 这周这星期这节这个地点有课
                                Mark = False
                                break;
                            elif DislikeTime[ChoseNumber - 1][ChoseDays - 1] == 1:  # 这星期这节教师不想上课
                                Mark = False
                                break;
                    else:
                        pass
            # 所选星期几，第几节，哪个地点，在规定的上课周内均符合条件,生成排课记录
            ChoseWeek = 0
            for weektemp in labWeekHours:
                ChoseWeek += 1
                if weektemp != '0':
                    ClassCount = int(int(weektemp) / 2)  # 一周要上课的次数
                    for x in range(0, ClassCount):
                        ChoseDays = ChoseDay[x]
                        coursearrange = CourseArrange()
                        coursearrange.teacher = teacher
                        coursearrange.course = course
                        coursearrange.classes = courseClass
                        coursearrange.week = ChoseWeek
                        coursearrange.day = ChoseDays
                        coursearrange.number = ChoseNumber
                        coursearrange.laborthy = True
                        coursearrange.place = ClassRoom.objects.get(id=ChoseLocation)
                        coursearrange.save()
        data = {'status': 'success', 'msg': '排课成功，请等待管理员发布课表'}
        return HttpResponse(json.dumps(data), content_type='application/json')

