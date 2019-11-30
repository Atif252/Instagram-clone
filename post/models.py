from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete
from django.conf import settings
from django.dispatch import receiver
import string
import random



def upload_location(instance, filename, **kwargs):
	file_path = 'post/{author_id}/{caption}-{filename}'.format(
			author_id=str(instance.author_id), caption=str(instance.caption), filename=filename
		)
	# result = cloudinary.uploader.unsigned_upload(file_path, 'post', **options)
	return file_path


def generate_id():
        n = 11
        return ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=n))


class Post(models.Model):
	caption				= models.CharField(max_length=2200, null=False, blank=True)
	image				= models.ImageField(upload_to=upload_location, null=False, blank=False)
	date_published		= models.DateTimeField(auto_now_add=True, verbose_name="date published")
	date_updated		= models.DateTimeField(auto_now=True, verbose_name="date updated")
	author				= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	slug				= models.SlugField(blank=True, unique=True, max_length=11, default=generate_id)
	likes 				= models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')

	objects = models.Manager()

	def __str__(self):
		return self.slug

	def post_caption(self, caption):
		return caption

	def post_author(self, author):
		return author


class Comment(models.Model):
	post 			= models.ForeignKey(Post, on_delete=models.CASCADE)
	commenter		= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	comment 		= models.CharField(max_length=2200, null=True, blank=False)
	date_commented	= models.DateTimeField(auto_now_add=True, verbose_name="date commented")

	def __str__(self):
		return str(self.commenter) + ": " + self.comment


@receiver(post_delete, sender=Post)
def submission_delete(sender, instance, **kwargs):
	instance.image.delete(False)


def pre_save_blog_post_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.author.username + "-" + instance.caption)

pre_save.connect(pre_save_blog_post_receiver, sender=Post)