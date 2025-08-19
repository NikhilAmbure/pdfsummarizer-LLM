from django.db import models

# Create your models here.


class pdf_upload(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')

