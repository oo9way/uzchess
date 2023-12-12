from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from course.models import Course, CourseLesson


@receiver(post_save, sender=CourseLesson)
def increase_course_lesson_count(sender, instance, created, **kwargs):
    if created:
        course = Course.objects.get(id=instance.course.id)
        course.increase_lessons_count()

@receiver(pre_delete, sender=CourseLesson)
def decrease_course_lesson_count(sender, instance, **kwargs):
    course = Course.objects.get(id=instance.course.id)
    course.decrease_lessons_count()