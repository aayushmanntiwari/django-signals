import redis
from django.db import models
from django.utils.text import slugify
from django.db.models.fields import SlugField

# Create your models here.

redis_instance = redis.StrictRedis(host='localhost',port=6379, db=0)

class Pizza(models.Model):
    choices = (
        ('Veg','Veg'),
        ('Non-Veg','Non-Veg'),
    )
    name = models.CharField(max_length=225,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    image = models.ImageField(blank=True,null=True,upload_to="pizza/images")
    type = models.CharField(max_length=225,blank=True,null=True,choices=choices)
    slug = models.SlugField(blank=True,unique=True)
    date = models.DateTimeField()

    def __str__(self):
        if self.name is not None:
            return self.name
    
    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Pizza.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug
 
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save(*args, **kwargs)
    

class PizzaOptions(models.Model):
    CHOICES_FOR_SIZE = (
        ("S","S"),
        ("M","M"),
        ("L","L")
    )
    availability = (
        ('available','available'),
        ('Not available','Not available'),
    )
    pizza = models.ForeignKey(Pizza,on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    type = models.CharField(max_length=20,blank=True,null=True,choices=CHOICES_FOR_SIZE)
    status = models.CharField(max_length=100,blank=True,null=True,choices=availability)

    def __str__(self):
        if self.pizza is not None and self.type is not None:
            return self.pizza.name + '_' + self.type 

    def save(self, *args, **kwargs):
        if self.quantity==0:
            self.status = 'Not available'
        super().save(*args, **kwargs)
