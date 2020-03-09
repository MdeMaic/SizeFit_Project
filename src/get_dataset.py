import pandas as pd
import numpy as np
import matplotlib as plt
import re
from bs4 import BeautifulSoup
import json
import requests
from IPython.display import Image
import os
import urllib.request
import glob
import cv2


#Request API function
def requestJSON(url):
    res = requests.get(url)
    if res.status_code != 200:
        print(res.text)
        raise ValueError("Bad Response")
    return res.json()

lst = ['lacoste','miu-miu','louis-vuitton','chanel','altuzarra','hermes']
count = 0
urls = []
names = []
paths = []

print(f"Testing vogue.com picture exctraction...")
for ind,val in enumerate(lst):
    url = f'https://www.vogue.com/fashion-shows/fall-2020-ready-to-wear/{val}/slideshow/collection/print'
    print(f"Test {ind+1}/",len(lst),"...")
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.select('.slide--image')

    for ind,image in enumerate(images):
        url_name = image['src']
        name = "OK_"+str(count).zfill(6)
        urls.append(url_name)
        names.append(name)
        count+= 1
        
        #Extract the pictures
        path_name = '../inputs/images/People_Yes_fullHD/{}.jpg'.format(name)
        paths.append(path_name)
        urllib.request.urlretrieve(url_name, path_name)

print(f"Test completed succesfully!")

#Create dataframe
df = pd.DataFrame()
df["urls"]=urls
df["names"]=names
df["paths"]=paths
df = df.set_index("names")
df = df.drop_duplicates()

## NOW THAT IT IS WORKING. Create the function.
def extractVogue(designer,collection,urls,names,paths,count=0):
      
    url = f'https://www.vogue.com/fashion-shows/{collection}/{designer}/slideshow/collection/print'

    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    images = soup.select('.slide--image')
    print(f"Extracting pictures from vogue.com designer:{designer}, collection:{collection}...")
    for image in images:
        url_name = image['src']
        name = "OK_"+str(count).zfill(6)
        urls.append(url_name)
        names.append(name)
        count+=1
        
        #Extract the pictures
        path_name = '../inputs/images/People_Yes_fullHD/{}.jpg'.format(name)
        paths.append(path_name)
        urllib.request.urlretrieve(url_name, path_name)

    #Create dataframe
    df = pd.DataFrame()
    df["names"]=names
    df["paths"]=paths
    df["urls"]=urls
    df = df.set_index("names")
    df = df.drop_duplicates()
    
    return df,urls,names,paths,count

#Adding some extra values
df,urls,names,paths,count = extractVogue("moises-nieto","madrid-spring-2020",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("jacquemus","spring-2020-menswear",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("ludovic-de-saint-sernin","spring-2020-menswear",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("abasi-rosborough","spring-2020-menswear",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("alyx","fall-2020-menswear",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("todd-snyder","spring-2019-menswear",urls,names,paths,count)
df,urls,names,paths,count = extractVogue("berluti","spring-2017-menswear",urls,names,paths,count)

#Clean df to create the GT = OK
df["GT"]="OK"

## RECOMMENDATION: Reshape using magick mogrify 640x640 save it in other folder: People_Yes_resized_640 
## magick mogrify -format jpg -resize 640x640 *.jpg
OK_list = glob.glob("../inputs/images/People_Yes_resized_640/*.jpg")
df["paths"]=OK_list


print(df.head(5))
print("Shape OK_pictures =",df.shape)

#Create the GT = KO
KO_list = glob.glob("../inputs/images/People_No/*.jpg")
dfno = pd.DataFrame()
dfno["paths"]=KO_list
dfno["urls"]= "COCO_Dataset"
dfno = dfno.reset_index()
dfno = dfno.rename(columns={"index":"order"})
dfno["names"] = dfno.order.apply(lambda x: "KO_"+str(x).zfill(6))
dfno = dfno.drop(columns=["order"])
dfno["GT"]= dfno.names.apply(lambda x: "KO")
dfno = dfno.set_index("names")

print(dfno.head(5))
print("Shape KO_pictures =",dfno.shape)

#Reorder and concatenate in one DataFrame
col_ord = ["urls","paths","GT"]
dfno = dfno[col_ord]
df = df[col_ord]
df_final = pd.concat([df,dfno])
print(df_final.head(10))
print("Shape ALL_pictures =",df_final.shape)


#To csv
df_final.to_csv("../inputs/datasets/body_recognition.csv")
print("Dataset created succesfully :)")

## RECOMMENDATION: Reshape using magick mogrify 640x640.
## magick mogrify -format jpg -resize 640x640 *.jpg