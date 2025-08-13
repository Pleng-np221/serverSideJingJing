from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count, Value
from django.db.models.functions import Concat
from .models import *


class StudentView(View):

    def get(self, request):
        
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")
        #filters = []
        if (filter_type == ""):
            student_list = Student.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(full_name__icontains = search_txt )
            #filters["full_name__icontain"] = search_txt
        elif (filter_type == "email"):
            student_list = Student.objects.filter(studentprofile__email__icontains = search_txt )
            #filters["studentprofile__email__icontain"] = search_txt
        elif (filter_type == "faculty"):
            student_list = Student.objects.filter(faculty__name__icontains = search_txt )
            #filters["faculty__name__icontain"] = search_txt
        else:
            student_list = Student.objects.all()
        context = {
            "student_list": student_list,
            "total": student_list.count()
                   }
        #student_list = Student.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(**filters)
        return render(request, "index.html", context)
    
class ProfessorView(View):

    def get(self, request):

        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")
        if (filter_type == ""):
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(full_name__icontains = search_txt )
        elif (filter_type == "faculty"):
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(faculty__name__icontains = search_txt )
        else:
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name"))
        context = {
            "professor_list": professor_list,
            "total": professor_list.count()
                   }
        return render(request, "professor.html", context)
    
class CourseView(View):

    def get(self, request):
        course_list = Course.objects.all()
        context = {
            "course_list": course_list,
            "total": course_list.count()
                   }
        return render(request, "course.html", context)
    
class FacultyView(View):

    def get(self, request):
        search_txt = request.GET.get("search")
        if (search_txt == None):
            faculty_list = Faculty.objects.annotate(num_professors = Count("professor", distinct = True), num_students = Count("student", distinct = True))
        else:
            faculty_list = Faculty.objects.annotate(num_professors = Count("professor", distinct = True), num_students = Count("student", distinct = True)).filter(name__icontains = search_txt)
        
        context = {
            "faculty_list": faculty_list,
            "total": faculty_list.count()
                   }
        return render(request, "faculty.html", context)

class CreateStudentView(View):

    def get(self, request):
        student_list = Student.objects.all()
        faculties = Faculty.objects.all()
        sections = Section.objects.all()
        context = {
            "student_list": student_list,
            "total": student_list.count(),
            "faculties": faculties,
            "sections": sections
                   }
        return render(request, "create_student.html", context)
    
    def post(self, request):
        student_id = request.POST.get('student_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        faculty = request.POST.get('faculty')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = phone = request.POST.get('address')
        #new_student = Student.objects.create(student_id = student_id, first_name = first_name, last_name = last_name, )
        return redirect("index")