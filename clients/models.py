from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=64)
    photo = models.ImageField(upload_to='users', blank=True, null=True)

    def __str__(self):
        return self.name
