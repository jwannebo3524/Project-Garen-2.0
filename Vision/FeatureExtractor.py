import numpy as np

#can be used for things other than vision, but built with that in mind.

def SimpleExtraction(vectors,feature_num,example_num,round_num):
    #Takes a set of data (vectors) in 1 hot encoding and attempts to compute features by caterogrizing examples and then using the groups to update the filters. Filters represnt minimum for group membership.
    #example_num : random examples used per round      round_num : number of rounds

    #for best performance use a small number instead of 0 in data. (like 0.01)

    Features = []
    Groupings = []
    
    #choose random vectors as initial values for the features:
    c = 0
    while(c<feature_num):
        z = np.random.randint(0,len(vectors))
        Features.append(vectors[z])
        Groupings.append([])
        c += 1
    
    empty = Groupings
    Features = np.array(Features)

    #for round_num rounds
    c = 0
    while(c<round_num):
        Groupings = empty #reset groupings
        c2 = 0
        while(c2<example_num): #group each example
            z = np.random.randint(0,len(vectors)) #get index for random example
            sims = np.multiply(Features,np.reshape(vectors[z],(,1))) #dot-product simularity
            Groupings[sims.index(max(sims))].append(vectors[z]) #add example to most simular group
            c2 += 1

        c2 = 0
        while(c2<feature_num): #update the features
            Groupings[c2].append(Features[c2]) #add the feature to the group (important when using small group size)

            product = np.ones((len(Features[c2]))) #vector of ones
            c3 = 0
            while(c3<len(Groupings[c2])): #product over the group (representing the simularities between elements)
                product = np.multiply(product,Groupings[c2][c3])
                c3 += 1

            Features[c2] = np.pow(product,1/len(Groupings[c2])) # nth root to avoid vanishingly small values.
            c2 += 1
        c += 1
    return Features
    



        