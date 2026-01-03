from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

# AbstractUser = add/modify any fields
# AbstractBaseUser = we use this if you want to full control over your model. 
# BaseUserManager = Employee.object = Manager

# app name should be plural
# Model name should be capital letter start
# view/function name should be small letter format

# CustomUser model =

class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email" # login field will be email.
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email