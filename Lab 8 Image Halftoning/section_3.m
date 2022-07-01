clear all;
clc;
close all;

% Section 3 %
f = imread('house.tif');
f = double(f);

[M, N] = size(f);

b = zeros(M,N); % binary image

T = 127; % threshold

for i=1:M
    for j=1:N
        if f(i,j) > T
            b(i,j) = 255;
        else
            b(i,j) = 0;
        end
    end
end

b = double(b);

rmse = sqrt((sum(sum((f-b).^2)))/(N*M));
disp(rmse);

fid = fidelity(f,b);
disp(fid);

function fid = fidelity(f,b)
    % Un-gammacorrect f and b
    f = double(f);
    b = double(b);
    
    f = 255*(f/255).^2.2;
    
    [M, N] = size(f);
    
    % Low-pass filtering
    % Initialize the filter
    sigma = 2; % variance
    num_ind = 7; % number of pixels used in the filter
    ind = -floor(num_ind/2):floor(num_ind/2);
    [X Y] = meshgrid(ind, ind);
    h = exp(-(X.^2+Y.^2)/(2*sigma));
    h = h / sum(h(:));
    
    % Convolution
    f_conv = conv2(f, h, 'same');
    b_conv = conv2(b, h, 'same');
    
    % Improve the visual perception
    f_imp = 255*(f_conv/255).^(1/3);
    b_imp = 255*(b_conv/255).^(1/3);
    
    fid = sqrt((sum(sum((f_imp - b_imp).^2)))/(N * M));
end
