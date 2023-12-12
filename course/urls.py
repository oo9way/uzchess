from django.urls import path
from course import views

urlpatterns = [
    # Course categories
    path('categories/', views.CourseCategoryAPIView.as_view()),

    # Courses and details
    path('list/', views.CourseAPIView.as_view(), name='course-list'), # List courses
    path('create/', views.CourseCreateAPIView.as_view(), name='course-create'), # Create course
    path('details/<str:slug>/', views.CourseDetailsView.as_view()), # Course details
    path('update/<str:slug>/', views.CourseUpdateView.as_view()), # Update course
    path('delete/<str:slug>/', views.CourseDestroyView.as_view()), # Delete course

    # Course comments
    path('comments/create/', views.CourseCommentCreateAPIView.as_view()), # Create course comment
    path('comments/update/<int:pk>/', views.CourseCommentUpdateAPIView.as_view()), # Update course comment
    path('comments/delete/<int:pk>/', views.CourseCommentsDeleteAPIView.as_view()), # Delete course comment

    # Course lessons
    path('lessons/create/', views.CourseLessonCreateAPIView.as_view()), # Create course lesson
    path('lessons/update/<int:pk>/', views.CourseLessonUpdateAPIView.as_view()), # Update course lesson
    path('lessons/delete/<int:pk>/', views.CourseLessonDestroyAPIView.as_view()), # Delete course lesson

    # Subscribe to course
    path('subscribe/<str:course_slug>/', views.CourseSubscribeAPIView.as_view()), # Subscribe to course
    path('unsubscribe/<str:course_slug>/', views.CourseUnsubscribeAPIView.as_view()), # Unsubscribe to course


]