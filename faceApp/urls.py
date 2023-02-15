from django.urls  import path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name= "faceApp"

urlpatterns=[
    path("", views.index, name="index"),
    path("face/", views.index, name="face"),
    path("upload/", views.upload, name="upload"),
    path("manage_upload/", views.manage_upload, name="manage_upload"),
    path("show_image/<int:id>", views.show_image, name="show_image"),
    path("<int:iddetalle>/detalle", views.detalle, name="detalle"),
    path("detalle/<int:iddetalle>", views.detalle, name="detalle2"),
    path("ajax/", views.ajax, name="ajax"),
    path("usaajax/", views.usaajax, name="usaajax"),
    path("gallery_images/", views.usaajax, name="usaajax"),
    path("detect_faces/", views.detect_faces, name="detectfaces"),

    
]
if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )


