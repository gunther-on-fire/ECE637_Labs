#include <math.h>
#include "tiff.h"
#include "allocate.h"
#include "randlib.h"
#include "typeutil.h"

void error(char * name);
double limit_image(double pixel);

int main(int argc, char ** argv) {
  FILE * fp;
  struct TIFF_img input_img, color_img;
  double ** img_temp;
  int i, j, k, l;
  uint8_t channel;

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

  /* Filter each of three color channels of the image */
  for (channel = 0; channel < 3; channel++) {

    img_temp = (double ** ) get_img(input_img.width + 1, input_img.height + 1, sizeof(double));

    for (i = 0; i < input_img.height + 1; i++) {
      for (j = 0; j < input_img.width + 1; j++) {
        img_temp[i][j] = 0;
      }
    }
    for (k = 0; k < input_img.height; k++) {
      for (l = 0; l < input_img.width; l++) {
        img_temp[k + 1][l + 1] = 0.01 * input_img.color[channel][k][l] + 0.9 * img_temp[k][l + 1] + 0.9 * img_temp[k + 1][l] - 0.81 * img_temp[k][l];
        color_img.color[channel][k][l] = limit_image(img_temp[k + 1][l + 1]);
      }
    }
    free_img((void ** ) img_temp); // Clear allocated memory after each iteration
  }

  /* open color image file */
  if ((fp = fopen("iir_image.tif", "wb")) == NULL) {
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
  printf("It then filters the image with the IIR filter,\n");
  printf("and writes out the result as a 24-bit image\n");
  printf("with the name 'iir_image.tiff'.\n");
  exit(1);
}

double limit_image(double pixel) {
  if (pixel > 255) return 255;
  if (pixel < 0) return 0;
  return pixel;
}