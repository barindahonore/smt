from django.db import models
from ckeditor.fields import RichTextField


# from citizen.models import Citizens


class Isibo(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Amasibo"
        
    def __str__(self) -> str:
        return self.name


class Stories(models.Model):
    topic = models.CharField(max_length=500)
    content = RichTextField()
    file = models.FileField()
    updated = models.DateTimeField(auto_now = True, auto_now_add=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inkuru z'amateka"

    def __str__(self) -> str:
        return self.topic





