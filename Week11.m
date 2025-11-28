%%%%% recap
a = [1 2 3 4; 5 6 7 8]
a(:, 5) = [9 10]
a(2, 6) = 1 % this automatically adds a 0 because number of rows have to stay equal
a(:, 6) = [] % to remove the indexed col

%%% loading .mat file which contains variables
load firstMatFile.mat

help("randperm")

%%% functions in MATLAB!

%{
outputArray - what's returned from the function
inputArray - what's passed to the function
subtractOne - what the function is called
%}
function outputArray = subtractOne(inputArray)
    outputArray = inputArray - 1;
end

% error handling in MATLAB!!!

%{
try
    Some commands
catch
    Some other commands
end
Look into: what's the Python equivalent to this?
%}

% text in MATLAB!!!!
double('Minecraft') % converts to ASCII values

% '' seem to be denote arrays of chars
% and "" for strings

"apples" == "applez" % returns ans (logical) = 0
'apples' == 'applez' % returns ans (logical array) = [1 1 1 1 1 0]

% structures in MATLAB are similar to dataframes!

char1 = ['apples', 'oranges'] % returns   'applesoranges'
% vs
cell1 = {'apples', 'oranges'} % returns    {'apples'}    {'oranges'}

cell2 = {[1 2 3 4 5], [5 10 15 20]}
cell2{2}(4) % returns 20

% nested variables within a singular structure - look this up later

data2.subject = 'SME';
data2.RTs = [.9 1.2];
