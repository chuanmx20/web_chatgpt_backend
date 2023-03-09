from django.db import models
import time

# Create your models here.
class User(models.Model):
    email = models.EmailField()

    def __str__(self):
        return "%s" % (self.email)

class Token(models.Model):
    token = models.CharField(max_length=100, unique=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exp = models.DateTimeField(default=time.time() + 3600)

class Message(models.Model):
    from_user = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
