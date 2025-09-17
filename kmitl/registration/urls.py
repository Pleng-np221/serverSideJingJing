from django.urls import path

from . import views


urlpatterns = [
    # ex: /polls/
    path("", views.StudentView.as_view(), name="index"),
    path("professor/", views.ProfessorView.as_view(), name="professor"),
    path("course/", views.CourseView.as_view(), name="course"),
    path("faculty/", views.FacultyView.as_view(), name="faculty"),
    path("create_student/", views.CreateStudentView.as_view(), name="create_student"),
    path("update_student/", views.UpdateStudentView.as_view(), name="update_student"),
]