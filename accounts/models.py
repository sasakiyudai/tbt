from django.db import models
from timeline.models import Want, Post
from django.contrib.auth.models import AbstractUser
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill

class CustomUser(AbstractUser):
    description = models.TextField(verbose_name='プロフィール', null=True, blank=True)
    photo = models.ImageField(verbose_name='写真', blank=True, null=True, upload_to='images/')
    thumbnail = ImageSpecField(source='photo',
                               processors=[ResizeToFill(256, 256)],
                               format='JPEG',
                               options={'quality': 60})
    github_url = models.CharField(max_length=100, verbose_name='GitHub URL (任意)', null=True, blank=True)

    def get_wanted(self):
        wants = Want.objects.filter(wanting=self)
        res = set()

        for want in wants:
            res.add(want.wanted)
        return res
    
    def get_wanting(self):
        wants = Want.objects.filter(wanted=self)
        res = set()

        for want in wants:
            res.add(want.wanting)
        return res

    class Meta:
        verbose_name_plural = 'CustomUser'

class Comment(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(to=Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(to=CustomUser, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text