# -*- coding: utf-8 -*-
"""
Sep 25, 2025

Note from last class:
Match-case statements are for a fixed number of cases, 
instead of evaluations of conditions!    

LOOPS:
A FOR loop is a loop that runs for a preset number of times.
A WHILE loop is a loop that is repeated as long as an expression is true. 

"""

# for loop

for i in range(1,5): # iterates through range 1-4 (1, 2, 3, 4)
    print(i) # prints each value of i for each iteration
    
for i in range(1,10): # iterates through range 1-10 (1, 2, 3, 4, 5, 6, 7, 8, 9)
    # executes below statement for the number of iterations       
    print("AAAAAAAAAA I AM IN THE LOOP AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

print()    
print("I AM OUT OF THE LOOP WHEW")

myDrinks = ['vodka', 'gin', 'lager', 'cider']
for x in myDrinks: # iterates through each element of the list
    print (x)

# another way to iterate through lists
for y in range(len(myDrinks)):
    print(myDrinks[y])

# while loop

i = 1
while i < 6: # while given condition is true
    print(i)
    i += 1 # increments variable on left by 1

i = 0
while i <= 10: # while given condition is true
    print("AAAAAAAAAA I AM IN THE LOOP AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    i += 1 # increments i
print()    
print("I AM OUT OF THE LOOP WHEW")

"""
EXITING/CONTROLLING LOOPS IN OTHER WAYS:
    
A 'break' command exits out a loop entirely.

A 'continue' command skips the remaining commands in the loop
and moves on to the next iteration.
"""

i = 0
while i < 6:
    i += 1
    if i == 3:
        continue # skips to the next iteration of the loop
    print (i)
    
"""
VARIABLE SCOPE:
The region of the code in which a variable or resource
is visible and accessible.

Local scope: Within a certain function, the variables declared
would only exist inside that function and nothing outside it.

Global scope: Accessible throughout the program
Usually declared at the top of the script

"""

for i in range(0,5):
    x = i
    print(x)
    
print(x)


for y in myDrinks:
    if y == 'vodka':
        flag = 1
    else:
        flag = 0
    print ("Vodka: ", flag)

print ("Vodka: ", flag) 
# so I guess this isn't just a variable existing in the loop lmao

"""
using the RANDOM library
random.randint
random.getstate
random.setstate
random.seed
random.normalvariate

use the help command to learn more about each!
"""

import random

for i in range(1,5):
    print(random.randint(0, 10))

myState = random.getstate() # the current "seed" of your random number generator, so to speak
    
random.setstate(myState) # sets to old state
for i in range(1,5):
    print(random.randint(0, 10)) # able to repeat prev RNG
    
"""
FUNCTIONS and CLASSES:
* Functions are modular bits of code which can take
arguments (inputs), carry out a particular task or operation,
and can return values (outputs)
* Classes are FUNCTIONS that have data (ATTRIBUTES)
and operations (METHODS) for handling said data.
A form of object oriented programming.
Various INSTANCES can then be created for a given class.
"""

# defining a function to take a name and print + output it

def printName(name): # whenever the function is called, brings with it the argument 'name'
    print("The name is", name)
    return name # to return the passed argument; could be assigned to variable via function call

printName("Malavika") # returns output in terminal

myName = printName("Kavi") # output goes to variable instead

# defining a new function to add the same value twice

def adder(val):
    sumVal = val + val
    print(sumVal)
    
adder('hello')

print(sumVal) # this does not work! as 'added' is only defined within the function.

def adder_2(val):
    sumVal = val + val
    return sumVal

sumof5 = adder_2(5)
print(sumVal) # this would still not work
print(sumof5) # this works!

def adderFunc(val1, val2 = 5):
    """
Adds two numbers and returns the double of the sum.

    Parameters
    ----------
    val1 : TYPE
        DESCRIPTION.
    val2 : TYPE, optional
        DESCRIPTION. The default is 5.

    Returns
    -------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.

This is the description returned for help(adderFunc)
    """
    x = val1 + val2 # val2 defaults to 5 if no value has been given
    y = x + x
    return x, y

x, y = adderFunc(2)
print(x, y) # x and y are separate values
z = adderFunc(2)
print(z) # z is a tuple



# creating a sample class

class car:
    
    def __init__(self, color = 'white'): # initialise attributes of every instance of the class
        self.speed = 0 # self allows you to access variable from anywhere else in class
        self.color = color # color is defined by (optional) input 
    
    def drive(self):
        # self is who the function operates on!
        self.speed += 1
        
    def brake(self):
        self.speed -= 1
        
# creating instance(s) of the class

volkswagen = car()

toyota = car('green')

# to create a list of objects
carList = [car() for x in range(0,5)]
carList

carList[0].speed # no brackets for attributes

for i in range(0,100):
    carList[0].drive() # do not forget to put brackets for functions!!!
    print("Driving...")
    print(carList[0].speed)