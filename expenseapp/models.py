from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class UserModel(AbstractUser):
    email=models.EmailField(unique=True)

class CategoryModel(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class ExpenseModel(models.Model):
    user=models.ForeignKey(UserModel,on_delete=models.CASCADE)
    category=models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    amount=models.IntegerField()
    date=models.DateField()
    description=models.CharField(max_length=30)

   
    


