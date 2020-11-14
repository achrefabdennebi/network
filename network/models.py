from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import DO_NOTHING


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=250)
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete=DO_NOTHING, related_name="users")
    created_date = models.DateTimeField() 

