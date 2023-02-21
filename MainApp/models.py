from django.db import models

# Create your models here.
class CSVUpload(models.Model):
    csv_file = models.URLField(max_length=200)
    timeframe = models.IntegerField()
    json_file = models.URLField(max_length=200)