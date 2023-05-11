function []=Graph_data(arg1)

clc;
fid = readmatrix(arg1);

fid_new=diff(fid);
M = mean(fid_new);

for i = 1 : length(fid_new)
    if (fid_new(i) > 20000)
        fid_new(i) = M;
    end
end

%yy1 = smoothdata(fid_new,'movmean',30);
%yy2 = smoothdata(fid_new,'movmedian',30);
%yy3 = smoothdata(fid_new,'gaussian',10);
yy4 = smoothdata(fid_new,'rlowess',20); % I like this one
yy5 = smoothdata(fid_new,'rlowess',250); % I like this one
%yy5 = smoothdata(fid_new,'sgolay',20);
%yy6 = smoothdata(fid_new,'rloess',20);



subplot(2,1,1)
plot(yy4);
hold on
title('Smoothed Data');

% subplot(3,1,2)
% plot(yy5);
% hold on
% title('Simple Data');

subplot(2,1,2)
plot(fid_new);
hold on
title('Raw Data');
% 
% subplot(4,1,4)
% plot(yy4);
% hold on
% title('1');


end
