"""
ANSWER TO QUESTION 5
"""
from psychopy import visual, core, event

# firstly, initialising a window and clock for the experiment
sampleWin = visual.Window(size = [800,600], color=[255,255,255], colorSpace='rgb255', fullscr=False, units='pix')
respClock = core.Clock()

fixation = visual.TextStim(sampleWin, text = '+', color=[0,0,0], colorSpace='rgb255', height=50) # fixation cross
fixation.draw() # draws TextStim fixation on sampleWin
sampleWin.flip()
core.wait(1.0) # tells the system to wait for 1 sec

prompt = visual.TextStim(sampleWin, text = 'GO!', color=[0,0,0], colorSpace='rgb255', height=100, bold=True) # creates textStim for text "GO!"
prompt.draw() # draws TextStim prompt on sampleWin
sampleWin.flip()
respClock.reset() # right after flipping, clock is reset to 0
event.waitKeys() # tells the system to wait until a key is pressed
rt = respClock.getTime() * 1000 # stops clock and records value as soon as the user responds with a keypress. This is the reaction time. 
# multiplying by 1000 to convert to milliseconds

rt_announcement = "Reaction time in ms:\n" + str(rt) # preparing to print RT to screen coherently
output = visual.TextStim(sampleWin, text = rt_announcement, color=[0,0,0], colorSpace='rgb255', height=50) # a new TextStim with RT text as defined above
output.draw() # draws TextStim output on sampleWin
sampleWin.flip()
core.wait(2.0) # tells the system to wait for 2 secs