#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""
#%% Required set up 
# this imports everything you might need and opens a full screen window
# when you are developing your script you might want to make a smaller window 
# so that you can still see your console 
import numpy as np
import pandas as pd
import os, sys
from psychopy import visual, core, event, gui, logging
from psychopy.hardware import keyboard
from psychopy import core

event.globalKeys.add(key='q',func=core.quit)


# create a gui object
subgui = gui.Dlg()
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]


# Output preparation:

ouputFileName = 'data' + os.sep + 'sub' + subjID + '_sess' + sessNum + '_trustworthiness.csv'

if os.path.isfile(ouputFileName) :
    sys.exit("data for this session already exists")

outVars = ['subj', 'trial', 'faceL','faceR', 'response', 'rt','lr','sex']
out = pd.DataFrame(columns=outVars)


#setting up of the window

win = visual.Window(size=[3840, 2160], fullscr=True, allowGUI=False,
                    color=(0,0,0), units = 'height')

win.recordFrameIntervals = True
win.refreshThreshold = 1/60 + 0.004
logging.console.setLevel(logging.WARNING)


# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', unit='height') 

# uncomment if you use a clock. Optional because we didn't cover timing this week, 
# but you can find examples in the tutorial code 
#trialClock = core.Clock()


instructions = visual.TextStim(win, text = 'Thank you for participating in this experiment.Today, you will be deciding which of the faces presented are most trustworthy. In order to make your decision, you need to press l or r on your keyboard to indicate the left or right face is most trustworthy. When you are ready, please press the letter s to start the task.',pos = (0,0), color = 'black', height = 0.05) #note default color is white, which you can't see on a white screen!

instructions.draw()

win.flip()

keys = event.waitKeys(keyList = ('s'))

core.wait(1)

#%% your loop here
# start by copying your one trial here, then identify what needs to be
# changed on every trial.  Likely your stimuli, but you might want to change a few things

# File with experiment information:
trialInfo = pd.read_csv('faceGender.csv')
trialInfoLeft = pd.read_csv('faceGenderLeft.csv')
trialInfoRight = pd.read_csv('faceGenderRight.csv')

# I want to find a way to randomize the trials without replacement from a
# dataframe. I want to keep the onset values in original order
# onset = trialInfo.onset.values # save original onset values
trialInfo = trialInfo.sample(frac=1)
trialInfo = trialInfo.reset_index()
# trialInfo.loc[:,'onset'] = onset

# make a list or a pd.DataFrame that contains trial-specific info (stimulus, etc)
# e.g. stim = ['1.jpg','2.jpg','3.jpg']
#stimLeft = [r'rateFace\facesR\1.jpg', r'rateFace\facesR\2.jpg', r'rateFace\facesR\3.jpg', r'rateFace\facesR\4.jpg', r'rateFace\facesR\5.jpg', r'rateFace\facesR\6.jpg', r'rateFace\facesR\7.jpg', r'rateFace\facesR\8.jpg']
#stimRight = [r'rateFace\facesR\8.jpg', r'rateFace\facesR\7.jpg', r'rateFace\facesR\6.jpg', r'rateFace\facesR\5.jpg', r'rateFace\facesR\4.jpg', r'rateFace\facesR\3.jpg', r'rateFace\facesR\2.jpg', r'rateFace\facesR\1.jpg']

#stimLeft = trialInfo
#stimRight = trialInfo

# make your loop

trial = 0

nTrials = len(trialInfo)

#kb = keyboard.Keyboard()

# set stimulus and response times in seconds
stimDur = 0.15
isiDur = 1
respDur = 2
fbDur = 1

# track response from last trial
lastResp = 's'


#keys = kb.getKeys(['l', 'r'])
#for key in keys:
#    print(key.name)

#ListofKeys = getKeys(keyList=('l','r'), modifiers=False, timeStamped=False)

expClock = core.Clock() # won't reset
trialClock = core.Clock() # will reset at the beginning of each trial
stimClock = core.Clock() # will reset when stim are presented
fbClock = core.Clock() # reset for each feedback interval

while trial < (nTrials - 1):
    for t in range(nTrials) :
        
        trialClock.reset()
        expClock.reset()
        stimClock.reset()
        fbClock.reset
        
        if lastResp=='l':
            lr = -1
        elif lastResp=='r':
            lr = 1
        else:
            lr = 0
            
        trialInfo.loc[t,'lr'] = lr
            
        faceLeft = visual.ImageStim(win, image=trialInfoLeft.loc[t,'face'], pos = (-0.5,0), interpolate=True)
    
        # include your trial code in your loop but replace anything that should 
        # change on each trial with a variable that uses your iterater
        # e.g. thisStimName = stim[t]
        #      thisStim = visual.ImageStim(win, image=thisStimName ...)
    
        # if you're recording responses, be sure to store your responses in a list
        # or DataFrame which also uses your iterater!
        faceRight = visual.ImageStim(win, image=trialInfoRight.loc[t,'face'], pos = (0.5,0), interpolate=True)
    
        myText = visual.TextStim(win, text = 'Which face is most TRUSTWORTHY?',pos = (0,0.2), color = 'black', height = 0.04) #note default color is white, which you can't see on a white screen!
        responseText = visual.TextStim(win, text = 'l = Left, r = Right. If you input s, then it is incorrect.',pos = (0,-0.2), color = 'black', height = 0.03)
        # Step 2 draw stimuli
        faceLeft.draw()
        faceRight.draw()
        myText.draw()
        responseText.draw()
    
        # Step 3 flip window to show stim
        win.flip()

        # Step 4 wait for a response
        # keys = event.waitKeys(keyList = ('l', 'r','s'))
        
        # saveAsExcel(fileName, sheetName='rawData', stimOut=None, dataOut=('n', 'all_mean', 'all_std', 'all_raw'), matrixOnly=False, appendFile=True, fileCollisionMethod='rename')
        
        # check for a key response
        trialResp = None
        trialRT = None
        event.clearEvents() # clear out key presses prior to trial
        keys = event.waitKeys(keyList=['l','r','s'],timeStamped=stimClock)
        if len(keys)>0: # if response made, collect response information
            trialResp = keys[0][0] # setting trialResp will end the while loop (i.e., end the trial) 
            trialRT = keys[0][1]
        
        # show feedback
        
        #if trialResp=='l' and trialInfoLeft.loc[t,'lr']==1:
           # corFeedback.draw()
        #elif trialResp=='r' and trialInfoRight.loc[t,'lr']==-1:
         #   corFeedback.draw()
        #else:
            #incFeedback.draw()
        
        # Feedback
        
        # If the participant inputs an l or r, then they should get a prompt that says correct, other than that, incorrect
        corFeedback = visual.TextStim(win, text='correct!', pos=(0,0), height=.05, color = 'black')
        incFeedback = visual.TextStim(win, text='wrong!', pos=(0,0), height=.05, color = 'black')
        
        if trialResp=='l':
            corFeedback.draw()
            win.flip()
            core.wait(2)
        elif trialResp=='r':
            corFeedback.draw()
            win.flip()
            core.wait(2)
        else:
            incFeedback.draw()
            win.flip()
            core.wait(2)
        
        # record trial prarameters
        out.loc[t,'faceL'] = trialInfoLeft.loc[t,'face']
        
        out.loc[t,'faceR'] = trialInfoRight.loc[t,'face']
        
        if trialResp == 'l':
            out.loc[t,'sex'] = trialInfoLeft.loc[t,'sex']
        elif trialResp == 'r':
            out.loc[t,'sex'] = trialInfoRight.loc[t,'sex']
        else:
            out.loc[t,'sex'] = 'NaN'
        
        out.loc[t,'trial'] = trial + 1
        
        if trialResp == 'l':
            out.loc[t,'lr'] = trialInfoLeft.loc[t,'lr']
        elif trialResp == 'r':
            out.loc[t,'lr'] = trialInfoRight.loc[t,'lr']
        else:
            out.loc[t,'lr'] = 'NaN'
        
        #Update the trial number
        trial += 1
        
        # save responses, if made
        if trialResp != None: 
            out.loc[t, 'response'] = trialResp
            out.loc[t, 'rt'] = trialRT
    
        # store current trial response for next trial
        lastResp = trialResp
        
        print('for trial ' + str(trial) + ' the RT is ' + str(trialRT) + 'ms, the person chose the letter ' + str(trialResp) + ' where l means left face and r means right face.' + ' The gender of the face was ' + str(out.loc[t,'sex']) + ', m meaning male and f meaning female.')
        
    break

conclusion = visual.TextStim(win, text = 'Thank you for participating in this experiment! Please call the experimenter for the next steps. Please press the letter s to stop the experiment.',pos = (0,0), color = 'black', height = 0.07) #note default color is white, which you can't see on a white screen!

conclusion.draw()

win.flip()

keys = event.waitKeys(keyList = ('s'))


#%% Required clean up
# this cell will make sure that your window displays for a while and then 
# closes properly

# manage output
out['subj'] = subjID
out.to_csv(ouputFileName, index = False)

core.wait(2)
win.close()
