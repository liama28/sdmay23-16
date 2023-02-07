clc;clear all;
cd 'C:\Users\gohsh\OneDrive\W\Documents\ISU\Spring2023\SeniorDesign\Data'; % Path of the Data
spectre_data=readmatrix('mov15_2.txt');

%% Energy
samples=5001;
measurement=15;
N=samples*measurement;
k=1;
for j=1:samples:N       
    E_attack(:,k)=spectre_data(j:j+samples-1,1);
    k=k+1;
end

  
%% Energy difference
for i=1:measurement
    for j=2:samples
        delE_attack(j-1,i)=E_attack(j,i)-E_attack(j-1,i);
    end
end

X_attack=delE_attack';
%% Benign Applications
% b1=readmatrix('aobench.txt');
% b2=readmatrix('amg.txt');
% b3=readmatrix('git.txt');
% b4=readmatrix('video.txt');
% b5=readmatrix('website_browsing.txt');
%% Energy
% clear E;
% num_class=5;
% measurement=20;
% N=samples*measurement;
% k=1;
% for i=1:num_class
%     %E = eval(strcat('b',num2str(i)));
%     k=1;
%     for j=1:samples:N       
%         %E_benign(:,k,i)=E(j:j+samples-1,1);
%         k=k+1;
%      end
% end
% %% Energy difference
% for m=1:num_class
%     for i=1:measurement
%         for j=2:samples
%             %delE_benign(j-1,i,m)=E_benign(j,i,m)-E_benign(j-1,i,m);
%         end
%     end
% end
% %% X merge
% k=1;
% for i=1:num_class
%     for j=1:measurement
%         X_benign(k,:)=delE_benign(:,j,i);
%         k=k+1;
%     end
% end
% 
% X=[X_attack;X_benign];

%%
y1=zeros(1,size(X_attack,1));
% y2=ones(1,size(X_benign,1));
% Y=[y1 y2];

%% X and Y save
% dlmwrite('D:\CPR Research\Senior_Design_Project\Anomaly_Detector\FinalData\X.csv',X);
% dlmwrite('D:\CPR Research\Senior_Design_Project\Anomaly_Detector\FinalData\Y.csv',Y);

%% Train data
% N = size(X,1)*0.7;
% num_measure=100;
% num_category=2;
% interval=N/num_category;
% k=1;
% m=0;
% for i=1:interval:N
%     x_train(i:i+interval-1,:)=X(k:k+interval-1,:);
%     y_train(i:i+interval-1,1)=Y(:,k:k+interval-1);
%     k=k+num_measure;
%     m=m+1;
% end
% %% validation data
% N = size(X,1)*0.15;
% num_measure=100;
% k=interval+1;
% interval=N/num_category;
% m=0;
% for i=1:interval:N
%     x_val(i:i+interval-1,:)=X(k:k+interval-1,:);
%     y_val(i:i+interval-1,1)=Y(:,k:k+interval-1);
%     k=k+num_measure;
%     m=m+1;
% end 
%% Test data
% N = size(X_attack,1)*0.15;
% num_measure=100;
% k=(num_measure-interval)+1;
% interval=N/num_category;
% m=0;
% for i=1:interval:N
%     x_test(i:i+interval-1,:)=X(k:k+interval-1,:);
%     y_test(i:i+interval-1,1)=Y(:,k:k+interval-1);
%     k=k+num_measure;
%     m=m+1;
% end 
%%
% dlmwrite('C:\Users\gohsh\OneDrive\W\Documents\ISU\Spring2023\SeniorDesign\Final\X_train_100.csv',x_train);
% dlmwrite('C:\Users\gohsh\OneDrive\W\Documents\ISU\Spring2023\SeniorDesign\Final\Y_train_100.csv',y_train);
% dlmwrite('D:\CPR Research\Senior_Design_Project\Anomaly_Detector\FinalData\X_val_100.csv',x_val);
% dlmwrite('D:\CPR Research\Senior_Design_Project\Anomaly_Detector\FinalData\Y_val_100.csv',y_val);
dlmwrite('C:\Users\gohsh\OneDrive\W\Documents\ISU\Spring2023\SeniorDesign\Final\X_attack_test_15.csv',X_attack);
dlmwrite('C:\Users\gohsh\OneDrive\W\Documents\ISU\Spring2023\SeniorDesign\Final\Y_attack_test_15.csv',y1');

