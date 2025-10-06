# PsychoPy runs base Python by default
# we still need to import in specific modules from Psychopy

from psychopy import visual, core
win = visual.Window([400, 400]) # creating a window with given name and size
message = visual.TextStim(win, text='hello')  
# draws a text stimulus to the back buffer
# assigns it to a window and specifies the type of stimulus
message.autoDraw = True # automatically draws every frame
win.flip() # flips back buffer to front buffer so that stimulus appears on screen
core.wait(2.0) # delays next evenets
message.text = 'world' # changes the text attribute of existing stim
win.flip() # flips back buffer to front buffer again!
core.wait(2.0)