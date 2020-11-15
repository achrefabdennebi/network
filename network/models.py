from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import DO_NOTHING


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=250)
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete=DO_NOTHING, related_name="users")
    likes = models.IntegerField(default=0)
    created_date = models.DateTimeField() 

    def serialize(self):
        return {
            "id": self.id,
            "created_by": self.created_by.name,
            "timestamp": self.created_date.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"{self.content[:25] } - {self.created_by} / ({self.created_date.strftime('%b %d %Y, %I:%M %p') })"