from django.db import models

# Create your models here.


class TrialRequest(models.Model):
    email = models.EmailField()
    pseudoID = models.CharField(max_length=20)
    deviceInformation = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)
    checked = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.email
