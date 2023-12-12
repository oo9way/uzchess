from django.shortcuts import get_object_or_404
from rest_framework import generics, views, response, status
from course import serializers, models, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend



# Course list API view
class CourseAPIView(generics.ListAPIView):
    queryset = models.Course.objects.select_related('category').order_by('-created_at')
    serializer_class = serializers.CourseListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'level', 'category', 'language', 'rating']

# Course create API view
class CourseCreateAPIView(generics.CreateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseCreateUpdateDeleteSerializer
    permission_classes = [IsAdminUser]


# Course Details API View
class CourseDetailsView(generics.RetrieveAPIView):
    queryset = models.Course.objects.select_related('category').prefetch_related('comments')
    serializer_class = serializers.CourseDetailSerializer
    lookup_field = 'slug'


# Course Update API View
class CourseUpdateView(generics.UpdateAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseCreateUpdateDeleteSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]


# Course Destroy API View
class CourseDestroyView(generics.DestroyAPIView):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseCreateUpdateDeleteSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminUser]


# Course Categories
class CourseCategoryAPIView(generics.ListCreateAPIView):
    queryset = models.CourseCategory.objects.all()
    serializer_class = serializers.CourseCategorySerializer
    permission_classes = [permissions.DefaultMethodsPermission]


#Course Comments Create view
class CourseCommentCreateAPIView(generics.CreateAPIView):
    queryset = models.CourseComment.objects.all()
    serializer_class = serializers.CourseCommentCreateDeleteSerializer
    permission_classes = [permissions.DefaultMethodsPermission]

    # Setting user for course comments
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Course Comments Update view
class CourseCommentUpdateAPIView(generics.UpdateAPIView):
    queryset = models.CourseComment.objects.all()
    serializer_class = serializers.CourseCommentUpdateSerializer
    permission_classes = [permissions.DefaultMethodsPermission, permissions.IsOwnerOfObject]


# Course Comments Delete view
class CourseCommentsDeleteAPIView(generics.DestroyAPIView):
    queryset = models.CourseComment.objects.all()
    serializer_class = serializers.CourseCommentCreateDeleteSerializer
    permission_classes = [permissions.DefaultMethodsPermission, permissions.IsOwnerOfObject]


# Course Lessons Create view
class CourseLessonCreateAPIView(generics.CreateAPIView):
    queryset = models.CourseLesson.objects.all()
    serializer_class = serializers.CourseLessonCreateSerializer
    permission_classes = [IsAdminUser]


# Course Lessons Create view
class CourseLessonUpdateAPIView(generics.UpdateAPIView):
    queryset = models.CourseLesson.objects.all()
    serializer_class = serializers.CourseLessonDetailSerializer
    permission_classes = [IsAdminUser]


# Course Lesson Delete view
class CourseLessonDestroyAPIView(generics.DestroyAPIView):
    queryset = models.CourseLesson.objects.all()
    serializer_class = serializers.CourseLessonDetailSerializer
    permission_classes = [IsAdminUser]


# Subscribe to Course
class CourseSubscribeAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_slug):
        course = get_object_or_404(models.Course, slug=course_slug)

        if course.subscribe_user(request.user):
            return response.Response({'details':"Successfully subscribed"}, status=status.HTTP_201_CREATED)
        return response.Response({'details':"User already subscribed to this course"}, status=status.HTTP_208_ALREADY_REPORTED)
        

# Unsubscribe from Course
class CourseUnsubscribeAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_slug):
        course = get_object_or_404(models.Course, slug=course_slug)

        if course.unsubscribe_user(request.user):
            return response.Response({'details':"Successfully unsubscribed"}, status=status.HTTP_200_OK)
        return response.Response({'details':"User not subscribed to this course"}, status=status.HTTP_204_NO_CONTENT)