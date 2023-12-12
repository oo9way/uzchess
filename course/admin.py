from django.contrib import admin
from course.models import Course, CourseCategory, CourseSubscription, CourseLesson, CourseComment

# Register your models here.
admin.site.register([Course, CourseCategory, CourseSubscription, CourseLesson, CourseComment])