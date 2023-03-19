import urllib2
x1=14.544823 #Latitude
x2=120.991335 #Longitude
x3=0 #Speed or Pothole
x4=61 #Speed
x5=10003 #Vehicle ID
x6=0 #Status
f = urllib2.urlopen("https://api.thingspeak.com/update?api_key=7FV28MU6PT4ESS4I&field1=%s&field2=%s&field3=%s&field4=%s&field5=%s&field6=%s" % (x1,x2,x3,x4,x5,x6))  
f.close()

for i in range(3):
    print "Test"
