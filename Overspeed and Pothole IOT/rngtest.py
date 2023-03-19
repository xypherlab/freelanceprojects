import random
for x in range(100000):
  
  i=random.randint(1,101)
  print i
  print "#"+str(x)
  if i==50:
      print "Found"
      break
