#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

#define NUM_PIX 5

struct window {
	unsigned int weight;
	unsigned int pixel;
};

unsigned int weighted_median_filter(unsigned int **img, int i, int j);

void error(char *name);

int main (int argc, char **argv) 
{
    FILE *fp;
    struct TIFF_img input_img, output_img;
    unsigned int **img;
    int32_t i,j;
    int num_pix_half = (NUM_PIX - 1)/2;
  
    if (argc != 2) error(argv[0]);

    /* Open image file */
    if ((fp = fopen (argv[1], "rb")) == NULL) {
        fprintf (stderr, "cannot open file %s\n", argv[1]);
        exit (1);
    }

    /* Read image */
    if (read_TIFF (fp, &input_img)) {
        fprintf (stderr, "error reading file %s\n", argv[1]);
        exit (1);
	}

    /* Close image file */
    fclose (fp);

    /* Check the type of image data */
    if (input_img.TIFF_type != 'g') {
        fprintf (stderr, "error:  image must be grayscale\n");
        exit (1);
    }

    /* Allocate image of unsigned integers for applying the weighted median filter */
    img = (unsigned int **)get_img(input_img.width + NUM_PIX - 1, input_img.height + NUM_PIX - 1, sizeof(unsigned int));

    /* Prepare the image for filtering */
    for (i=0; i<input_img.height + NUM_PIX - 1; i++) {
	    for (j=0; j<input_img.width + NUM_PIX - 1; j++) {
			  if(((i >= num_pix_half) && (i<input_img.height + num_pix_half)) && ((j >= num_pix_half) 
			  	&& (j < input_img.width + num_pix_half))) {
				  img[i][j] = input_img.mono[i-num_pix_half][j-num_pix_half];
			} else {
				img[i][j] = 0;
			}
		}
	}

    /* Set up structure for output achromatic image */
    get_TIFF (&output_img, input_img.height, input_img.width, 'g');

    /* Filter the image */
    for (i=num_pix_half; i<input_img.height+num_pix_half; i++) {
	    for (j=num_pix_half; j<input_img.width+num_pix_half; j++) {
			  output_img.mono[i-num_pix_half][j-num_pix_half] = weighted_median_filter(img, i, j);
		}
	}

    /* Open output image file */
    if ((fp = fopen ("output1.tif", "wb")) == NULL) {
        fprintf (stderr, "cannot open file output.tif\n");
        exit (1);
    }

    /* Write output image */
    if (write_TIFF (fp, &output_img)) {
        fprintf (stderr, "error writing TIFF file %s\n", argv[2]);
        exit (1);
    }

    /* Close output image file */
    fclose (fp);

    /* De-allocate space which was used for the images */
    free_img((void**)img);
	  free_TIFF(&(input_img));
	  free_TIFF( &(output_img));
	return (0);
}

unsigned int weighted_median_filter(
	unsigned int **img, 
  int i, 
	int j) {
	
	int num_pix_sq = NUM_PIX * NUM_PIX;
	int num_pix_half = (NUM_PIX - 1)/2;

	/* Set the initial weighting factors of the filter at each iteration */
	unsigned int weights[] = 
	{1, 1, 1, 1, 1,
	 1, 2, 2, 2, 1,
	 1, 2, 2, 2, 1,
	 1, 2, 2, 2, 1,
	 1, 1, 1, 1, 1};

	struct window data[num_pix_sq];
	struct window temp;  
	int32_t k, l, m, n;
    
	/* Store the weighting factors in the special data structure */
	for (k = 0; k < num_pix_sq; k++) {
		data[k].weight = weights[k];
	}
    
	/* Store the pixels contained in a 5x5 window in the special data structure */
	l = 0;
	for (m = 0; m < NUM_PIX; m++) {
		for (n = 0; n < NUM_PIX; n++) {
			data[l].pixel = img[i+m-num_pix_half][j+n-num_pix_half];
			l++;
		}
	}
    
	/* Sort the pixels in the descending order */
	for (m = 0; m < num_pix_sq; m++) {
		for (n = m+1; n < num_pix_sq; n++) {
			if (data[m].pixel < data[n].pixel) {
				temp = data[m];
				data[m] = data[n];
				data[n] = temp;
			}
		}
	}

  /* Find the weighted median */
	unsigned int sum_f = 0;
	unsigned int sum_b = 34; // sum of all weighting factors

  l = 0;
  while (sum_f < sum_b) {
		sum_f += data[l].weight;
		sum_b -= data[l].weight;
		l++;
	}
  return data[l].pixel;
}
void error(char *name)
{
    printf("usage:  %s  image.tiff \n\n",name);
    printf("this program applies a weighted median filter to a grayscale TIFF image.\n");
    printf("and writes out the result as an 8-bit image\n");
    printf("with the name 'output.tiff'.\n");
    exit(1);
}