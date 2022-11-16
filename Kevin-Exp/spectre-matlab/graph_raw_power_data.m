function []=graph_raw_power_data(arg1)

cd ~/Documents/sdmay23-16/Kevin-Exp/spectre-matlab/;
clc;
fid = readmatrix(arg1);

fid_new=diff(fid);

for i = 1 : length(fid_new)
    if (fid_new(i) > 10000)
        fid_new(i) = mean(fid_new);
    end
end

%yy1 = smoothdata(fid_new,'movmean',30);
%yy2 = smoothdata(fid_new,'movmedian',30);
%yy3 = smoothdata(fid_new,'gaussian',10);
yy4 = smoothdata(fid_new,'rlowess',20); % I like this one
yy5 = smoothdata(fid_new,'rlowess',250); % I like this one
%yy5 = smoothdata(fid_new,'sgolay',20);
%yy6 = smoothdata(fid_new,'rloess',20);



subplot(3,1,1)
plot(yy4);
hold on
title('Smoothed Data');

subplot(3,1,2)
plot(yy5);
hold on
title('Simple Data');

subplot(3,1,3)
plot(fid_new);
hold on
title('Raw Data');

%plot(x,yy1,'-o',x,fid_new,'-x')

%plot(x,yy1,x,yy2,x,yy3)


end