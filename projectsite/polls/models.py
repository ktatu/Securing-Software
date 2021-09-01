import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    pub_date = models.DateTimeField('date published', default=timezone.now())


class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
