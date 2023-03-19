import cv2
import numpy as np
import pymeanshift as pms
while True:
    original_image = cv2.imread("imageB.png")
    partL=original_image[60:405,80:270]
    partR=original_image[120:425,320:530]
    
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    ######Left Side
    original_image = cv2.filter2D(partR, -1, kernel) 
    #Waste Detection BGR
    (segmented_image, labels_image, number_regions) = pms.segment(original_image, spatial_radius=3, 
                                                          range_radius=3, min_density=25)
    
    
    
    lowerrange = np.array([10,10,10]) #Color
    upperrange = np.array([50,50,50])
    mask = cv2.inRange(segmented_image, lowerrange, upperrange)
    
    mask = cv2.bitwise_not(mask)
    mask = cv2.convertScaleAbs(mask)
    segmented_image = cv2.bitwise_and(segmented_image,segmented_image,mask = mask)
    
    grayimg=cv2.cvtColor(segmented_image,cv2.COLOR_BGR2GRAY)
    
    bimg=cv2.threshold(grayimg, 105, 255, cv2.THRESH_BINARY)[1]
    bimg = cv2.bitwise_not(bimg)
    output =  cv2.connectedComponentsWithStats(bimg)
    num_labels = output[0]-1
    labels = output[1]
    stats = output[2]
    centroids = output[3]	    
    sizes = stats[1:, -1]
    #Size
     
    mask = np.zeros((labels.shape))
    z=0
    min_size = 1000
    max_size = 100000
    totalareadog=0
    for i in range(0, num_labels):
               if sizes[i] >= min_size and sizes[i] <= max_size:
                    mask[labels == i + 1] = 255

                    totalareadog=totalareadog+sizes[i]
                    z=z+1
    print "Area Left Dog: "+str(totalareadog)
    bimg = cv2.convertScaleAbs(mask)
    cv2.imshow('Binary',bimg)
    z=0
    min_size = 1000
    max_size = 5000 
    totalarea=0
    for i in range(0, num_labels):
               if sizes[i] >= min_size and sizes[i] <= max_size:
                    mask[labels == i + 1] = 255

                    totalarea=totalarea+sizes[i]
                    z=z+1
    print "Area Left: "+str(totalarea)
    if totalareadog>5000:
        print "Dog Detected"
    totalarealeft=totalarea
    bimg = cv2.convertScaleAbs(mask)
    cv2.imshow('Original',original_image)
    cv2.imshow('Left',partL)
    cv2.imshow('Right',partR)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
