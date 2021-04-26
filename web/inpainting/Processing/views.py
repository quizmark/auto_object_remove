from django.shortcuts import render
from django.http import HttpResponse
from static.python import ModelUpdate
from django.contrib.auth.models import User
from datetime import datetime
import random
import base64
import re
import os
import subprocess
import shutil
from cv2 import cv2
import numpy as np


def process(request):
    # username=str(random.randint(1,100000))
    # request.user = User.objects.create_user(username=username,first_name='Anonymous',last_name='User')
    # request.user.set_unusable_password()
    # request.user.save()
    # u = User.objects.get(username = username)
    # u.delete()
    return render(request,'web/Mainprocess.html')

def contact(request):
    return render(request,'web/member.html')

def create_model(request):
    ModelUpdate.insert_value(request.POST['value'])

    print(request.POST['value'])
    return HttpResponse(request.POST['value'])

def upload_image(request):
    #print(request.POST['preview'])

    imgdata=base64.b64decode(re.search(r'base64,(.*)', request.POST['preview']).group(1))
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y-%H-%M-%S-%f")
    file='media/FileUpload-'+timestampStr+'.jpg'
    with open(file,'wb') as f:
        f.write(imgdata)
    return HttpResponse(file)

def process_image(request):
    if request.POST['selection']=="1":
        current_dir = os.getcwd()
        current_dir = current_dir.replace("\\","/")
        image_dir = current_dir+"/"+request.POST['file']
        #print(image_dir)
        project_dir = "E:/MainProject"
        subprocess.call(["python","demo.py","--input",image_dir,
            "--selection","1"],cwd=project_dir)
        shutil.copy(project_dir+"/generative_inpainting/result/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:],
                    current_dir+"/media/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:])
        return HttpResponse("/media/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:])
    elif request.POST['selection']=="2":
        img=np.zeros((500,500),dtype=np.uint8)
        arr = request.POST.getlist('arr[]')
        for val in arr:
            temp=val.split('_')
            temp[0]=int(temp[0])
            temp[1]=int(temp[1])
            temp[2]=int(temp[2])
            temp[3]=int(temp[3])

            temp[2]=temp[0]+temp[2]
            if temp[2]<temp[0]:
                temp[0],temp[2]=temp[2],temp[0]

            temp[3]=temp[1]+temp[3]
            if temp[3]<temp[1]:
                temp[1],temp[3]=temp[3],temp[1]

            img[temp[1]:temp[3]+1,temp[0]:temp[2]+1]=255
        
        current_dir = os.getcwd()
        current_dir = current_dir.replace("\\","/")
        image_dir = current_dir+"/"+request.POST['file']
        project_dir = "E:/MainProject"
        src=cv2.imread(image_dir)
        img=cv2.resize(img,(src.shape[1],src.shape[0]))
        cv2.imwrite('E:/MainProject/PoolNet/results/run-1-sal-e1/'
            +image_dir.split('/')[-1],img)
        subprocess.call(["python","demo.py","--input",image_dir,
            "--selection","2"],cwd=project_dir)
        
        shutil.copy(project_dir+"/generative_inpainting/result/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:],
                    current_dir+"/media/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:])
        return HttpResponse("/media/"+image_dir.split('/')[-1][:-4]+"_output"+image_dir.split('/')[-1][-4:])
# Create your views here.
