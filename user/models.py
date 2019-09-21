from django.db import models
from django.contrib.auth.models import AnonymousUser, AbstractUser

class User(AbstractUser):
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    points = models.IntegerField( blank=True, null=True)
    rank=models.IntegerField(blank=True,null=True)
    verified = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "{}".format(self.first_name)