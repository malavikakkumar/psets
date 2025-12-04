% PSYC 5F01 - Answers to Problem Set 5

%% Problem 1

RT = [520 498 601 1200 450 475 3000 510 490]; % as given

RT_clean = RT(RT <= 1500); % picks out all the values of RT for which RT <= 1500 is TRUE

meanRT = mean(RT_clean) % calculates mean of array RT_clean and prints to command window
medianRT = median(RT_clean) % calculates median of array RT_clean and prints to command window

trials_removed = size(RT) - size(RT_clean); % this gives an array with the difference in the number of rows and columns between RT and RT_clean
fprintf('No. of trials removed: %i\n', trials_removed(2)) % print the 2nd element of trials_removed, as only the number of "columns" (total elements) changes when subtracting two horizontal arrays

%% Problem 2

rng('shuffle'); % starting by shuffling the rng

% column 1: stimulus intensity (random integers from 1-100)
intensity = randi([1 100], 10, 1); % produces a 10x1 vertical matrix with randomly generated numbers in the given range
% column 2: condition (1 = low load, 2 = high load), randomly assigned
condition = randi([1 2], 10, 1);
% column 3: response (random integers 1 or 2)
response = randi([1 2], 10, 1);

data = [intensity condition response]; % creating an array data with each vertical matrix as an element - this creates a 3x10 matrix

highLoadData = data(data(:, 2) == 2, :) % indexes all the rows of data for which the value of column 2 = 2

lowIntensityMean = mean(data(data(:, 2) == 1, 1)) % calculates the mean for column 1 (intensity) for all rows for which the value of column 2 (condition) = 1
highIntensityMean = mean(data(data(:, 2) == 2, 1)) % calculates the mean for column 1 (intensity) for all rows for which the value of column 2 (condition) = 2
% without semicolons, above commands will print to command window

%% Problem 3

criterion = 50; % as given

for i = 1:size(data, 1) % i to iterate through rows of 'data' - goes from 1 to number of rows of 'data'
    if (data(i, 1) < criterion && data(i, 3) == 1) || (data(i, 1) >= criterion && data(i, 3) == 2)
    % tests for Correct response - 1 for intensity < criterion 
    % and 2 for intensity < criterion
        fprintf('Correct\n'); % if above check succeeds, prints "Correct"
    else
        fprintf('Incorrect\n'); % if above check fails, prints "Incorrect"
    end
end

%% Problem 4
% So a change I've made here is to use 700 for the distribution mean rather than 0.7
% and also change the distribution SD accordingly
% using 0.7 mean and 400 noise just wasn't giving any outliers as intended

rng('shuffle'); % starting by shuffling the rng

mu = 700;
sigma = 200; % let's say
% using randn to generate a vertical array of 100 normally distributed elements
RTs = mu + sigma * randn(100, 1); % normal distribution with given sigma (standard deviation) and mu (mean)
% using rand to generate a vertical array of 100 uniformly distributed numbers between 0 and 1
noise = 400 * rand(100, 1); % for the upper limit of uniformly distributed noise to be 400
RTs = RTs + noise % adding calculated noise to RTs array
% also prints RTs to command window because no semicolon

help("removeOutliers")
[cleanedRTs, removedRTs, iterations] = removeOutliers(RTs)
outliersNum = size(removedRTs);
cleanedRTmean = mean(cleanedRTs);

fprintf("Mean of cleaned RT list: %f\n", cleanedRTmean)
fprintf("Number of outliers removed: %i\n", outliersNum(1))
fprintf("Number of list iterations: %i\n", iterations)

%% Question 5

load("experiment_data.mat")

fprintf("Participant ID: %s\n", data(1).participant) % indexing and printing field 'participant' of first entry (the only entry, in this case)
data(1).trials % indexing field 'trials' of first entry
% we get a struct within a struct! Pretty neat :)
data(1).mean_RT = mean([data(1).trials.rt]) % adding a new field within participant 1
% converted data(1).trials.rt to a horizontal array for ease of calculation

% not sure how to calculate accuracy when there's nothing to compare the responses to

data(2).participant = 'P011'
data(2).trials = data(1).trials % I just duplicated the same structure from the first entry in data.trials
newRTs = num2cell(mu + sigma * randn(10, 1)) % using mu and sigma values from before
[data(2).trials.rt] = deal(newRTs{:}) % replaced RTs only with deal function, given there are an equal number of old and new RTs in struct field
%%