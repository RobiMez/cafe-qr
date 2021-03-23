from django.db import models

# Create your models here.

class user(models.Model):
    name            = models.TextField()
    is_female       = models.BooleanField(default=False, null=True)
    dob             = models.TextField()
    enrollment      = models.TextField(default='undefined')
    uid             = models.TextField(default='GUR/00000/12')
    term            = models.TextField(default='undefined')
    contact         = models.TextField(default='undefined')
    access          = models.TextField(default='undefined')