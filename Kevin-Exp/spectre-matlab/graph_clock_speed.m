
cd ~/Documents/sdmay23-16/Kevin-Exp/spectre-matlab/;
clc;
fid = readmatrix("20221115-120804/clock_speed_20221115-120804.txt");

yy4 = smoothdata(fid,'rlowess',5);

subplot(4,1,4)
plot(yy4);
hold on
title('Clock Speed');

%plot(x,yy1,'-o',x,fid_new,'-x')

%plot(x,yy1,x,yy2,x,yy3)
