clear all;
close all;

f = imread('house.tif');
f = double(f);
[M,N] = size(f);

b = error_diffusion(f);

colormap(gray(256));
image(b);
truesize
imwrite(b,'res_err_diff2.tif')

rmse = sqrt((sum(sum((f-b).^2)))/(N*M));
disp(rmse);

fid = fidelity(f,b);
disp(fid);

function b = error_diffusion(f)

    f = double(f);
    f_lin = 255 * (f/255).^2.2;
    T = 127;
    [M, N] = size(f_lin);
    b = zeros(M,N);
    
    bord = 1;

    f_pad = zeros(M+2*bord,N+2*bord);
    for i=1+bord:M+bord
        for j=1+bord:N+bord
            f_pad(i,j)=f_lin(i-bord,j-bord);
        end
    end

    for i=1+bord:M+bord
        for j=1+bord:N+bord
            if f_pad(i,j) > 127
                b(i-bord,j-bord) = 255;
            end
      
            e = f_pad(i,j) - b(i-bord,j-bord);
        
            f_pad(i+1,j-1) = f_pad(i+1,j-1) + e*3/16;
            f_pad(i+1,j) = f_pad(i+1,j) + e*5/16;
            f_pad(i,j+1) = f_pad(i,j+1) + e*7/16;
    	    f_pad(i+1,j+1) = f_pad(i+1,j+1) + e*1/16;

        end
    end
end
   
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
