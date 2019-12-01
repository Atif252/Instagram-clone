from django import forms
from post.models import Post, Comment
# import cloudinary
# import datetime
# import json


# def upload_image(instance, filename, **kwargs):
# 	file_path = 'post/{author}/'.format(
# 			author=str(instance.author)
# 	)
# 	img_request = cloudinary.uploader.unsigned_upload(filename, "insta-clone", 
# 	cloud_name = 'instacloud252', public_id=str(datetime.datetime.now()), folder=file_path)
# 	url = list(img_request.values())[14]
# 	return url

class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('caption', 'image')

	# def save(self, commit=True):
	# 	post = self.instance
	# 	post.caption = self.cleaned_data['caption']
	# 	if self.cleaned_data['image']:
	# 		post.image = self.cleaned_data['image']
	# 		url = upload_image(filename=post.image, instance=post)
	# 		post.image = url
	# 	if commit:
	# 		post.save()
	# 	return post


class UpdatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('caption', 'image')


	def save(self, commit=True):
		post = self.instance
		post.caption = self.cleaned_data['caption']

		if self.cleaned_data['image']:
			post.image = self.cleaned_data['image']

		if commit:
			post.save()
		return post



class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ('comment',)