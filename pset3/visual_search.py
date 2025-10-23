# importing the modules required for this script
from psychopy import visual, core, event, data, gui
import random

"""
The below section of code is largely taken from the lecture slides, and deals with storing all the experiment info
(in this case, the participant number, observer's name, and number of trials per set size), based on input entered
by the user from a dialog box, creating a filename for output file based on this info, and opening a .csv file for experiment output.
"""
info = {'Participant': '', 'Observer': '', 'Trials per set size': ''} # creates a dictionary to store key experiment info
dlg = gui.DlgFromDict(info, title='Input Experiment Details', alwaysOnTop=True) # creates a dialog box based on the dictionary created above
if not dlg.OK:
    core.quit() # quits experiment if OK not clicked on dialog box
fileName = 'Participant' + info['Participant'] + '__' + info['Observer'] # creates a filename string from the user-given information
dataFile = open(fileName + '.csv', 'w') # opens .csv file with given filename in write mode
dataFile.write("trialNumber,target,setSize,rt,acc\n") # writes the first row of the file in comma separated format.

"""
The below section of code creates a window with the resolution of my screen, full screen set to True.
I tried using event.globalKeys.add to make it so that pressing the Esc key at any time during the experiment
would quit the experiment, but this wasn't working for some reason, so I incorporated this function into anytime
event.waitKeys() was called during a trial.
"""
trialWindow = visual.Window([1920,1080], color=[255,255,255], colorSpace='rgb255', fullscr=True, units='pix')
# event.globalKeys.add(key='escape', func=core.quit)

set_sizes = [8, 12, 14] # list of all the set sizes
trials = int(info['Trials per set size']) # assigns number of trials from info dictionary to a variable (and converts to int as a precaution against any input errors that may pop up)
"""
Ensuring that there was an equal number of target present and absent trials proved surprisingly challenging. I fiddled for a long time with this code:
conditions = random.choices(["present", "absent"], k=trials)
But turns out, having a 50% chance of selection for each option does not actually guarantee that the options will be distributed equally.
So the below code is the more foolproof solution (manually coding the permutations of target absent/present based on the number of trials), 
but I'm left wondering if there was something more straightforward that I overlooked.
"""
conditions = [] # initialising the conditions list  
"""
The logic here is to look at the number of trials per set size, and make sure that the present/absent conditions are distributed equally
for each set size. If the number of trials per set size (n) is odd, we'll make sure there's an equal distribution of n-1 trials,
and add an extra trial that is randomly picked to be target present/absent condition.
"""
for trial in range(int(trials/2)): # repeats for half the number of trials (rounded to an even n-1 in case of odd numbers)
    conditions.extend([condition for condition in ["present", "absent"]]) # present and absent repeat an equal number of times for each trial
if trials % 2 != 0:
    conditions.append(random.choice(["present", "absent"])) # addition of a randomly chosen condition for odd numbers
random.shuffle(conditions) # conditions list is shuffled to randomise order. This is repeated before every trial (as seen below)
print(conditions) # this is included as a check

"""
The next section of code creates our textStim object to provide instructions/feedback to the participant whenever needed, 
and pushes it to the window created at the beginning of this script.
I just keep updating this throughout the experiment as needed (whether for instructions or for feedback)
"""
feedback = visual.TextStim(trialWindow, text="Press the L key if target T is present on screen.\nPress the A key if target T is absent from screen.\nPress the ESC key to end the experiment at any time.\n\nPress any key to continue.", color=[0,0,0], colorSpace='rgb255', height=40)
feedback.draw()
trialWindow.flip()
# calls event.waitKeys so that the participant can advance to the trials whenever ready (as per instructions)
# if the participant presses ESC at this point, it will also quit the experiment.
if 'escape' in event.waitKeys():
    core.quit()

"""
Developing a class to handle an experiment was a fun challenge! I decided to create a class that represents a single trial, 
as the structure of that doesn't really change as long as you provide variables to take the set size and target condition into account.
This class will be called to produce a new instance of a trial for every loop of the experiment.
"""
class trial:
    
    # initialising class trial, the information passed for each instantiation is the window, the set size, and the target present/absent condition
    def __init__(self, window, set_size, condition):
        self.window = window
        self.respClock = core.Clock() # instantiates the clock which will be used to measure RT for each trial. Should I have done this outside the class? Possibly, but I wanted to make it as self-contained as possible.
        self.set_size = set_size
        self.condition = condition
        """
        The below section of code randomly calculates an x position and y position for the target, in the same way as will be calculated
        for the distractors (as seen in function Distractors ()), but the orientation will be 0 by default.
        """
        self.x_pos_t = random.randrange(-760,760,100) # 1920/2 - (100*2), with steps of 100 (50*2) so that there's no scope for overlap with target size 50
        self.y_pos_t = random.randrange(-340,340,100) # 1920/2 - (100*2), with steps of 100 (50*2) so that there's no scope for overlap with target size 50
        self.target = visual.ImageStim(self.window, image='T.png', units='pix', pos=[self.x_pos_t,self.y_pos_t], size=50) # generates a target
        self.distractors = self.Distractors(self.set_size) # created a separate function to return a list of distractors so that the __init__ function is cleaner
        """
        the below values will be recorded and written to file for each trial
        """
        self.keys = [] # for storing keypresses
        self.rt = 0
        self.accuracy = 0
        
    """
    trial.Distractors() will only ever be called within the class (during initialisation, in fact). I like to think that my logic is sound here,
    but I may have overlooked something because I keep observing that some trials simply do not match up to the intended set size. I realise that
    this is a pretty serious flaw, but I can't really see anything that I can do to fix it (within the time that I have, anyway.) 
    I'm wondering if some of the distractors simply end up outside of the screen, due to something I'm doing wrong with the positioning!
    What I'm trying to do is:
        1) create an empty list to store distractors
        2) create as many distractors as the set size demands (and remove the extra one later on if target is present)
        3) calculate a random position for each distractor similarly to above, also calculate a random orientation using random.choice()
        4) create an ImageStim object for each distractor and append to distractors list
        5) return the distractors list
    """
    def Distractors(self, set_size):
        distractors = []
        for num in range(set_size):
            x_pos_l = random.randrange(-760,760,100) # 1920/2 - (100*2), with steps of 100 (50*2) so that there's no scope for overlap with distractor size 50
            y_pos_l = random.randrange(-340,340,100) # 1920/2 - (100*2), with steps of 100 (50*2) so that there's no scope for overlap with distractor size 50
            orientation = random.choice([0,90,180,270])
            distractor = visual.ImageStim(self.window, image='L.png', units='pix', pos=[x_pos_l,y_pos_l], size=50, ori=orientation)
            distractors.append(distractor)
        return distractors
    
    """
    this function was written to handle the actual trial, from drawing the target and distractors and flipping the trial window,
    to recording the RT and accuracy, providing feedback, and returning the recorded values (but writing to file is handled during the actual experiment)
    """
    def display(self):
        if self.condition == "present": # if, for current trial, the target is supposed to be present
            self.target.draw() # draws the target generated at initialisation
            self.distractors.pop(-1) # removes a distractor from distractors list
        for distractor in self.distractors:
            distractor.draw() # draws every distractor in distractors list   
        self.window.flip()
        self.respClock.reset() # resets the clock at window flip
        self.keys = event.waitKeys(maxWait=2.0, keyList=['a','l','escape'], clearEvents=True) # event.waitKeys is called with a max wait time of 2 secs
        self.rt = self.respClock.getTime() # RT is recorded
        # checking if 1) any keys have been pressed, otherwise we go to the Incorrect response by default
        # 2) the response matches the target condition
        if self.keys and ((self.condition == 'present' and self.keys[0] == 'l') or (self.condition == 'absent' and self.keys[0] == 'a')):
            self.accuracy = 1 # accuracy set to 1 for correct response
            feedback.text = "Correct"
        elif self.keys and self.keys[0] == 'escape': # if ESC has been pressed, quits the experiment
            core.quit()
        else:
            feedback.text = "Incorrect" # accuracy set to 0 by default for incorrect response
        feedback.draw() # updates and draws the textStim, whatever its value has been set to
        self.window.flip()
        core.wait(1.0)
        return self.rt, self.accuracy

# creating a variable to store the current trial number
# and dicts to store average accuracy and RT by set size
trialNum = 0
avgAccuracy = {}
avgRT = {}

for set_size in set_sizes: # goes through each set size in the pre-defined set size list
    accuTotal = 0 # stores sum of trial accuracy for calculating the average
    rtTotal = 0 # stores sum of RT accuracy for calculating the average
    random.shuffle(conditions) # shuffles target condition list, just to keep it unpredictable :)
    for condition in conditions: # goes through each condition in the pre-defined condition list
        currentTrial = trial(trialWindow, set_size, condition) # creates a new trial object for the current loop
        rt, acc = currentTrial.display() # runs the trial
        accuTotal += acc
        rtTotal += rt
        trialNum += 1
        # writes attributes of current trial to file
        dataFile.write('%i,%s,%i,%f,%f\n' %(trialNum, condition, set_size, rt, acc))
    # at the end of each set_size, calculates and stores average accuracy (in % form) and RT
    avgAccuracy[set_size] = (accuTotal/trials) * 100
    avgRT[set_size] = rtTotal/trials

dataFile.close()

"""
This last bit of code simply formats the information from dicts avgAccuracy and avgRT and compiles them into a single string,
then updates textStim feedback to display the information on successive screens for each set size.
"""
for set_size in set_sizes:
    end_feedback_acc = "Average accuracy: " + str(avgAccuracy[set_size]) + "%"
    end_feedback_rt = "Average RT: " + str(avgRT[set_size])
    end_feedback = "For set size " + str(set_size) + "\n" + end_feedback_acc + "\n" + end_feedback_rt + "\n\nPress any key to continue"
    feedback.text = end_feedback
    feedback.draw()
    trialWindow.flip()
    event.waitKeys() # participant can progress to next screen whenever ready