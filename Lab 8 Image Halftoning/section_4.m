clear all;
clc;
close all;

f = imread('house.tif');
f = double(f);

fl = 255 * (f/255).^2.2;

[M, N] = size(fl);

% Bayer threshold matrices
IN = [1, 2; 3, 0];
I2N = [4*IN + 1, 4*IN + 2; 4*IN + 3, 4*IN];
I4N = [4*I2N + 1, 4*I2N + 2; 4*I2N + 3, 4*I2N];

[M1 N1] = size(IN);
[M2 N2] = size(I2N);
[M4 N4] = size(I4N);

T = (255 * (IN + 0.5)) / (M1 * N1);
T2 = (255 * (I2N + 0.5))/(M2 * N2);
T4 = (255 * (I4N + 0.5))/(M4 * N4);


b = zeros(M,N);
b2 = zeros(M,N);
b4 = zeros(M,N);

for i=1:M
    for j=1:N
        if fl(i,j) > T(mod(i-1, M1)+1, mod(j-1, N1)+1)
            b(i,j) = 255;
        else
            b(i,j) = 0;
        end
    end
end

for i=1:M
    for j=1:N
        if fl(i,j) > T2(mod(i-1, M2)+1, mod(j-1, N2)+1)
            b2(i,j) = 255;
        else
            b2(i,j) = 0;
        end
    end
end

for i=1:M
    for j=1:N
        if fl(i,j) > T4(mod(i-1, M4)+1, mod(j-1, N4)+1)
            b4(i,j) = 255;
        else
            b4(i,j) = 0;
        end
    end
end



rmse = sqrt((sum(sum((f-b).^2)))/(N*M));
rmse2 = sqrt((sum(sum((f-b2).^2)))/(N*M));
rmse4 = sqrt((sum(sum((f-b4).^2)))/(N*M));

disp(rmse);
disp(rmse2);
disp(rmse4);

fid = fidelity(f,b);
fid2 = fidelity(f,b2);
fid4 = fidelity(f,b4);

disp(fid);
disp(fid2);
disp(fid4);

imwrite(b, 'halftone_2.tif');
imwrite(b2, 'halftone_4.tif');
imwrite(b4, 'halftone_8.tif');

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
