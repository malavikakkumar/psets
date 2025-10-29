# PSYC 5P02- Introduction to Programming for Psychology
## Fall 2025

### Problem Set #3

### Rubric:
* Accuracy & Efficiency: 50%
* Explanation and documentation: 50%

--- 
###  Feedback:
* I like your solution to having an equal number of odd and even trials. I usually do something similar to this
* Great use of the class! Glad to see this implemented. 
* You hard-coded the range of possible x and y locations for the stimuli, but this may not be the best idea given that it's tied to your monitor size. Instead, you could create global variables for our hight and width of your monitor (that way if your monitor changes, the coordinates will change with it). Or since you're tying it to the monitor you could just present everything in _normalized_ units since it's already a % of the monitor height. You also use these values multiple times in the code so again - try to avoid hard-coding
* A small point but you're calculating RT after the key response in a separate line of code, so it's not really the **true** RT value. waitKeys can return the clock time at the same time it's called. 
* **Overall:** Great work. Very efficient and great use of a class. Some small places where you could improve but I think you captured the assignment perfect.

**Accuracy & Efficiency:** 23/25
**Explanation and documentation:** 25/25
**Bonus:** + 1
**Total:** 49/50
