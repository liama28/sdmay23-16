function []=graph_raw_power_data(arg1)

cd ~/Desktop/Senior_Design/sdmay23-16/Liam_experiments/;
clc;
fid = readmatrix(arg1);

fid_new=diff(fid);

for i = 1 : length(fid_new)
    if (fid_new(i) > 10000)
        fid_new(i) = mean(fid_new);
    end
end

yy1 = smoothdata(fid_new,'movmean',30);
yy2 = smoothdata(fid_new,'movmedian',30);
yy3 = smoothdata(fid_new,'gaussian',10);
yy4 = smoothdata(fid_new,'rlowess',20); % I like this one
yy5 = smoothdata(fid_new,'sgolay',20);
%yy6 = smoothdata(fid_new,'rloess',20);

subplot(6,1,1)
plot(yy1);
hold on
title('1');

subplot(6,1,2)
plot(yy2);
hold on
title('2');

subplot(6,1,3)
plot(yy3);
hold on
title('3');

subplot(6,1,4)
plot(yy4);
hold on
title('4');

subplot(6,1,5)
plot(yy5);
hold on
title('5');

subplot(6,1,6)
plot(fid_new);
hold on
title('6');

%plot(x,yy1,'-o',x,fid_new,'-x')

%plot(x,yy1,x,yy2,x,yy3)


end