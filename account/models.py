from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_delete, post_save
from django.conf import settings
from django.dispatch import receiver
from post.models import Post



DEFAULT_IMG = 'res.cloudinary.com/instacloud252/image/upload/v1575045629/default-pic_ljw66l.jpg'

def upload_location(instance, filename, **kwargs):
	clean_username = instance.username.replace(" ", "")
	file_path = 'profile-picture/{author_id}/{filename}'.format(
			author_id=str(clean_username), filename=filename
		)

	return file_path


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError("Users must have an Email Address")

		if not username:
			raise ValueError("Users must have an Username")

		user = self.model(
			email= self.normalize_email(email),
			username=username,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):

	GENDER_CHOICES = (
		('male', 'Male'),
		('female', 'Female'),
		('not-specified', 'Not Specified')
	)

	ACCOUNT_CHOICES = (
		('public', 'Public_Account'),
		('private', 'Private_Account')
	)


	email				= models.EmailField(verbose_name="email", max_length=255, unique=True)
	username			= models.CharField(unique=True, max_length=255)
	name				= models.CharField(max_length=255, null=False, blank=False)
	profile_picture		= models.ImageField(upload_to=upload_location, null=False, blank=True, default=DEFAULT_IMG)
	bio					= models.CharField(verbose_name="bio", max_length=150, blank=True, null=False)
	gender				= models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
	account_type		= models.CharField(max_length=80, choices=ACCOUNT_CHOICES, null=False, blank=True, default='public')
	date_joined			= models.DateTimeField(verbose_name="date joined", auto_now=True)
	last_login			= models.DateTimeField(verbose_name="last login", auto_now_add=True)
	is_active			= models.BooleanField(default=True)
	is_admin			= models.BooleanField(default=False)
	is_staff			= models.BooleanField(default=False)
	is_superuser		= models.BooleanField(default=False)
	slug				= models.SlugField(blank=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def get_status(self, instance):
		following_status = Connection.objects.filter(following=instance)
		return following_status



REQUEST_CHOICES = (
    (0, "False"),
    (1, "True"),
)



class Connection(models.Model):
	followers			= models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True,related_name='user_followers')
	following			= models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True,related_name='user_following')
	request				= models.IntegerField(choices=REQUEST_CHOICES, default=0)



class Request(models.Model):
	request_by			= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_requesting')
	target_user			= models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_requested')


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
	instance.profile_picture.delete(False)


def pre_save_account_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.username)

pre_save.connect(pre_save_account_receiver, sender=Account)