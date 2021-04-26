import argparse
import os
import numpy as np
import shutil
import glob
import cv2
import subprocess

def DeleteAllFileinFolder(path):
    dir=os.listdir(path)
    for file in dir:
        print(file)
        os.remove(path+"/"+file)

def SalientObject(args):
    if "/"in args.input:
        image_name = args.input.split('/')[-1]
    else :
        image_name = args.input.split("\\")[-1]
    shutil.copy(args.input,'PoolNet/data/ECSSD/Imgs1/'+image_name)
    file=open("E:/MainProject/PoolNet/data/ECSSD/test1.lst","w")
    file.write(image_name)
    file.close()
    #subprocess.Popen(r"C:/Users/nglam/anaconda3/python.exe",cwd='E:/MainProject/PoolNet')
    subprocess.call(["python","joint_main.py","--mode","test","--model","results/run-1/models/final.pth"
                            ,"--test_fold","results/run-1-sal-e1","--sal_mode","e","--output",image_name],cwd='PoolNet')

def ObjectSegmentation(args):
    image_name = args.input.split('/')[-1]
    current_dir = os.getcwd()
    current_dir = current_dir.replace("\\", "/")
    subprocess.call(["python","demo/centermask_demo.py","--config-file","configs/centermask/centermask_V_99_eSE_FPN_ms_3x.yaml","--weights","centermask-V2-99-FPN-ms-3x.pth"
                     ,"--conf_th","0.1","--display_text","True","--display_scores","True","--input",args.input,"--output_dir","output"
                     ,"--salient",current_dir+"/PoolNet/results/run-1-sal-e1/"+image_name
                     ,"--map_dir",current_dir+"/generative_inpainting/result/"+image_name[:-4]+"_mask"+image_name[-4:]
                     ,"--selection",str(args.selection)],cwd='CenterMask')
    shutil.copy(args.input, 'generative_inpainting/result/'+image_name[:-4]+"_input"+image_name[-4:])

def PhatHienVatTheKhongNoiBat(args):
    salientFolder= os.listdir('PoolNet/results/run-1-sal-e1')
    for img in salientFolder:
        salientMap=cv2.imread('PoolNet/results/run-1-sal-e1/'+img,0)
        ret,salientMap=cv2.threshold(salientMap,96,255,cv2.THRESH_BINARY)

    maskNotSalient=np.zeros(shape=(salientMap.shape[0],salientMap.shape[1],1),dtype=np.uint8)
    MaskObjectFolder=os.listdir('CenterMask/output')
    for img in MaskObjectFolder:
        if "mask_"in img:
            objectImg=cv2.imread('CenterMask/output/'+img,0)
            ret,objectImg=cv2.threshold(objectImg,96,255,cv2.THRESH_BINARY)
            Intersect = cv2.bitwise_and(objectImg, salientMap)
            num_intersect = np.count_nonzero(Intersect)
            num_objectImg = np.count_nonzero(objectImg)
            print(f"{img} {num_intersect} {num_objectImg}")
            if num_intersect/num_objectImg<0.75:
                maskNotSalient=cv2.bitwise_or(maskNotSalient,objectImg)

    pos=args.input.find('.')
    filetype=args.input[pos+1:]

    cv2.imwrite("generative_inpainting/result/mask."+filetype,maskNotSalient)
    shutil.copy(args.input, 'generative_inpainting/result/input.' + filetype)

def Inpainting(args):
    image_name = args.input.split('/')[-1]
    path_input= "result/"+image_name[:-4]+"_input"+image_name[-4:]
    path_mask=  "result/"+image_name[:-4]+"_mask"+image_name[-4:]
    path_output="result/"+image_name[:-4]+"_output"+image_name[-4:]
    subprocess.call(["python","test1.py","--image",path_input,"--mask",path_mask,
                     "--output",path_output,"--checkpoint_dir","logs/release_places2_256"],cwd="generative_inpainting")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input",type=str,default='')
    parser.add_argument("--selection", type=int, default=1)
    args = parser.parse_args()
    # DeleteAllFileinFolder('PoolNet/data/ECSSD/Imgs1')
    # DeleteAllFileinFolder('PoolNet/results/run-1-sal-e1')
    # DeleteAllFileinFolder('CenterMask/output')
    # DeleteAllFileinFolder('generative_inpainting/result')
    if args.selection==1:
        SalientObject(args)
        ObjectSegmentation(args)
        #PhatHienVatTheKhongNoiBat(args)
        Inpainting(args)
    elif args.selection==2:
        ObjectSegmentation(args)
        Inpainting(args)

main()