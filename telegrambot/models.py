from django.db import models

# Create your models here.
class Call(models.Model):
    button_name = models.CharField(max_length=10)
    count = models.IntegerField()

class User(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user_name = models.TextField(null=True, unique=True)
    first_name = models.TextField(null=True)
    calls = models.IntegerField()
