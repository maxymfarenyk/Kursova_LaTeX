from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    email = models.EmailField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if not Profile.objects.filter(user=instance).exists():
            profile = Profile.objects.create(user=instance)
            profile.username = instance.username
            profile.email = instance.email
            profile.save()


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='')
    display_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    version = models.PositiveIntegerField(default=1)  # Поле для відстеження версій

    def save(self, *args, **kwargs):
        # Шукаємо останню версію файлу для цього користувача та файлу
        latest_version = UploadedFile.objects.filter(user=self.user, display_name=self.display_name).order_by(
            '-version').first()

        # Якщо остання версія існує, збільшуємо версію на 1
        if latest_version:
            self.version = latest_version.version + 1

        super(UploadedFile, self).save(*args, **kwargs)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    MARK_CHOICES = [
        ('viewed', 'Viewed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    mark = models.CharField(max_length=20, choices=MARK_CHOICES, null=True, blank=True)
    def __str__(self):
        return f'Comment by {self.user.username} on {self.file.display_name}'