from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nationality = models.CharField(max_length=100)
    interests = models.TextField()

    def __str__(self):
        return self.user.username

class Group(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    members = models.ManyToManyField(Profile, related_name='groups')

    def __str__(self):
        return self.name

class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    major = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="Student Affairs")
    attendees = models.ManyToManyField(Profile, related_name='attended_events', blank=True)  # 👈 Add this line
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HousingListing(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title
    
class Job(models.Model):
    jobtitle = models.CharField(max_length=100)
    compname = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    compdesc = models.TextField()
    complocation = models.CharField(max_length=100)

    def __str__(self):
        return self.jobtitle

class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:50]

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Job(models.Model):
    jobtitle = models.CharField(max_length=200)
    compname = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    compdesc = models.TextField()
    complocation = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.jobtitle} at {self.compname}"

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.project.title}"

