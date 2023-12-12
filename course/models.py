from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Base Model class
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Course model
class Course(BaseModel):
    LEVEL_TYPES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    LANGUAGES = (
        ('uz', 'O`zbek tili'),
        ('en', 'Ingliz tili'),
        ('ru', 'Rus tili'),
    )
    
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    price = models.PositiveIntegerField(default=0)
    level = models.CharField(choices=LEVEL_TYPES, max_length=16)
    description = models.TextField()
    category = models.ForeignKey('CourseCategory', on_delete=models.CASCADE)
    lessons_count = models.PositiveIntegerField(default=0)
    language = models.CharField(choices=LANGUAGES, max_length=2, default='uz')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)


    slug = models.SlugField(unique=True, blank=True)

    def is_user_subscribed(self, user):
        if user.is_authenticated:
            return self.subscriptions.filter(user=user, active=True).exists()
        return False
    
    def increase_lessons_count(self):
        self.lessons_count += 1
        self.save()   

    def decrease_lessons_count(self):
        self.lessons_count -= 1
        self.save()    

    def subscribe_user(self, user):
        if not self.is_user_subscribed(user):
            CourseSubscription.objects.create(course=self, user=user)
            return True
        return False

    def unsubscribe_user(self, user):
        if self.is_user_subscribed(user):
            CourseSubscription.objects.get(user=user).delete()
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    
# Course category
class CourseCategory(models.Model):
    title = models.CharField(max_length=128)


# Comments
class CourseComment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    rating = models.DecimalField(decimal_places=1, max_digits=2)


# Course Lessons
class CourseLesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=128)
    body = models.TextField()
    active = models.BooleanField(default=True)


# Subscription
class CourseSubscription(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscriptions')
    active = models.BooleanField(default=True)

