function [list, outliers_list, iters] = removeOutliers(list)
% removeOutliers  removes all outliers > +2SD and < -2SD
%
% [list, outliers_list, iters] = removeOutliers(list)
%
% given a numerical list (one-dimensional matrix),
% returns the cleaned list, the list of outliers, 
% and the number of iterations until there
% are no more outliers left to remove.
%
outliers_list = zeros(0,1); % preallocating a vertical empty matrix
iters = 0;
while ~isempty(list) % as long as the given list is not empty
    % below code finds mean and SD, upper and lower limits
    % for each iteration of this loop
    listMean = mean(list);
    listSD = std(list);
    upper = listMean + (2 * listSD);
    lower = listMean - (2 * listSD);
    % I remember doing the following in Python with list comprehension...
    % well, now I know what logical indexing is!
    cleaned_list = list(list < upper & list > lower);
    outliers_new = list(list >= upper | list <= lower);
    if isempty(outliers_new) % checks whether the list of outliers is empty for this iteration
        break; % breaks the while loop if no outliers were removed
    end
    list = cleaned_list; % assigns the cleaned list as the list for next iteration of while loop
    outliers_list = [outliers_list; outliers_new]; % adds the specific outliers removed during this iteration to the existing list
    iters = iters + 1;
end
end