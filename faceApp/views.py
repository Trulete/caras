from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import GalleryImageForm
from .models import GalleryImage
import boto3
from botocore.exceptions import NoCredentialsError
import json
from pathlib import Path
from django.http import JsonResponse
import cv2
import numpy as np
from PIL import Image

def index(request):
    print("index")
    context = {"valor":"texto"}
    return render(request, "faceApp/index.html", context)

def detalle(request, iddetalle):
    return HttpResponse("detalle %s." % iddetalle)

def upload(request):
    print(request)
    form = GalleryImageForm()
    print(form)
    return render(request, "faceApp/upload.html", { "form": form })

def manage_upload(request):
    if request.method == "POST":
        form = GalleryImageForm(request.POST, request.FILES)
        if form.is_valid():
            object=form.save()
            return redirect("faceApp:show_image", id=object.id)
    return redirect("faceApp:index")

def show_image(request, id):    
    aws_access_key_id="ASIAT47P6J6FH3S6NTMU"
    aws_secret_access_key="yenlhoQIcmiJMNwWqWkWTXVwy49v86NL7RxXLhqV"
    aws_session_token="FwoGZXIvYXdzEJv//////////wEaDHPwF1xOYvyamh88cCLAAW3eZNW7Gnz7uEGmDAi0AiWZSex47xdSI/Wqf5aHKNEkMv8uPnEV77mOZp1VS8xuzqngpD4XlhEwZiidkgwUr5/cdjdhqtu5vnbl9J3t37BVaGjWcaP+1MNR8xXcxHq09S79foMjCpgS8Bl+57afqhtAFiKfNI1AW8Ez+qGmrYgHtXbe7zLgFh71vu0g3KA1dUwOWCYBRey3vnUal3O5zQm56WFH1RrsY605RvuycJ+yqjj4r+6TjJdz1+EwjT9smyiz6ZGhBjItxH57s2A0EVTflgB3KWd7J4z32M4h9tWqmhHQckpm7iRfAai3XQvSgSXkc5iy"
    bucket="trulete-iabd-bucket"
    zona="us-east-1"
    imgobject=GalleryImage.objects.get(id = id)
    fullpath = "c:/iabd/pia/django/caras" + imgobject.image.url
    photo = open(fullpath)
    
    def SubeS3(local_file, bucket, s3_file):
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token)
        s3.upload_file(local_file, bucket, s3_file)
    
    SubeS3(fullpath, bucket, 'Reconoce.jpg')
    
    reko = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,aws_session_token=aws_session_token, region_name=zona)
    resultado = reko.detect_faces(Image={'S3Object': {'Bucket': bucket, 'Name': 'Reconoce.jpg'}}, Attributes=['ALL'])

    image = cv2.imread(fullpath)

    menores = []
    for i in resultado['FaceDetails']:
        if i['AgeRange']['Low'] <= 18:
            bounding_box = i['BoundingBox']
            left = int(bounding_box['Left'] * image.shape[1])
            top = int(bounding_box['Top'] * image.shape[0])
            width = int(bounding_box['Width'] * image.shape[1])
            height = int(bounding_box['Height'] * image.shape[0])
            # menores.append({left, top, width, height})
            menores.append({'left':left,'top':top,'width':width,'height':height})

    with open("faceApp/static/faceApp/assets/menores.json", "w") as outfile:
        json.dump(menores, outfile)
        outfile.close()

    print(id)
    object=GalleryImage.objects.get(id = id)
    return render(request, "faceApp/show_image.html", { "data": object })

def blur_image(request):

    id = request.POST['imagen']
    coords = request.POST['coordenadas']
    object = GalleryImage.objects.get(id = id)
    
    #img = cv2.imread("c:/iabd/pia/django/caras"+object.image.url)
    img = Image.open("c:/iabd/pia/django/caras"+object.image.url)
    new_file = 'imagen_final.jpg'
    #img_cv2 = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    img_cv2 = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2RGBA)
    for item in json.loads(coords):
        x = int(item[0])
        y = int(item[1])
        w = int(item[2])
        h = int(item[3])
        img_cv2[y : y + h, x : x + w] = cv2.GaussianBlur(img_cv2[y : y + h, x : x + w], (31,31), 0)
    cv2.imwrite('faceApp/static/faceApp/assets/img/'+new_file, img_cv2)
    
    
    
    return redirect("faceApp:show_blur_image",id='imagen_final.jpg')
    #return render(request, "faceApp/show_image_2.html", { "data": object })

def show_blur_image(request,id):
    #object = GalleryImage.objects.get(id = id)
    return render(request, "faceApp/show_image_2.html", { "data": id })

