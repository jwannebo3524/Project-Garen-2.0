import numpy as np
def Convolve(filters,image, stride = 1):
  #performs a convultion operation on a 2d (NOT RGB) image. resulting shape is (x/stride-filtx,y/stride-filty,# of filters)
  #TODO: add 3d convolution for more layers and RGB. Idk why i built it for 2d images because thats kinda useless.
  out = []
  filtX = len(filters[0])
  filtY=len(filters[0][0])
  c = 0
  while(c+filtX<len(image)): #scan over x axis
    c2 = 0
    out.append([]) #add blank column to output
    while(c2+filtY<len(image[0])): #scan over y axis
      patch = np.flatten(image[c:c+filtX,c2:c2+filtY]) #convert 2d segment to 1d
      out[c].append(np.multiply(filters,np.reshape(patch, (,1)))) #apply the filters and add result to output
      c2 += stride #move over y
    c += stride #move over x
  return out

def Sigmoid(data):
  #just the sigmoid function
  return 1/(np.nan_to_num(np.exp(-data))+1)

def ReLu(data):
  #just ReLu
  return np.clip(data,0,999999)
    
def Deconvolve(filters,data, stride=1):
  #performs a deconvultion for a 2d image. resulting shape is (x*stride+filtx,y*stride+filty)
  #this doesn't really work this isn't how image generation normally works. Also should be 3d not 2d see above.
  filtX = len(filters[0])
  filtY=len(filters[0][0])
  out = np.zeros(filtX*len(data),filtY*len(data))
  norm = np.zeros(filtX*len(data),filtY*len(data))
  c = 0
  while(c<len(data)): #for each colomun of feature values
    c2 = 0
    while(c2<len(data[0])): #for each feature value
      patch = np.multiply(data,np.reshape(filters,(,1))) #get the approximate image patch
      out[c*stride:(c*stride)+filtX,c2*stride:(c2*stride)+filtY] = patch #put it in the right spot
      norm[c*stride:(c*stride)+filtX,c2*stride:(c2*stride)+filtY] += 1 #add one to the norm value
      c2 += 1
    c += 1
  #go back and try to normalize the values
  c = 0
  while(c<len(out)): #for each pixel column
    c2 = 0
    while(c2<len(out[0])): #for each pixel
      if(norm[c,c2] >0):  #just in case it tries to divide by 0
        out[c,c2] = out[c,c2]/norm[c,c2] #normalize the pixel
      c2 += 1
    c += 1
    
  return out
