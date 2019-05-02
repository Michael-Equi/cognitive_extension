import cv2 #Note: comment out sourceing ROS in bashrc if problems occur with the import
import numpy as np
import pandas as pd
import sys

def seriesToImage(series):
    image = np.zeros((200, 10))
if(len(sys.argv) > 1):
    file = sys.argv[1]
    print("File to display = " + file)
else:
    file = input("File to display: ")

df = pd.read_csv(file, delimiter = ',')

i = 0
for series in df['time series']:
#    print(series)
    #np.fromstring(series)
    print(df['label'].shape)
    # image = seriesToImage(series)
    # imshow(str(label[i]), image)
    # cv2.waitkey(0)
    i+=1
