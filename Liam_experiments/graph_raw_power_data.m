cd ~/Desktop/Senior_Design/;
clc;
fid = readmatrix('20221102T164727.txt');

fid_new=diff(fid);

for i = 1 : length(fid_new)
    if (fid_new(i) > 10000)
        fid_new(i) = mean(fid_new);
    end
end

plot(fid_new)