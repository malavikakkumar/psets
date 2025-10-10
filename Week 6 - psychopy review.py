# PsychoPy runs base Python by default
# we still need to import in specific modules from Psychopy
from psychopy import visual, core

win = visual.Window([400, 400]) # creating a window with given name and size

message = visual.TextStim(win, text='hello', pos=(-0.1,0)) # draws a text stimulus to the back buffer
# assigns it to a window and specifies the type of stimulus
message2 = visual.TextStim(win, text='world', pos=(0.1,0))
message.autoDraw = True # automatically draws every frame

timer = core.Clock() # instance of a core.Clock()
x = 0.0
y = 0.0
startTime = timer.getTime()

while timer.getTime() - startTime < 2.0: # an alternative to core.wait which FREEZES THINGS IN PLACE, equivalent of core.wait(2.0)?
    # to make a certain action last a certain duration
    x += 0.001
    y += 0.001
    message.pos = (x,y)
    message.draw() # optional??
    win.flip()

# win.flip() # flips back buffer to front buffer so that stimulus appears on screen
# core.wait(1.0) # delays next events

# message.text = 'word' # changes the text attribute of existing stim
message.autoDraw = False
message2.autoDraw = True
win.flip() # flips back buffer to front buffer again!
core.wait(1.0)