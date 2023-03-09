from django.db import models
import time

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return "%s" % (self.email)

class Token(models.Model):
    token = models.CharField(max_length=200, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    exp = models.FloatField(default=time.time() + 3600, blank=False)

class Message(models.Model):
    from_user = models.BooleanField(default=False)
    content = models.TextField(blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def get_message(self):
        return {
            'role': 'user' if self.from_user else 'assistant',
            'content': self.content,
        }
