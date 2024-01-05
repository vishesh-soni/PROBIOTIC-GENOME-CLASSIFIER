from django.db import models
from multiupload.fields import MultiFileField

# Create your models here.
class Kmer(models.Model):
    kmer_file = MultiFileField()

class Pro_file(models.Model):
    pro_seq = models.FileField(upload_to="pro_file")

class Pat_file(models.Model):
    pat_seq = models.FileField(upload_to="pat_file")

class Seq(models.Model):
    sequence = models.FileField(upload_to="seq")

class MLmodel(models.Model):
    ml_file = models.FileField(upload_to="ml_model")