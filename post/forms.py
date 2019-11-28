from django import forms
from post.models import Post, Comment


class CreatePostForm(forms.ModelForm):

	class Meta:
		model = Post
		fields = ('caption', 'image')


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