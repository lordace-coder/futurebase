from django.db import models
from django.contrib.auth.models import User

# DATA TYPE FOR FIELDS
# TEXT,URL,NUMBER,DECIMAL,SELECT,JSON


class Column(models.Model):
    DATA_TYPES = (
        ('T','Text Field'),
            ('U','URL Field'),
            ('N','Number Field'),
        ('D','Decimal Field'),
        ('S','Select Field'),
        ('J','JSON Field'),
    )
    name = models.CharField(max_length=100)
    field = models.CharField(max_length=30,choices=DATA_TYPES)
    def __str__(self):
        self.name


# Create your models here.
class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.TextField()
    description = models.TextField(null= True,blank=True)
    created_at = models.DateTimeField(auto_created=True,null= True,blank=True,auto_now_add=True)

    def __str__(self):
        return self.title + " Project"


class Collection(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    columns = models.ManyToManyField(Column)

    def __str__(self):
        return self.name + " Collection"
