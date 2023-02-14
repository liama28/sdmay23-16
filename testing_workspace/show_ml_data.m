function []=show_ml_data(arg1)

cd ~/Desktop/Senior_Design/sdmay23-16/testing_workspace/;
clc;
f = readmatrix(arg1);
mean_val = mean(f, "all");
for i = 1 : height(f)
    for j = 1 : length(f)
        if (f(i,j) > 10000)
            f(i,j) = mean_val;
        end
    end
end
M = mean(f);

subplot(1,1,1)
plot(M);
hold on
title('Mean Data');

end