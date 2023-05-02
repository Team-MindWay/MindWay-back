from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, number, username, password=None):
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError('Users must have an email address.')
        if number is None:
            raise TypeError('Users must have a password.')
        if password is None:
            raise TypeError('Users must have a password.')
        
        user = self.model(
            email = email,
            username = username,
            number = number
        )
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, number, username, password):
        if password is None:
            raise TypeError('Users must have a password.')
        
        user = self.create_user(email, number, username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    email = models.EmailField(max_length=254, unique=True)
    number = models.CharField(max_length=4, unique=True, default=None, null=True)
    username = models.CharField(max_length=150, unique=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['number', 'username']

    def __str__(self) -> str:
        return f"{self.number} {self.username}"

class Refresh(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh = models.TextField()

    def __str__(self) -> str:
        return f"{self.user.username} refresh"