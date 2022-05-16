def Convolve(filters,image, stride = 1):
  #performs a convultion operation on a 2d image
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
  reutrn np.clip(data,0,999999)
    
