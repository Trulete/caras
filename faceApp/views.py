from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import GalleryImageForm
from .models import GalleryImage
import boto3
import json
from pathlib import Path
from django.http import JsonResponse

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
    print(id)
    object=GalleryImage.objects.get(id = id)
    return render(request, "faceApp/show_image.html", { "data": object })

#ajax: detergente, futbol, cantante, web
def ajax(request, id):
    list=[]
    list.append({"x":1, "y":3})
    list.append({"x":3, "y":4})
    return JsonResponse(list, safe= False)

def usaajax(request):
    return render(request, "faceApp/usaajax.html")
    #object=GalleryImage.objects.get(id = id)
    #subo s3
    #analizo rek
    #filtro resultado: json{array de coordenadas de los menores de edad}

def detect_faces(request, photo):
    aws_access_key_id="ASIAYYLDTHNX4C3K3MSN"
    aws_secret_access_key="WhNBif6YrDzawX4CM/l3srmp4rbwIY9nNOqkJzaM"
    aws_session_token="FwoGZXIvYXdzECIaDOOP+kOCZj730f9+0SK8AVaPYeaLjAnL18dDfU4Bhk8vmU/VlKk08F8HESoJ7V/1Dh4X6Qdg0EzDrDI1k07zU+0KNXqymonY5aFGpLx2DOheudhtbaLMM/k7kmFOaY7JBDyoAEDMww4Hq6Ul28Sm8HBs0WZLDCPHScrRGMCuWrnU54SfAybGvxWpKqH7CqD4JjAe2ZFzAzzMsxv0m7TppHSDjwqU//kBBJg3xRQbeggvEM5YkJTTQJnZyaQotzdWOqZl2kgBbI3691ZLKKfYpZ4GMi1Eb6Y5DiHNYObq9TNoqTB+p0DGeERpwIrKjNOW0qL0dyIhrUISVYxSq5giucM="
    bucket="iabd-ickkck-aws-bucket"
    region="us-east-1"
    

    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    data = open(photo, 'rb')
    s3.Bucket(bucket).put_object(Key=photo, Body=data)

    def caritas(bucket, key, attributes=['ALL'], region="us-east-1"):
        rekognition = boto3.client("rekognition", region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
        response = rekognition.detect_faces(
            Image={
                "S3Object": {
                    "Bucket": bucket,
                    "Name": photo,
                }
            },
            Attributes=attributes,
        )
        return response
 
    output=caritas(bucket, photo)
    print(output)

    d = open("salida.json", "w")
    json.dump(output,d)

    f=open("salida.json","r")
    content = f.read()
    jsondecoded=json.loads(content)

    return 
    for entity in jsondecoded["FaceDetails"]:
        entityName= entity["AgeRange"]["Low"]
        if entityName < 18:
            print(entity["BoundingBox"])