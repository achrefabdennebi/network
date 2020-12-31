from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import DO_NOTHING

class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=250)
    created_by = models.ForeignKey(User,null=True, blank=True, on_delete=DO_NOTHING, related_name="users")
    created_date = models.DateTimeField() 

    def num_likes (self):
        return Like.objects.filter(post_id=self.id).count()

    def serialize(self):
        return {
            "id": self.id,
            "created_by": self.created_by.name,
            "timestamp": self.created_date.strftime("%b %d %Y, %I:%M %p")
        }

    def __str__(self):
        return f"{self.content[:25] } - {self.created_by} / ({self.created_date.strftime('%b %d %Y, %I:%M %p') })"

class Like(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return u'%s like %s' % (self.user , self.post)

class Follower(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User,on_delete=models.CASCADE, related_name="followers")
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return u'%s follows %s' % (self.follower, self.following)