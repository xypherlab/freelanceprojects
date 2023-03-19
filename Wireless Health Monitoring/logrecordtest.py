import pandas as pd
import numpy as np
import time
import os
val1=0
val2=0
val3=0
while True:
    val1=1+val1
    val2=2+val2
    val3=3+val3
    pathtarget="logrecord.csv"
    cnt=0
    if os.path.exists(pathtarget):
                     
         df=pd.read_csv(pathtarget,names=['HeartRate','RespiratoryRate','Temperature'],skiprows=1)
         np_df = df.as_matrix()
         df = df.append({'HeartRate':val3,'RespiratoryRate':val2,'Temperature':val1}, ignore_index=True)
         df.to_csv(pathtarget,  index = False)
         print df
    else:
         
         columns = ['HeartRate','RespiratoryRate','Temperature']
         df = pd.DataFrame(columns=columns)
         np_df = df.as_matrix()
         
         df = df.append({'HeartRate':val3,'RespiratoryRate':val2,'Temperature':val1}, ignore_index=True)
         df.to_csv(pathtarget,  index = False)
         print df

    time.sleep(2)
