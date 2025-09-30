from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Count, Value
from django.db.models.functions import Concat
from .models import *
from .forms import *

from django.conf import settings
from django.core.files.storage import FileSystemStorage

class StudentView(View):

    def get(self, request):
        
        search_txt = request.GET.get("search")
        filter_type = request.GET.get("filter")
        #filters = []
        if (filter_type == "email"):
            student_list = Student.objects.filter(studentprofile__email__icontains = search_txt )
            #filters["studentprofile__email__icontain"] = search_txt
        elif (filter_type == "faculty"):
            student_list = Student.objects.filter(faculty__name__icontains = search_txt )
            #filters["faculty__name__icontain"] = search_txt
        elif (search_txt):
            student_list = Student.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(full_name__icontains = search_txt )
            #filters["full_name__icontain"] = search_txt
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
        if (filter_type == "faculty"):
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(faculty__name__icontains = search_txt )
        elif (search_txt):
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name")).filter(full_name__icontains = search_txt )

        else:
            professor_list = Professor.objects.annotate(full_name = Concat("first_name", Value(" "), "last_name"))
        context = {
            "professor_list": professor_list,
            "total": professor_list.count()
                   }
        return render(request, "professor.html", context)
    
class CourseView(View):

    def get(self, request):
         
        search_txt = request.GET.get("search")
        if (search_txt):
            course_list = Course.objects.filter(course_name__icontains = search_txt)
        else:
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

# class CreateStudentView(View):

#     def get(self, request):
#         student_list = Student.objects.all()
#         faculties = Faculty.objects.all()
#         sections = Section.objects.all()
#         form = StudentForm()
#         context = {
#             "student_list": student_list,
#             "total": student_list.count(),
#             "faculties": faculties,
#             "sections": sections,
#             "form": form,
#                    }
#         return render(request, "create_student.html", context)
    
#     def post(self, request):
#         student_id = request.POST.get('student_id')
#         first_name = request.POST.get('first_name')
#         last_name = request.POST.get('last_name')
#         faculty = request.POST.get('faculty')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         address = request.POST.get('address')
#         section_ids = request.POST.getlist('section_ids')
#         new_student = Student.objects.create(student_id = student_id, first_name = first_name, last_name = last_name, faculty_id = faculty)
#         student_profile = StudentProfile.objects.create(student = new_student, email = email, phone_number = phone_number, address = address)
#         if (section_ids):
#             new_student.enrolled_sections.add(*section_ids)
#             new_student.save()
#         return redirect("index")
class CreateStudentView(View):

    def get(self, request):
        stdform = StudentForm()
        pfform = StudentProfileForm()
        context = {
            "stdform": stdform,
            "pfform": pfform,
        }
        return render(request, "create_student.html", context)
    
    def post(self, request):
        stdform = StudentForm(request.POST)
        pfform = StudentProfileForm(request.POST, request.FILES)

        if stdform.is_valid() and pfform.is_valid():
            student = stdform.save()
            profile = pfform.save(commit=False)
            profile.student = student
            # student.save()
            profile.save()

            return redirect('index')

        return render(request, "create_student.html", {
            "stdform": stdform,
            "pfform": pfform,
        })
    
class UpdateStudentView(View):

    # def get(self, request):
    #     # student_id = request.GET.get('student_id')
    #     # student = Student.objects.get(student_id=student_id)

    #     id = request.GET.get('id')
    #     student = Student.objects.get(pk=id)

    #     faculties = Faculty.objects.all()
    #     sections = Section.objects.all()

    #     form = StudentForm(initial=
    #             {"student_id": student.student_id,
    #              "first_name": student.first_name,
    #              "last_name": student.last_name,
    #              "faculty": student.faculty,
    #              "email": student.studentprofile.email,
    #              "phone_number": student.studentprofile.phone_number,
    #              "address": student.studentprofile.address,
    #             }
    #         )
    #     context = {
    #         "student": student,
    #         "form": form,
    #         "faculties": faculties,
    #         "sections": sections
    #                }
    #     return render(request, "update_student.html", context)
    # def post(self, request):
    #     # id = request.POST.get('id')
    #     student_id = request.POST.get('student_id')
    #     first_name = request.POST.get('first_name')
    #     last_name = request.POST.get('last_name')
    #     faculty = request.POST.get('faculty')
    #     email = request.POST.get('email')
    #     phone_number = request.POST.get('phone_number')
    #     address = request.POST.get('address')
    #     section_ids = request.POST.get('enrolled_sections')
    #     print(section_ids)
    #     update_student = Student.objects.get(student_id = student_id)
    #     update_student = Student.objects.get(student_id=student_id)
    #     update_student.first_name = first_name
    #     update_student.last_name = last_name
    #     update_student.faculty_id = faculty
    #     update_student.save()
    #     profile = StudentProfile.objects.get(student = update_student)
    #     profile.email = email
    #     profile.phone_number = phone_number
    #     profile.address = address
    #     profile.save()

    #     if (section_ids):
    #         update_student.enrolled_sections.add(*section_ids)
    #         update_student.save()
    #     return redirect("index")
    def get(self, request):
        id = request.GET.get('id')
        student = Student.objects.get(pk=id)

        # Bind student + profile to forms
        stdform = StudentForm(instance=student)
        pfform = StudentProfileForm(instance=student.studentprofile)

        context = {
            "student": student,
            "stdform": stdform,
            "pfform": pfform,
        }
        return render(request, "update_student.html", context)

    def post(self, request):
        id = request.POST.get('id')
        student = Student.objects.get(pk=id)

        stdform = StudentForm(request.POST, instance=student)
        pfform = StudentProfileForm(request.POST, instance=student.studentprofile)

        if stdform.is_valid() and pfform.is_valid():
            student = stdform.save()
            profile = pfform.save(commit=False)
            profile.student = student
            profile.save()

            return redirect("index")

        return render(request, "update_student.html", {
            "student": student,
            "stdform": stdform,
            "pfform": pfform,
        })
    
class CreateCourseView(View):

    def get(self, request):
        cform = CourseForm()
        sform = SectionForm()
        context = {
            "cform": cform,
            "sform": sform,
        }
        return render(request, "create_course.html", context)
    
    def post(self, request):
        cform = CourseForm(request.POST)
        sform = SectionForm(request.POST)

        if cform.is_valid() and sform.is_valid():
            course = cform.save(commit=False)
            section = sform.save(commit=False)
            section.course = course
            course.save()
            section.save()

            return redirect('course')
        print("cform:", cform.errors)
        print("sform:", sform.errors)
        return render(request, "create_course.html", {
            "cform": cform,
            "sform": sform,
        })
    
class UpdateCourseView(View):

    def get(self, request):
        id = request.GET.get('id')
        course = Course.objects.get(pk=id)
        section = Section.objects.get(course=course)
        cform = CourseForm(initial=
                {"course_code": course.course_code,
                "course_name": course.course_name,
                "credits": course.credits
                }
            )
        sform = SectionForm(initial=
                {"section_number": section.section_number,
                "semester": section.semester,
                "professor": section.professor,
                "day_of_week": section.day_of_week,
                "start_time": section.start_time,
                "end_time": section.end_time,
                "capacity": section.capacity,
                }
            )
        
        context = {
            "cform": cform,
            "sform": sform,
                   }
        return render(request, "create_course.html", context)
    
    # def post(self, request):
    #     cform = CourseForm(request.POST)
    #     sform = SectionForm(request.POST)

    #     if cform.is_valid() and sform.is_valid():
    #         course = cform.save(commit=False)
    #         section = sform.save(commit=False)
    #         section.course = course
    #         course.save()
    #         section.save()

    #         return redirect('course')
    #     print("cform:", cform.errors)
    #     print("sform:", sform.errors)
    #     return render(request, "create_course.html", {
    #         "cform": cform,
    #         "sform": sform,
    #     })
    
    def post(self, request):
        id = request.GET.get('id')
        course = Course.objects.get(pk=id)
        cform = CourseForm(request.POST, instance=course)
        section = Section.objects.get(course=course)
        sform = SectionForm(request.POST, instance=section)
        # save if valid                                       
        if cform.is_valid() and sform.is_valid():
            course = cform.save(commit=False)
            section = sform.save(commit=False)
            section.course = course
            course.save()
            section.save()

            return redirect('course')

        return render(request, "create_course.html", {
            "cform": cform,
            "sform": sform,
        })