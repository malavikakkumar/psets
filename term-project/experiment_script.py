# Import modules required for this script
from psychopy import visual, core, event, data, gui, monitors
import random
import pandas as pd

"""
This code will take information from the experimenter about the list to be used (out of the lists generated using the randomization script)
and import the correct list, and run all aspects of the experiment from displaying stimuli (from the imported list ONLY)
and recording behavioural data including accuracy and response time to file.
"""

# From experimenter, collect participant information
exptInfo = {'Participant Number': '', 'Age': '', 'Sex': '', 'List': 'A'} # creates a dictionary to store key experiment info
exptDlg = gui.DlgFromDict(exptInfo, title='Input Experiment Details', alwaysOnTop=True) # creates a dialog box based on the dictionary created above
if not exptDlg.OK:
    core.quit() # quits experiment if OK not clicked on dialog box
    
fileName = "NChanExpt2025" + "_Participant" + str(exptInfo['Participant Number']) + "_List" + exptInfo['List'] # creates a filename string from the user-given information
dataFile = open(fileName + '.csv', 'w') # opens .csv file with given filename in write mode
dataFile.write("Participant,Age,Sex,List,TrialNumber,Item,Type,Condition,Stimulus,Error Type,Edits,CompQuestion,CompQAcc,CompQRT\n") # writes the first row of the file in comma separated format.
    
# Import the CSV file for the specified list as dataframe
# CSV files are all counterbalanced for distribution of critical and filler sentences
listName = 'List' + exptInfo['List'] + '.csv'
stimList = pd.read_csv(listName)
# Import the main list of ALL stimuli, just in case
masterList = pd.read_csv("MasterList.csv")
masterList = pd.concat([masterList, stimList], axis=0).drop_duplicates(keep=False) # this is to remove all the entries that are also present in stimList, by first joining the two dfs together then dropping duplicates from the combined df

# Experiment starts
# Create a window
screenRes = [1920,1080]
trialWin = visual.Window(screenRes, color=[0,0,0], colorSpace='rgb255', fullscr=False, units='pix')

# Define a class Trial to handle each trial of the experiment

class Trial:
    
    # initialising the class; the information passed for each instantiation is the window and the current row of the dataframe stimList
    def __init__(self, win, stim, trialnum):
        
        self.win = win
        self.trialNum = trialnum
        """Below stores detailed information about the current stimulus
        I've put information into separate dictionaries for the condition, actual stimulus, and question for more efficient organization."""
        self.cond = {'type': stim['Type'], 'cond': stim['Condition'], 'item': stim['Item'], 'error': stim['Error Type'], 'edits_num': stim['Edits']}
        self.sent = stim['Sentence']
        self.que = {'Ques': stim['CompQ'], 'RespCorrect': stim['CompQAns']}
        """Below information is about participant response"""
        self.resp = '' # for storing participant response
        self.acc = 0 # will compare participant response to correct answer and accordingly assign an accuracy value
        self.rt = 0 # will record reaction time using clock
        
    # a function to handle the actual trial (RSVP)--called for each trial in a loop     
    def display(self):
        
        soa = 0.6 # stimulus onset asynchrony, 600 ms converted to seconds
        isi = 0.2 # inter stimulus interval, 400 ms converted to seconds
        trial_interval = soa - isi # could have just hard coded this but I wanted the durations to be defined consistently
        
        # first screen - "Blink", onscreen for 1000 ms
        display_text = visual.TextStim(self.win, text="Blink", color=[255,255,255], colorSpace='rgb255', height=100, autoDraw=False, wrapWidth=1000)
        display_text.draw()
        self.win.flip()
        core.wait(1.0) # text display duration as per expt design - 1000 ms
        self.win.flip() # to clear the screen
        core.wait(0.5) # blank screen duration
        # second screen - fixation cross, onscreen for 500 ms
        display_text.text = "+"
        display_text.draw()
        self.win.flip()
        core.wait(0.5) # fixation cross display duration as per expt design - 500 ms
        self.win.flip() # to clear the screen
        core.wait(0.5) # blank screen duration
        # a loop to display all words of current stimulus in sequence
        sentence = self.sent.split()
        for word in sentence: # splits the sentence stored in self.sent attribute at all whitespaces, to display on screen
            display_text.text = word
            display_text.draw()
            self.win.flip()
            core.wait(trial_interval)
            self.win.flip()
            if word == sentence[-1]:
                core.wait(0.7) # end of sentence off-set
            else:
                core.wait(isi)
        # last screen - comprehension question and response
        display_text.text = self.que['Ques']
        display_text.height = 50
        display_text.draw()
        YES_text = visual.TextStim(self.win, text="YES", pos=(-250, -150), color=[255,255,255], colorSpace='rgb255', height=50, autoDraw=False)
        YES_text.draw()
        NO_text = visual.TextStim(self.win, text="NO", pos=(250, -150), color=[255,255,255], colorSpace='rgb255', height=50, autoDraw=False)
        NO_text.draw()
        self.win.flip()
        respClock = core.Clock() # starts a new clock at the point of question onset
        keys = event.waitKeys(keyList=['escape', 'right', 'left'], timeStamped=respClock, clearEvents=True) # the option timeStamped returns the time at which response key is pressed along with the key values
        if 'escape' in keys[:][0]: # accesses the first element, which is the key value, of the tuple for ALL key presses
            core.quit()
        
        # record response for current trial:
        # event.waitKeys will return a list of tuples, with a tuple for the key value and timestamp for each key pressed.
        self.resp = keys[0][0] # accesses the first element, which is the key value, of the tuple for the first key press
        self.rt = keys[0][-1] # accesses the last element, which is the timestamp, of the tuple for the first key press
        # to compare participant response to correct answer and accordingly assign an accuracy value
        if ((self.que['RespCorrect'] == 'Yes') & (self.resp == 'left')) | ((self.que['RespCorrect'] == 'No') & (self.resp == 'right')): # for accuracy = correct
            self.acc = 1
        # else:
            # self.acc = 0
            # accuracy = incorrect, the default option
            
    # a function to write information about the current trial to file
    def record(self):
        # for reference, header: Participant,Age,Sex,List,TrialNumber,Item,Type,Condition,Stimulus,Error Type,Edits,CompQuestion,CompQAcc,CompQRT
        dataFile.write('%s,%s,%s,%s,%i,%s,%s,%s,%s,%s,%i,%s,%i,%f\n' 
        %(exptInfo['Participant Number'], exptInfo['Age'], exptInfo['Sex'], exptInfo['List'], self.trialNum, self.cond['item'],
        self.cond['type'], self.cond['cond'], self.sent, self.cond['error'], self.cond['edits_num'], self.que['Ques'], self.acc, self.rt))

instructions_text = "Welcome to this study!\nRead the sentence that will appear word by word on this screen.\nPay attention because you will also be asked a question about what you just read.\n\n\nPress any key to start the practice trials.\n\nPress ESC to quit now or at any point between trials."
instructions = visual.TextStim(trialWin, text=instructions_text, color=[255,255,255], colorSpace='rgb255', height=50, autoDraw=False, wrapWidth=1000)
instructions.draw()
trialWin.flip()
if 'escape' in event.waitKeys():
    core.quit()
    
# practice trials here
practice_stimuli = masterList[masterList['Type'] == "Expt"].sample(n=5) # select 5 experimental stimuli randomly from the masterlist (which excludes stimuli from the current list)
# loop for iterating through the practice_stimuli list
for inx in range(practice_stimuli.shape[0]): # practice_stimuli.shape[0] to get the number of rows of practice_stimuli
    currentTrial = Trial(trialWin, practice_stimuli.iloc[inx], inx+1)
    currentTrial.display()
    # the only difference between these and the main trials is that we do not record data from these trials

instructions.text = "You have finished the practice trials.\n The main experiment will start now.\n\n\nWhen you are ready, press any key to start.\n\nPress ESC to quit now or at any point between trials."
instructions.draw()
trialWin.flip()
if 'escape' in event.waitKeys():
    core.quit()

# main trials here - loop for iterating through the stimList
for inx in range(stimList.shape[0]): # stimList.shape[0] to get the number of rows of stimList
    currentTrial = Trial(trialWin, stimList.iloc[inx], inx+1)
    currentTrial.display()
    currentTrial.record()
    
dataFile.close()
# done with the experiment!!!!!