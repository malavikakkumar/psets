from psychopy import visual, core, event

win = visual.Window([400, 400])
message = visual.TextStim(win, text='click to end')

mouse = event.Mouse(visible=True)

timer = core.Clock() # instance of a core.Clock()
startTime = timer.getTime()

while not any(mouse.getPressed()): # trying to make this end when the mouse is clicked!
    
    mousePos = mouse.getPos()
    message.pos = (mousePos[0], mousePos[1])
    message.draw()
    win.flip()