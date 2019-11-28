from django.db import models
from django.conf import settings



class Stories(models.Model):
	image	 			= models.ImageField()