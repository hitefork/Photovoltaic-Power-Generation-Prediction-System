clear all
close all
clc

data=readcell('data_new.xlsx','Sheet','PSx-u');
id=1704:1749;
G=cell2mat(data(id,[2]));
T=cell2mat(data(id,[3]));
V=cell2mat(data(id,[4]));
I=cell2mat(data(id,[5]));
num=size(V,1);
num_sample=num-19;
result=zeros(num_sample*20,4);
for i=1:num_sample
    result((i-1)*20+1:i*20,1:4)=[G(i:i+19),T(i:i+19),V(i:i+19),I(i:i+19)];
    %result((i-1)*20+1:i*20,5)=4;
end