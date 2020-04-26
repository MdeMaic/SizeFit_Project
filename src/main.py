#Import required packages
import cv2
import numpy as np
import pandas as pd
import argparse
from checkPicture import resizeImg, obtainMeasures
from scipy.spatial import distance as dist
from findSize import *
from pymongo import MongoClient

# Connect to the database
client = MongoClient("mongodb://localhost/fitsize")

# Asignar variables a las colecciones para evitar que se reinicien en cada función.
db = client.get_database()
coll_measures = db["user_measures"]

#Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-a", "--altura", required=True, help="altura en centimetros")
args = vars(ap.parse_args())

#Load the image, save it and do the same with the height
image = args["image"]
altura = args["altura"]

#Welcome pack
print("\n------------------------------------------------------------")
print("WELCOME! :)")
print("Let's find together the best size for your kid in five steps!")
print("------------------------------------------------------------\n")

print("STEP 1: Choose your product")
print("---------------------------")
product = input("Choose here - camisa, abrigo, pantalon o falda: ")
print(f"You choosed {product}")

lst_product = ["camisa","abrigo","pantalon","falda"]

while product not in lst_product:
    print("Sorry, not in the options right now… plese choose again")
    product = input("camisa, abrigo, pantalon o falda: ")
    print(f"You choosed {product}")


print("\nSTEP 2: Validating your picture")
print("---------------------------")

#Define global variables
start = False
refpt = []
inicio = 0 
fin = 0
measures = {}

#Colours RGB
azul = (42, 90, 118)
verde = (44, 84, 62)
rojo = (128, 51, 34)

def RGBtoBGR(col):
    '''
    Transform BGR colour to RGB
    '''
    return (col[2],col[1],col[0])

def on_mouse(event, x, y, flags, param):
    '''
    Generate the call for the mouse operation and save the x,y points for posterior distance calculations
    '''
    global start,refpt,inicio,fin

    if len(refpt) < 4:
        if event == cv2.EVENT_LBUTTONDOWN:
            start = True
            inicio = (x,y)
        elif event == cv2.EVENT_LBUTTONUP:
            start = False
            fin = (x,y)
            refpt.append((inicio,fin))
            if len(refpt)==1: print("PECHO          --> OK")
            if len(refpt)==2: print("CINTURA        --> OK")
            if len(refpt)==3: print("CADERA         --> OK")
            if len(refpt)==4: print("LONG. PIERNA   --> OK")

    if len(refpt) >= 4:
        cv2.putText(param,"Values setted. Press 's' to save",(15,50),cv2.FONT_HERSHEY_SIMPLEX,0.5,RGBtoBGR(azul), 2)

if __name__ == "__main__":

    title = 'Draw the measures'

    #Validate the image loaded using clasification machine learning model
    image,pix = obtainMeasures(image,altura)
    
    #If the validation is OK
    if type(image) != bool:
        clone = image.copy()
        cv2.namedWindow(title)
        
        while(1):
            cv2.setMouseCallback(title, on_mouse, image)
            cv2.imshow(title, image)
            cv2.putText(image,"Draw the measures. Press 'r' to restart",(15,30),cv2.FONT_HERSHEY_SIMPLEX,0.5,RGBtoBGR(azul), 2)
            
            for i in range(len(refpt)):
                if len(refpt) <= 4:
                    if len(refpt) < 4:
                        d = dist.euclidean(refpt[i][0], refpt[i][1])
                        reald = (d/pix)*2*1.3
                        cv2.line(image, refpt[i][0], refpt[i][1], RGBtoBGR(azul), 2)
                        cv2.putText(image,"{:.1f} cm".format(reald),(refpt[i][1][0]+5,refpt[i][1][1]+5),cv2.FONT_HERSHEY_DUPLEX,0.6,RGBtoBGR(azul), 2)

                    if len(refpt) == 4:
                        dp = dist.euclidean(refpt[3][0], refpt[3][1])
                        realdp = (dp/pix)*1.1
                        cv2.line(image, refpt[3][0], refpt[3][1], RGBtoBGR(azul), 2)
                        cv2.putText(image,"{:.1f} cm".format(realdp),(refpt[3][1][0]+5,refpt[3][1][1]+5),cv2.FONT_HERSHEY_DUPLEX,0.6,RGBtoBGR(azul), 2)
                else:
                    break

            key = cv2.waitKey(20) & 0xFF
            if key == ord('q'):
                print("------")
                break
            elif key == ord('s'):
                if len(refpt) == 4:
                    dpecho = (dist.euclidean(refpt[0][0], refpt[0][1])/pix)*2*1.3
                    dcint = (dist.euclidean(refpt[1][0], refpt[1][1])/pix)*2*1.3
                    dcadera = (dist.euclidean(refpt[2][0], refpt[2][1])/pix)*2*1.3 
                    dpierna = (dist.euclidean(refpt[3][0], refpt[3][1])/pix)*1.1
                    measures = {"altura":float(altura),
                                "pecho":dpecho.round(2),
                                "cintura":dcint.round(2),
                                "cadera":dcadera.round(2),
                                "pierna":dpierna.round(2)
                                }
                    print("------")
                    print("SAVED")
                    #print(measures)
                    cv2.putText(image,"Values SAVED",(15,90),cv2.FONT_HERSHEY_SIMPLEX,0.5,RGBtoBGR(verde), 2)

                    df = pd.read_csv("../outputs/ropa_clean.csv",index_col=0)
                    df = cleanMyDf(df)

                    if len (measures) >= 1:
                        uptalla = findUp(df,measures)

                        dwtalla = findDw(df,measures)
                        
                        print("\nSTEP 4: Your recommendation")
                        print("---------------------------")
                        if product == 'camisa' or product == 'abrigo':

                            print(f"If you are looking for a {product}")
                            print(f"Your kid size recommendation is {uptalla}\n")

                        elif product == 'pantalon' or product == 'falda':

                            print(f"If you are looking for {product}")
                            print(f"Your kid size recommendation is {dwtalla}\n")
                        

                        print("THANKS FOR USING THIS SERVICE!")
                        print("We hope it helped…\n\n")

                        cv2.waitKey(10000)
                        print("FEW TIMES LATER.... AFTER THE DELIVERY")
                        print("\nSTEP 5: Are you happy?")
                        print("---------------------------")
                        print("Satisfaction: 'return' if the user returned the product. 'happy' if not...")
                        size_satisf = input ("return or happy: ")
                        satisf_lst = ["return","happy"]

                        while size_satisf not in satisf_lst:
                            print("Try again please")
                            size_satisf = input ("return or happy: ")

                        new_query = {"measures":measures,
                                    "product":product,
                                    "size_choosed_up":uptalla,
                                    "size_choosed_dw":dwtalla,
                                    "satisfact":size_satisf
                                    }
                        

                        query = coll_measures.insert_one(new_query)

                        print("\n\nThank you! Press 'q' in the picture to exit :)")                 
                
                else:
                    cv2.putText(image,"Not saved. Need 4 values",(15,70),cv2.FONT_HERSHEY_SIMPLEX,0.5,RGBtoBGR(rojo), 2)
            
            elif key == ord('r'):
                print("------")
                print("RESET")
                print("Getting Measures")
                image = clone.copy()
                refpt = []
        
        cv2.destroyAllWindows()

        