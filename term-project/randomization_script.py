import random
import pandas as pd

"""
This code is designed to divide the compiled masterlist of all stimuli into 4 separate lists
while ensuring the even distribution of all stimuli. Each list will have 80 FILLER STIMULI
and 96 CRITICAL STIMULI. There is a total of 320 UNIQUE CRITICAL STIMULI and 96 UNIQUE FILLER STIMULI,
meaning that the same filler stimuli will be used for each list.
Critical stimuli will NOT repeat across/within lists once used.
"""

masterList = pd.read_csv("MasterList.csv") # importing the main list of ALL stimuli

# below code separates the imported list into critical and filler trial stimuli
criticals = masterList[masterList['Type'] == "Expt"]
fillers = masterList[masterList['Type'] == "Filler"]
conditions = criticals['Condition'].unique() # to get a list with all the unique values of Condition in the Criticals list

for letter in ['A', 'B', 'C', 'D']: # to create four separate lists A, B, C, D, this loop will run each time
    
    fileName = 'List' + letter + '.csv' # creates the filename for this corresponding list

    filler_sample = fillers.sample(n=5) # sampling the fillers to be placed at the start and end of the list
    currentList = filler_sample # starting off the dataframe holding the current list with the first five entries as fillers
    fillers = fillers.drop(filler_sample.index) # dropping those fillers that have already been sampled from the fillers
    
    # selecting 80 criticals that haven't been used in a prior list from the criticals masterlist
    currentCrits = pd.DataFrame(columns=criticals.columns)
    for condition in conditions: # this is to ensure that there are an equal number of criticals belonging to each condition in each list
        currentCrits = pd.concat([currentCrits, criticals[criticals['Condition'] == condition].sample(n=5)], axis=0)
    
    while not (fillers.empty): # since the list of fillers is the longer one, I decided to run the loop predicate on whether we've run out of fillers to be used
        
        """
        This piece of code for distributing both criticals and fillers throughout the list
        was written such that more than 3 criticals do not occur in succession, and the same goes for fillers as well.
        """
        
        if not currentCrits.empty: # checks if we're out of criticals to be used for the current list
            
            crit_num = random.randint(1,3) # selects a random number of criticals to include in this round
            if currentCrits.shape[0] >= crit_num: # if the number of criticals left for this list is greater than the number we need
                crit_sampled = currentCrits.sample(n=crit_num) # randomly samples the given number of rows from the currentCrits list
            else: # if the number of criticals left for this list is LESSER than the number we need
                crit_sampled = currentCrits # prepares to simply join on the remaining criticals to the end of the current list
            currentCrits = currentCrits.drop(crit_sampled.index) # effectively slowly empties the currentCrits list until no more criticals are left for this list
            currentList = pd.concat([currentList, crit_sampled], axis=0) # joins the currently sampled criticals to the current list
            
        fill_num = random.randint(1,3) # similar logic as above
        if fillers.shape[0] >= fill_num:
            fill_sampled = fillers.sample(n=fill_num)
        else:
            fill_sampled = fillers
        fillers = fillers.drop(fill_sampled.index)
        currentList = pd.concat([currentList, fill_sampled], axis=0)
        
    currentList.to_csv(fileName, index=False) # writing the entire list to CSV after compiling
    
    fillers = masterList[masterList['Type'] == "Filler"] # refills the fillers list
    criticals = criticals.drop(currentCrits.index) # drops the criticals used in this list from the overall criticals list
    