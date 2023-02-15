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
    aws_access_key_id="ASIAT47P6J6FJUKLP4OU"
    aws_secret_access_key="YRUn+F/eEzgsIPhLw5omV+q7cu7f9t+sN5l8CHwa"
    aws_session_token="FwoGZXIvYXdzEGQaDHFb7BPE+MDf00e7YiLAAVkaoEKK4i99TRqr/P1PVM8yCkKl/JIBLVUQ70fO08yxD0+2+NPJlxdv7xY3Yn6S6cpCeMqIwKX57feSEgGru/uWUDicfDLhVHbXYdX9zgZuquroDVJmzdGOVfDnqpMHZyysv0z1s6kBSXUs11/PAJYD/jP89jEnwA70lNwPJFKazDc3Xfbwfms44g4aC/JnHkkIDlsTLRJFKG+Yf0SyrILYyTkun7qny57Y61Zdoa6rglAkw8v5e+3DNYDMFx/6PSiw6aSfBjItoCzcf+JWL/TaoiOMgYswBqdWnhirsoSdHeXtDRp8YtqNdO4Ts+YUpOpAs4x5"
    bucket="trulete-iabd-bucket"
    region="us-east-1"
    

    s3 = boto3.resource('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, aws_session_token=aws_session_token)
    data = open(photo, 'rb')
    s3.Bucket(bucket).put_object(Key=photo, Body=data)

    def recocaras(bucket, key, attributes=['ALL'], region="us-east-1"):
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
 
    output=recocaras(bucket, photo)
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