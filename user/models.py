from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def _create_user(self, email, password, **kwargs):
        email = self.normalize_email(email)
        user : AbstractUser = self.model(email = email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.update({'is_staff' : True})
        kwargs.update({'is_superuser' : True})
        return self.create_user(email, password, **kwargs)
    

class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    email = models.EmailField(("email address"), unique=True)
    username = models.CharField(
        ("username"),
        max_length=150,
        help_text=(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),

    )
    objects = UserManager()