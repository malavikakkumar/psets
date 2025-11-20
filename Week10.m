% this is a comment
% WELCOME TO THE BASICS OF MATLAB!!!

%{
MATLAB treats everything as an array!
(as opposed to Python which treats everything as an object.)
%}

% run a command without assigning to a variable
% MATLAB creates a variable ans to store the answer
5 + 5;
% "clear ans" will delete that variable alone from the workspace

%%

% This is a new section

% creating a new array
a = [1, 2, 3, 4, 5]; % semicolon hides output
% commas separate rows, semicolons separate columns
b = [1, 2, 3; 4, 5, 6] % 2x3 matrix 
c = [1 2 ; 3 4 ; 5 6] % 3x2 matrix
who

%%

% Matrices must always be rectangular
% To compensate for missing values, use NaN (not a number value - not text either!)
% indicates the absence of a number, 
% without being processed as a number or an error lmao

%%

% accessing specific values
a(3)
b(4)
b(2, 2) % equivalent to b(4)

cols = [1 3]
b(1, cols) % access first element of specific col numbers

b(2, [2 3])
b(2, 2:end) % equivalent to above

%%

% generating array
arr = 1:2:10 % start:step:end

% transpose array
arr'

% concatenation - resulting matrix must be square!!
d = [b c']
e = [b'; c]

% add a new row to b
b(3, :) = [7 8 9]

%%

% pre-allocating matrices
x = zeros(3,2)
y = ones(2,3)
z = NaN(3,4)
% can update values later; more memory-efficient

%%

save('firstMatFile');
clear;

%%

% MATH TIME IN MATLAB

mean(b) % column wise mean
mean(b') % row wise mean

%%