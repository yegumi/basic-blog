from django.db import models
from django.contrib.auth.models import User

class Relation(models.Model):
    from_user=models.ForeignKey(User,on_delete=models.CASCADE, related_name='followers')
    # from user started to follows to_user
    to_user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="following")
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.from_user} started to follow {self.to_user} at {self.created}'



class UserInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='userinfo',primary_key=True)
    age=models.SmallIntegerField(null=True,blank=True)
    bio=models.TextField(null=True,blank=True)

