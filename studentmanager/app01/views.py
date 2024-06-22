from django.shortcuts import render, HttpResponse, redirect
from app01.models import Student, StuCours, Course, CourseAcademy, Academy
# Create your views here.
# 登陆界面
def login(request):
    global username
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request._post.get('user')
        password = request._post.get('pwd')
        students = Student.objects.all()
        for obj in students:
            if username == str(obj.id):
                pwd = Student.objects.filter(id = username).first()
                pwd = pwd.password
                if password == pwd:
                    return redirect("/login/menu/")
        return render(request, 'login.html', {"error" : "用户名或密码错误"})
    
# 显示菜单
def menu(request):
    global datalist, academy, course, flat, academycourse
    flat = [False,False,False,False,False,False,False,False,False]
    course = StuCours.objects.filter(studentid = username)
    datalist = Student.objects.filter(id = username)
    academy = Academy.objects.filter(id = datalist[0].academyid)
    academyid = datalist[0].academyid
    academycourse = CourseAcademy.objects.filter(academyid__id = academyid)
    return render(request, "menu.html", {'datalist' : datalist[0], 'academy' : academy[0]})

# 选课界面
def select_course(request):
    flat = False
    if flat:
        return HttpResponse("您已选过，请退出")
    flat = True
    student = datalist[0].name
    if request.method == 'POST':
        option1 = request.POST.get('courseSelect1')
        option2 = request.POST.get('courseSelect2')
        option3 = request.POST.get('courseSelect3')
        print(option1)
        option1 = int(option1)
        option2 = int(option2)
        option3 = int(option3)
        if option1 == option2 or option1 == option3 or option2 == option3:
            return render(request, 'select_course.html', {"student" : student, "academy" : academy[0], 
                                                  'academycourse1' : academycourse[0].courseid, 
                                                  'academycourse2' : academycourse[1].courseid, 
                                                  'academycourse3' : academycourse[2].courseid,
                                                  'error' : '请不要重复选择相同的课程'})
        
        StuCours.objects.filter(id = course[0].id).update(courseid = option1)
        StuCours.objects.filter(id = course[1].id).update(courseid = option2)
        StuCours.objects.filter(id = course[2].id).update(courseid = option3)  
        return redirect('http://127.0.0.1:8000/login/menu/result/')
    return render(request, 'select_course.html', {"student" : student, "academy" : academy[0], 
                                                  'academycourse1' : academycourse[0].courseid, 
                                                  'academycourse2' : academycourse[1].courseid, 
                                                  'academycourse3' : academycourse[2].courseid})
    
# 查询选课结果
def result(request):
    student = datalist[0].name
    course1 = Course.objects.filter(id = course[0].courseid).first()
    course2 = Course.objects.filter(id = course[1].courseid).first()
    course3 = Course.objects.filter(id = course[2].courseid).first()
    return render(request, 'result.html', {"student" : student, "course1" : course1, 
                                           "course2" : course2, "course3" : course3})
# 修改结果
def modifyresult(request):
    student = datalist[0].name
    for i in range(9):
        if course[i//3].courseid == academycourse[i%3].courseid.id:
            flat[i] = True
    
    if request.method == 'POST':
        option1 = request.POST.get('courseSelect1')
        option2 = request.POST.get('courseSelect2')
        option3 = request.POST.get('courseSelect3')
        print(option1)
        option1 = int(option1)
        option2 = int(option2)
        option3 = int(option3)
        if option1 == option2 or option1 == option3 or option2 == option3:
            return render(request, 'modifyresult.html', {"student" : student, "academy" : academy[0], 
                                                         'academycourse1' : academycourse[0].courseid, 
                                                         'academycourse2' : academycourse[1].courseid, 
                                                         'academycourse3' : academycourse[2].courseid,
                                                         'error' : '请不要重复选择相同的课程',
                                                         'a1' : flat[0], 'a2' : flat[1], 'a3' : flat[2],
                                                         'a4' : flat[3], 'a5' : flat[4], 'a6' : flat[5], 
                                                         'a7' : flat[6], 'a8' : flat[7], 'a9' : flat[8]})
        StuCours.objects.filter(id = course[0].id).update(courseid = option1) 
        StuCours.objects.filter(id = course[1].id).update(courseid = option2)  
        StuCours.objects.filter(id = course[2].id).update(courseid = option3)
        return redirect('http://127.0.0.1:8000/login/menu/result/')
    return render(request, 'modifyresult.html', {"student" : student, "academy" : academy[0], 
                                                  'academycourse1' : academycourse[0].courseid, 
                                                  'academycourse2' : academycourse[1].courseid, 
                                                  'academycourse3' : academycourse[2].courseid,
                                                  'a1' : flat[0], 'a2' : flat[1], 'a3' : flat[2],
                                                  'a4' : flat[3], 'a5' : flat[4], 'a6' : flat[5], 
                                                  'a7' : flat[6], 'a8' : flat[7], 'a9' : flat[8] })
