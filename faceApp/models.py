from django.db import models

# Create your models here.
class GalleryImage(models.Model):
    title = models.CharField(max_length=255)
    image= models.ImageField(upload_to="faceApp/gallery_images")