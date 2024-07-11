from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    


class posts(models.Model):
    content = models.TextField(max_length=5000)
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts", blank=True)
    likes = models.ManyToManyField(User, related_name="liked")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "account": self.account.get_username(),
            "likes": [user.get_username() for user in self.likes.all()],
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
    
    def __str__(self):
        return f"By {self.account} on {self.timestamp.strftime('%b %d %Y, %I:%M %p')}"