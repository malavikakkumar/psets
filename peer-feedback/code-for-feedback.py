"""
PSYC 5P02 Peer Feedback Assignment
Malavika's comments are left in multi-line comments like this one.
"""
from psychopy import visual, event, core, data, gui
from psychopy.tools.filetools import fromFile
import random
import numpy as np

# Experiment setup
expName = 'VisualSearch'
dlg = gui.Dlg()
dlg.addField('SubjectID:')
dlg.addField('Trials Per Cond:')
ok_data = dlg.show()
if not dlg.OK:
    core.quit()

"""
It is interesting to see the Dlg() method being used differently 
from the way it was introduced to us in class! (using DlgFromDict())
The only downside (a very minor nitpick) I can see is that I personally like
having all the experiment info in one dictionary (including the experiment name)
and retrieving all info from that to construct a filename.
"""

sub_ID = ok_data[0]
trials = int(dlg.data[1])
fileName = sub_ID + "_" + expName
dataFile = open(fileName + '.csv', 'w')
dataFile.write('SetSize,TP, RT, Correct, Missed\n')
"""
I am curious to know why this code retrieves data from ok_data for the subject ID,
but the number of trials are retrieved from dlg.data! 
dlg.data is what gets returned by dlg.show(), as far as I'm aware,
and is what has been stored in ok_data.
"""

win = visual.Window([1920, 1080], fullscr=False, units='pix')

# Stimuli and conditions
conditions = [5, 8, 12]
stim_size = 30
T = visual.ImageStim(win, 'Stimuli/T.png', size=stim_size)
L = visual.ImageStim(win, 'Stimuli/L.png', size=stim_size)

# Draw stimuli at random positions/orientations
def pos_and_ori(target, distract, samp_size):
    samplelist = list(range(-180, 180, 25))
    x = random.sample(samplelist, samp_size)
    y = random.sample(samplelist, samp_size)
    """
    Taking a smaller list from a predefined range of all possible positions
    is really a clever way of ensuring that there's no repetition
    in distractor/target position! Nice!
    """
    for n in range(0, samp_size - 1):
        orientations = [0, 90, 180, 270]
        """
        could have defined this before the loop for efficiency
        """
        orin = random.choice(orientations)
        distract.ori = orin
        distract.pos = (x[n], y[n])
        distract.draw()
    for n in range(samp_size - 1, samp_size):
        target.pos = (x[n], y[n])
        target.draw()
    return distract, target
    """
    This was confusing to follow at first but after
    looking through your entire code I can see that you're
    drawing a distractor instead of a target in the target absent condition.
    This is really innovative!
    I don't really understand why you use a loop for the last step, though, because
    the loop you've defined is equivalent to running the line of code
    target.pos = (x[samp_size - 1], y[samp_size - 1])
    You might also want to use win.flip() here after drawing all the distractors and target if necessary.
    I also don't know if returning distract is necessary at all, as it only returns the last distractor drawn.
    """

# Determine if target is present on a given trial
def targ_pres(trial_list, total_trials, distract, target, condition_index):
    pres_or_not = random.choice(trial_list)
    trial_list.remove(pres_or_not)
    if pres_or_not <= np.median(total_trials):
        targ_there = 0
        stimuli = pos_and_ori(distract, distract, condition)
    else:
        targ_there = 1
        stimuli = pos_and_ori(target, distract, condition)
    return targ_there, stimuli

    """
    Here, two variables seem to be passed as arguments that are defined essentially the same below
    (trial_list and total_trials)... this could have been duplicated within the function.
    using np.median() for the untouched list of trials
    seems to be a functional way of making sure 50% of trials are target present vs. target absent.
    I do like how you call pos_and_ori with distract or target as the first argument based on whether
    we are in the target absent or target present condition.
    In an extension of my comment on the last function, is returning the stimuli variable necessary at all?
    Is it used anywhere else in the code?
    """

# Get response and RT
def KeyGet(trial_duration=2.0, rt=None, resp=None):
    startTime = core.getTime()
    while core.getTime() - startTime < trial_duration and resp is None:
        """
        instead of using this loop, the event.waitKeys() function has an attribute called maxWait
        that could have been set to trial_duration. I think that would have been more efficient :)
        But I do find this very creative, could never have thought of it myself, this essentially
        replicates the functionality of event.waitKeys() but with a loop!
        """
        keys = event.getKeys(keyList=['a', 'd', 'escape'])
        if keys:
            key = keys[0]
            rt = core.getTime() - startTime
            """
            Recording rt here does add a bit of lag to the actual rt.
            Could have done it right after the keys were recorded, or even before with waitKeys()
            and assigned rt as 999 for non-responses later on.
            """
            if key == 'a':
                resp = 'a'
                break
            elif key == 'd':
                resp = 'd'
                break
            elif key == 'escape':
                core.quit()
            """
            I like checking for escape key presses here!
            But again, I think we could have just saved key[0] as resp in a single line
            instead of using an if loop.
            keyList being defined ensures that only these keys will be recorded.
            """
        core.wait(0.01)
    if resp is None:
        resp = 'no_response'
        rt = 999
        """
        I like this default value of rt=999 to indicate no response.
        Makes it easier when the experimenter is looking at the data.
        """
    return resp, rt

# Evaluate response accuracy and feedback
def Response(resp, rt, targ_there):
    if resp == 'd' and targ_there == 1:
        corr = 1
        feedback = 'Correct!'
        response_time = round(rt, 2)
    elif resp == 'a' and targ_there == 1:
        corr = 0
        feedback = 'Incorrect!'
        response_time = round(rt, 2)
    elif resp == 'a' and targ_there == 0:
        corr = 1
        feedback = 'Correct!'
        response_time = round(rt, 2)
    elif resp == 'd' and targ_there == 0:
        corr = 0
        feedback = 'Incorrect'
        response_time = round(rt, 2)
    elif resp == 'no_response':
        corr = 0
        feedback = 'No Response'
        response_time = 'NA'
    return corr, feedback, response_time
"""
Seems straightforward and functional :)
The trial duration seems to be hardcoded for 
response_time = round(rt, 2) though.
"""

# Instructions
welcome = ''''
Welcome to the Visual Search Task

You will see an assortment of shapes in different positions and orientations.
Most will be 'L' shapes, but some may contain a 'T' shape.

If the T is present, press 'd'.
If the T is absent, press 'a'.

Respond quickly!
Press SPACE to begin 5 practice trials.
'''
"""
Really like the instructions. Clear and encouraging to the participant.
"""

instructions = visual.TextStim(win, color='white', text=welcome, units='norm', height=0.05)
instructions.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])
core.wait(0.25)
"""
I think there was no need here to assign the return value of event.waitKeys() to a separate variable,
or for a separate wait after that.
"""

# Practice trials
practice_trials = range(1, 6)
for condition in conditions:
    appear = list(practice_trials)
    for prac_trials in practice_trials:
        targ_there, stimuli = targ_pres(appear, practice_trials, L, T, condition)
        resp, rt = KeyGet()
        corr, feedback, response_time = Response(resp, rt, targ_there)
        cor_feedback = visual.TextStim(win, text=feedback, pos=(0, 30), height=40)
        back_rt = visual.TextStim(win, text=response_time, pos=(0, -30), height=40)
        cor_feedback.draw()
        back_rt.draw()
        win.flip()
        core.wait(0.5)

# Main experiment instructions
welcome = ''''
Practice complete! Now for the real trials.

Press SPACE to begin.
'''
instructions = visual.TextStim(win, color='white', text=welcome, units='pix', height=10)
"""
could just have changed the text property of the existing textStim
"""
instructions.draw()
win.flip()
keys = event.waitKeys(keyList=['space'])
core.wait(0.25)

# Trial setup
total_trials = range(1, trials + 1)
rt_list, corr_list, miss_rt_list = [], [], []
random.shuffle(conditions)

# Main experiment loop
for condition in conditions:
    appear = list(total_trials)
    for trial in total_trials:
        targ_there, stimuli = targ_pres(appear, total_trials, L, T, condition)
        resp, rt = KeyGet()
        corr, feedback, response_time = Response(resp, rt, targ_there)
        cor_feedback = visual.TextStim(win, text=feedback, pos=(0, 30), height=40)
        back_rt = visual.TextStim(win, text=response_time, pos=(0, -30), height=40)
        cor_feedback.draw()
        back_rt.draw()
        win.flip()
        core.wait(0.5)

        if rt != 999:
            rt_list.append(rt)
            miss_rt = 0
            corr_list.append(corr)
        else:
            miss_rt_list.append(1)
            miss_rt = 1
            corr_list.append(0)

        dataFile.write('%i, %i, %.3f, %i, %i\n' % (condition, targ_there, rt, corr, miss_rt))

dataFile.close()

# Final feedback
average_rt = round(np.mean(rt_list), 2)
average_corr = round(np.mean(corr_list), 2)
total_miss = sum(miss_rt_list)

avg_rt_text = f'average rt: {average_rt}'
avg_corr_text = f'average correct: {average_corr}'
miss_text = f'no response on {total_miss} trials'
leave_text = 'press SPACE to exit'
"""

"""

cor_avg_back = visual.TextStim(win, text=avg_corr_text, pos=(0, 50), height=20)
rt_avg_back = visual.TextStim(win, text=avg_rt_text, pos=(0, -10), height=20)
miss_tot_back = visual.TextStim(win, text=miss_text, pos=(0, -35), height=20)
exit_text = visual.TextStim(win, text=leave_text, pos=(0, -100), height=20)

cor_avg_back.draw()
rt_avg_back.draw()
miss_tot_back.draw()
exit_text.draw()

win.flip()
keys = event.waitKeys(keyList=['space'])
win.close()
core.quit()

"""
Overall, well done and mostly functional code.
I think that the code flows very smoothly for the latter part of this script (for the actual experiment loops
and writing to data file)
but that the supporting functions could have been defined efficiently.
"""