from django.db import models


# Base Model class
class BaseModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

class Book(BaseModel):
    LEVELS = (
        ('beginner', "Beginner"),
        ('intermediate', "Intermediate"),
        ('advanced', "Advanced"),
    )
    
    title = models.CharField(max_length=255)
    price = models.DecimalField(decimal_places=2, default="0.00", max_digits=10)
    discount_price = models.DecimalField(decimal_places=2, default="0.00", max_digits=10)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='data/books/covers/', blank=True, null=True)
    level = models.CharField(max_length=15, choices=LEVELS, default='beginner')
    author = models.CharField(max_length=255, null=True, blank=True)
    pages_count = models.IntegerField(default=0)
    publish_date = models.DateField(null=True, blank=True)

