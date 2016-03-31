from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=10)
    middle_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=15)
    email = models.EmailField(unique=True, max_length=25)
    mobile_no = models.CharField(max_length=12)
    admin_approval = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s-%s-%s" %(self.first_name, self.email, self.admin_approval)
