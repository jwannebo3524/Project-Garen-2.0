import numpy as np
import keyboard as ky
from PIL import Image
import pyautogui as ag

from MOpack import MatrixOperations as MO
import LowLevel as LL
from LeagueAdvancedGamer import LAG
from LOLautoconvo import ImageAutoEncoder4layer as Auto
from LagParams import Params
from LAGinputManager import LIM
import time

file = "NathansLAG"
#the file you want the agent to save too or load from.
#the file does not need to exist if you are not trying to load previos bot-
#program will create a new file when saving if it doesn't exist

CreateNewBot = False

visionfile = "LAGVisionSystem"

#this is the primary code!!

#yay

#run it to make stuff happen!

#holding spacebar down will stop the code.


#----------------------------IGNORE--------------------------------------------
#Update!! Imitation mode added, just start code and it will learn.


# when agent in basic training mode:
#  up gives reward of 1
#  left gives reward of 0.3
#  right gives reward of -0.3
#  down gives reward of -1
#  z gives reward of 0
#  if nothing pressed, agent gets whatever reward it thinks it should get.
#  (unless you goof with the settings)
#  pressing space exits the program


#if you are looking to modify the hyperparameters, which determine the structure,
#size, and overall behavior of the agent, go to "LagParams.py"

#if you want to tweak the agent's archetecture, go to "LeagueAdvancedGamer.py"

#if you want to tweak the vison system, go to "LOLautoconvo.py"

#if you want to tweak the functioning of induvidual layers and networks, go to
#"LowLevel.py"



#-------------------------------------------------------------------------------
Par = Params()
Agent = LAG(Par.p,Par.Lp,Par.Pe,file) #initalize the agent

if(not CreateNewBot):
    Agent.Load()

 #initialize vison system
OpticSystem = Auto(Par.aD,Par.aF,Par.aS)
OpticSystem.Load(visionfile)

LIO = LIM() #initialize i/o handler

learnrate = 0.0 #The learn rate- this is per action cycle. Set to zero to freeze weights
AgentSupervised = False #if set to true, agent tries to mimics your output rather than generating its own. Good for pre-training
Imitate = False
ConstantReward = False #primarily for imitation 
CONST = 1
Negitive = -0.1

RemoveElements = True #for removing every other pixel or simular operations
period = 4

MAX = 500 # hard to explain- has to do with the agent's learning. gamma is more important
dist = 0

gamma = Par.g
MOD = 3
OpticSystemLearning = False
OpticSystemLearnRate = 0.00 # does nothing if OpticSystemLearning = False
OpticSystemBatchSize = 3

RunAgent = True    #for debugging vision system
PrintOpticError = False
print("LAG ready. Starting in 5 seconds")
time.sleep(5)
print("LAG has been initialized. Press space to stop")
c = 1
while True:
    observation = np.array(LIO.GetImageData())/255
    if(RemoveElements):
        observation = observation[1::period]
    re,null = LIO.HandleReward()
    if(ConstantReward):
        if(null):
            re = CONST
            null = False
    OpticData = OpticSystem.ConvForward(observation)
    OpticData = np.array(OpticData).flatten()
    print("shape:")
    print(np.shape(OpticData))
    if(RunAgent):
        if(AgentSupervised):
            OVER = LIO.GetUserAction(MOD)
            Agent.Update(OpticData,re,null,gamma,learnrate,MAX,dist,OVER,True,Imitate,Negitive)
            ActionVector = Agent.GetOutput()
        else:
            Agent.Update(OpticData,re,null,gamma,learnrate,MAX,dist,[],False,False,0)
            ActionVector = Agent.GetOutput()
            LIO.HandleOutput(ActionVector,MOD)

    if(OpticSystemLearning):
        err = OpticSystem.Cycle(observation)
        if(PrintOpticError):
            print(err)
        c += 1
        if(c>OpticSystemBatchSize):
            c = 1
            OpticSystem.Update(OpticSystemLearnRate)
            OpticSystem.Save(visionfile)
    if(learnrate>0):
        if(RunAgent):
            Agent.Save()
    
    
    


