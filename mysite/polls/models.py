import datetime

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from taggit.managers import TaggableManager


@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = TaggableManager()

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE, null=True)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

