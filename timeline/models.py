from django.db import models
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

class Post(models.Model):
	author = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	text = models.TextField(verbose_name='本文')
	station = models.TextField(verbose_name='場所')
	photo = models.ImageField(verbose_name='写真', upload_to='images/')
	post_photo = ImageSpecField(source='photo',processors=[ResizeToFit(1080, 1080)],format='JPEG',options={'quality':60})
	created_at = models.DateTimeField(auto_now_add=True, blank=True)
	traded = models.BooleanField(default=False, blank=True)

	def get_like(self):
		likes = Like.objects.filter(post=self)
		return [like.user for like in likes]
	
	def get_notations(self):
		notations = Notation.objects.filter(post=self)
		return [notation.user for notation in notations]

class Like(models.Model):
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
	post = models.ForeignKey('Post', on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user', 'post')

class Notation(models.Model):
	user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="notations")
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="notations")

	class Meta:
		unique_together = ('user', 'post')

class Want(models.Model):
	wanting = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="wanting")
	wanted = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name="wanted")

	# class Meta:
	# 	unique_together = ('wanting', 'wanted')
