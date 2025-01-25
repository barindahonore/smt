from django.db import models

from authentication.models import CustomUser
from datetime import date
from django.utils import timezone

from core.models import Isibo

class Citizens(models.Model):
    GENDER_CHOICES = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    profile_picture = models.ImageField(upload_to='media/profiles', default='/media/profiles/default.png')
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    is_employed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.first_name
    
    class Meta:
        verbose_name_plural = "Citizens"


class Family(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    members = models.ManyToManyField(Citizens)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Families"


class Messages(models.Model):
    PURPOSE_CHOICES = (
        ('Ikibazo', 'Ikibazo'),
        ('Igitekerezo', 'Igitekerezo'),
        ('Ubufasha', 'Ubufasha'),
        ('Kunenga/Gushima', 'Kunenga/Gushima'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    topic = models.CharField(max_length=500)
    purpose = models.CharField(max_length=20, default='Ikibazo', choices=PURPOSE_CHOICES)
    urgent = models.BooleanField(default=False)
    message = models.TextField()
    reply = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now = True, auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.sender.username
    
    class Meta:
        verbose_name_plural = "Messages"


class Events(models.Model):
    title = models.CharField(max_length=20, default='Upcoming Activity')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)
    # is_expired = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.title
    
    def remaining_days(self):
        today = date.today()
        if self.start_date.date() > today:
            return (self.start_date.date() - today).days
        elif self.start_date == today:
            return 0
        return -1
    
    def period(self):
        return (self.end_date - self.start_date).days
    
    def check_expired(self):
        self.is_expired = self.start_date < timezone.now().date()
        self.save()


class Files(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    file = models.FileField(upload_to='media/files/')
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name_plural = "Files"

    


class Post(models.Model):
    post = models.CharField(max_length=100)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.post
    
    def remaining_days(self):
        today = date.today()
        if self.start_date > today:
            return (self.start_date - today).days
        elif self.start_date == today:
            return 0
        return -1
    class Meta:
        verbose_name="Imyanya itorerwa"
        verbose_name_plural="Imyanya itorerwa"
    
class Abakandida(models.Model):
    citizen = models.ForeignKey(Citizens, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.citizen.first_name
    
class Votes(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.user.username
    
class Kwimuka(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    isibo = models.ForeignKey(Isibo, on_delete=models.CASCADE)
    approve = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self) -> str:
        return self.user.username
    
    def save(self, *args, **kwargs):
        if self.approve:
            self.user.isibo = self.isibo
            self.user.save()
        super(Kwimuka, self).save(*args, **kwargs)
    @classmethod
    def get_latest_for_user(cls, user):
        try:
            return cls.objects.filter(user=user).latest('created')
        except cls.DoesNotExist:
            return None
