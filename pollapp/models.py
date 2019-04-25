from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class MakePoll(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,default = 1)
    question = models.CharField(max_length = 200)
    optionone = models.CharField(max_length = 200)
    optiontwo = models.CharField(max_length = 200)
    optionthree = models.CharField(max_length = 200)
    optionfour = models.CharField(max_length = 200)

    def __str__(self):
        return self.question

class Vote(models.Model):
    poll = models.ForeignKey(MakePoll,on_delete=models.CASCADE)
    vote = models.CharField(max_length = 200)

    def __str__(self):
        return "{}-{}".format(self.poll.question[:],self.vote)
