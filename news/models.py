from django.db import models
from django.utils.text import slugify


# Base Model class
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

# News model
class News(BaseModel):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=150)
    
    body = models.TextField()
    views = models.PositiveIntegerField(default=0)
    
    slug = models.SlugField(unique=True, blank=True)
    cover = models.ImageField(upload_to='data/news/covers/', null=True, blank=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

# Page view counter model
class PageViews(BaseModel):
    news_object = models.ForeignKey(News, on_delete=models.CASCADE)