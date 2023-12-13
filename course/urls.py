from django.urls import path
from course import views

urlpatterns = [
    # Course categories
    path('categories/', views.CourseCategoryAPIView.as_view()),

    # Courses and details
    path('list/', views.CourseAPIView.as_view(), name='course-list'), # List courses #Tested
    path('create/', views.CourseCreateAPIView.as_view(), name='course-create'), # Create course #Tested
    path('details/<str:slug>/', views.CourseDetailsView.as_view(), name='course-details'), # Course details #Tested
    path('update/<str:slug>/', views.CourseUpdateView.as_view(), name='update-course'), # Update course #Tested
    path('delete/<str:slug>/', views.CourseDestroyView.as_view(), name='delete-course'), # Delete course #Tested

    # Course comments
    path('comments/create/', views.CourseCommentCreateAPIView.as_view(), name='create-comment'), # Create course comment #Tested
    path('comments/update/<int:pk>/', views.CourseCommentUpdateAPIView.as_view(), name='update-comment'), # Update course comment #Tested
    path('comments/delete/<int:pk>/', views.CourseCommentsDeleteAPIView.as_view(), name='delete-comment'), # Delete course comment #Tested

    # Course lessons
    path('lessons/create/', views.CourseLessonCreateAPIView.as_view(), name='create-lesson'), # Create course lesson #Tested
    path('lessons/update/<int:pk>/', views.CourseLessonUpdateAPIView.as_view(), name='update-lesson'), # Update course lesson
    path('lessons/delete/<int:pk>/', views.CourseLessonDestroyAPIView.as_view(), name='delete-lesson'), # Delete course lesson

    # Subscribe to course
    path('subscribe/<str:course_slug>/', views.CourseSubscribeAPIView.as_view()), # Subscribe to course
    path('unsubscribe/<str:course_slug>/', views.CourseUnsubscribeAPIView.as_view()), # Unsubscribe to course


]