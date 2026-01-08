from django.urls import path
from. import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('student/',views.student_view,name='student'),
    path('teacher/',views.teacher_view,name='teacher'),
    path('about/',views.about_view,name='about'),
    path('contact/',views.contact_view,name='contact'),
]