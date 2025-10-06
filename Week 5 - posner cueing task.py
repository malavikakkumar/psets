# import the necessary libraries
from psychopy import visual, event, core, data
import random

# define a monitor
# mon = monitors.Monitor("testmonitor")

# create a window
# can be in terms of screen height, normalised units, centimeters, pixels, or degrees of visual angle
win = visual.Window([1024, 768], fullscr=False, units='pix')
# alternatively, to assign to a particular monitor
# win = visual.Window([1024, 768], fullscr=False, units='pix', monitor=mon)

respClock = core.Clock() # gets timestamp from system

# add trials to the experiment handler to store data


# create (but don't draw) a stimulus
fixation = visual.Circle(win, size=5, lineColor='white', fillColor='lightGrey')
fixation.autoDraw = True
# since we set our units to 'pix' in the previous step, size is in terms of pixel
# otherwise it's in terms of window heights

# create a second stimulus
probe = visual.GratingStim(win, size=80, pos=[300,0], tex=None, mask='gauss', color='green')
probe.autoDraw = True

# create a third stimulus
cue = visual.ShapeStim(win, vertices=[[-30,-20], [-30,20], [30,0]], lineColor='red', fillColor='salmon')
cue.autoDraw = True

info = {} # dictionary
info['fixTime'] = 0.5 # seconds
info['cueTime'] = 0.2
info['probeTime'] = 0.2

# side = [1,2]
# orient = [1,2]

# create multiple trials with responses

responses = []
rts = []

for trial in range(5):
    # in order to randomize probe and cue direction respectively
    # so that each can be pointing to either left or right
    # selecting a random negative/positive multiplier
    probe_random = random.choice([-1,1])
    cue_random = random.choice([-1,1])
    probe.pos = [x * probe_random for x in probe.pos] # I love list comprehension but I also need to keep googling it to figure it out lmao
    cue.vertices = [[i * cue_random for i in j] for j in cue.vertices]
    
    """
    
    # present dialog to collect info
    info['participant'] = ''
    dlg = gui.DlgFromDict(info) #(and from psychopy import gui at top of script)
    if not dlg.OK:
        core.quit()
    """
    
    # alternatively
    # random.shuffle(side) # reorganise list order
    # random.shuffle(orient) # reorganise list order
    
    fixation.draw()
    win.flip()
    core.wait(info['fixTime'])
    fixation.autoDraw = False # keeps the fixation on screen up until this command
    
    """
    alternatively,
    if orient[0] == 1:
        cue.ori = 0
    else:
        cue.ori = 180
    """

    cue.draw()
    win.flip()
    core.wait(info['cueTime'])
    cue.autoDraw = False
    
    """
    alternatively,
    if side[0] == 1:
        probe.pos = [300,0]
    else:
        probe.pos = [-300,0]
    """

    fixation.draw()
    probe.draw()
    win.flip() # so both fixation and probe are displayed at the same time
    core.wait(info['probeTime']) # no longer waiting
    fixation.autoDraw = False 
    probe.autoDraw = False
    respClock.reset() # reset as soon as probe appears on screen
    
    # to clear the screen
    win.flip()
    # wait for keyboard response
    keys = event.waitKeys(keyList = ['left', 'right', 'escape'])
    resp = keys[0] # take only the first response!!!!
    rt = respClock.getTime() # time passed between presentation of probe and key press
    
    # check for response accuracy
    if (probe_random == 1 and resp == 'right') or (probe_random == -1 and resp == 'left'):
        corr = 1
    else:
        corr = 0
        
    responses.append(corr)
    rts.append(rt)
    
    """
    fileName = expInfo['observer'] + expInfo['dateStr']
    dataFile = open(fileName + '.csv', 'w') # a simple text file with 'comma separated values'
    dataFile.write('targetSide, oriIncrement, correct\n')
    dataFile.write('%i, %.3f, %i\n' %(targetSide, thisIncrement, thisResp))
    dataFile.close()
    """
    
print(responses)
print(rts)
