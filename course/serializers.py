from rest_framework import serializers
from course.models import CourseCategory, Course, CourseComment, CourseLesson


# Course Comments
class CourseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('body', 'rating', 'user')


# Course Comment serializer for Create and Delete
class CourseCommentCreateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('course', 'body', 'rating',)


# Course Comment serializer for Update
class CourseCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseComment
        fields = ('body', 'rating',)


#Course category
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ('title',)


# Course Lessons detail serializer
class CourseLessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ('title', 'body', 'active')

# Course Lessons create serializer
class CourseLessonCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ('course','title', 'body', 'active')


# Course list
class CourseListSerializer(serializers.ModelSerializer):
    category = CourseCategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


# Course details
class CourseDetailSerializer(serializers.ModelSerializer):
    is_user_subscribed = serializers.SerializerMethodField()
    category = CourseCategorySerializer(read_only=True)
    comments = CourseCommentSerializer(many=True, read_only=True)
    lessons = CourseLessonDetailSerializer(many=True, read_only=True)

    def get_is_user_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.is_user_subscribed(request.user)
        return False
    
    class Meta:
        model = Course
        fields = "__all__"


# Course Create and Update
class CourseCreateUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('title','author', 'price', 'description', 'category', 'language', 'rating')


