from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    name = models.CharField(max_length=30, blank=False, unique=True)
    document = models.FileField('File', upload_to='docs/',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])])

    def __str__(self):
        return self.name


class Rating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False)
    rating = models.IntegerField(blank=False)
    review = models.TextField(blank=True, max_length=200)

    def __str__(self):
        return self.user.username + "_review"
