import pandas as pd

def cleanMyDf(df):
    df = df.reset_index(drop=True).drop(columns=['category','prod_category','original'])
    return df

def findUp(df,measures):
    updf = df.loc[(df.Altura >= measures["altura"]) 
                  & (df.Pecho >= measures["pecho"]) 
                  & (df.Cintura >= measures["cintura"]) 
                  & (df.Cadera >= measures["cadera"])]
    updf = updf.reset_index(drop=True)
    if len(updf)==0:
        return None
    else:
        uptalla = updf.iloc[len(updf.talla)-1,0]
        return uptalla

def findDw(df,measures):
    dwdf = df.loc[(df.Altura >= measures["altura"]) 
                  & (df.Cadera >= measures["cadera"]) 
                  & (df.Long_pierna >= measures["pierna"]) ]
    dwdf = dwdf.reset_index(drop=True)
    if len(dwdf)==0:
        return None
    else:
        dwtalla = dwdf.iloc[len(dwdf.talla)-1,0]
        return dwtalla