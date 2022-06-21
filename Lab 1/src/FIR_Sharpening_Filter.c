#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

#define FILTER_WIDTH 5
#define FILTER_HEIGHT 5

void error(char * name);
double limit_image(double pixel);

int main(int argc, char ** argv) {
  FILE * fp;
  struct TIFF_img input_img, color_img;
  double ** img_temp;
  int i, j, k, l;
  uint8_t channel;
  double sum;
  double h = 1.0 / (FILTER_WIDTH * FILTER_HEIGHT);
  double lambda = 1.5;
  double delta;
  double sharpening_filter[FILTER_WIDTH][FILTER_HEIGHT];
  int half_filter_width = (FILTER_WIDTH - 1) / 2;
  int half_filter_height = (FILTER_HEIGHT - 1) / 2;

  if (argc != 2) error(argv[0]);
  /* open image file */
  if ((fp = fopen(argv[1], "rb")) == NULL) {
    fprintf(stderr, "cannot open file %s\n", argv[1]);
    exit(1);
  }

  /* read image */
  if (read_TIFF(fp, & input_img)) {
    fprintf(stderr, "error reading file %s\n", argv[1]);
    exit(1);
  }

  /* close image file */
  fclose(fp);

  /* check the type of image data */
  if (input_img.TIFF_type != 'c') {
    fprintf(stderr, "error: image must be 24-bit color\n");
    exit(1);
  }

  get_TIFF( & color_img, input_img.height, input_img.width, 'c');

  /* Fill in the sharpening filter */
  for (i = 0; i < FILTER_WIDTH; i++) {
    for (j = 0; j < FILTER_HEIGHT; j++) {
      if (i == half_filter_width && j == half_filter_height) {
        delta = 1.0;
      } // the center of the filter
      else {
        delta = 0.0;
      }
      sharpening_filter[i][j] = delta + lambda * (delta - h);
    }
  }

  /* Filter each of three color channels of the image */
  for (channel = 0; channel < 3; channel++) {
    /* Allocate image of double precision floats */
    img_temp = (double ** ) get_img(input_img.width + 8, input_img.height + 8, sizeof(double)); 
    /* Filtering process */
    for (i = 0; i < input_img.height + (FILTER_HEIGHT - 1); i++) {
      for (j = 0; j < input_img.width + (FILTER_WIDTH - 1); j++) {

        if ((i >= half_filter_height && i < (input_img.height + half_filter_height)) 
          && (j >= half_filter_width && (j < input_img.width + half_filter_width))) {
          img_temp[i][j] = input_img.color[channel][i - half_filter_height][j - half_filter_width];
        } else {
          img_temp[i][j] = 0;
        }
      }
    }

    for (i = 0; i < input_img.height; i++) {
      for (j = 0; j < input_img.width; j++) {
        sum = 0.0;

        for (k = 0; k < FILTER_HEIGHT; k++) {
          for (l = 0; l < FILTER_WIDTH; l++) {
            sum += sharpening_filter[k][l] * img_temp[i + k][j + l];
          }
        }

        color_img.color[channel][i][j] = limit_image(sum);
      }
    }
    free_img((void ** ) img_temp); // Clear allocated memory after each iteration
  }

  /* open color image file */
  if ((fp = fopen("highpass_img.tif", "wb")) == NULL) {
    fprintf(stderr, "cannot open file color.tif\n");
    exit(1);
  }

  /* write color image */
  if (write_TIFF(fp, & color_img)) {
    fprintf(stderr, "error writing TIFF file %s\n", argv[2]);
    exit(1);
  }

  /* close color image file */
  fclose(fp);

  /* de-allocate space which was used for the images */
  free_TIFF( & (input_img));
  free_TIFF( & (color_img));

  return (0);
}

void error(char * name) {
  printf("usage: %s image.tiff \n\n", name);
  printf("this program reads in a 24-bit color TIFF image.\n");
  printf("It then filters the image with the low-pass filter,\n");
  printf("and writes out the result as a 24-bit image\n");
  printf("with the name 'highpass_img.tiff'.\n");
}
double limit_image(double pixel) {
  if (pixel > 255) return 255;
  if (pixel < 0) return 0;
  return pixel;
}