from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    channel = models.CharField(max_length=100000)

    def __str__(self):
	    return self.name