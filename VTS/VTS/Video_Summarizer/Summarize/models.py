from django.db import models

# Create your models here.
class Summary(models.Model):
    link = models.URLField()
    # summary_text = models.FileField()

    def __str__(self):
        return self.link
