#include <math.h>

#include <stdlib.h>

#include "tiff.h"

#include "allocate.h"

#include "randlib.h"

#include "typeutil.h"

struct pixel {
  int m, n; /* m = row, n = col */
};

void ConnectedNeighbors(
  struct pixel s,
  double T,
  unsigned char ** img,
  int width,
  int height,
  int * M,
  struct pixel c[4]);

void ConnectedSet(
  struct pixel s,
  double T,
  unsigned char ** img,
  int width,
  int height,
  int ClassLabel,
  unsigned int ** seg,
  int * NumConPixels);

int main(int argc, char ** argv) {
  FILE * fp;
  struct TIFF_img input_img, output_img;
  struct pixel s;
  unsigned int ** seg;
  double T;
  int ClassLabel = 1;
  int NumConPixels = 0;
  int i, j;

  /* Open image file */
  if ((fp = fopen(argv[1], "rb")) == NULL) {
    fprintf(stderr, "cannot open file %s\n", argv[1]);
    exit(1);
  }

  /* Read image */
  if (read_TIFF(fp, & input_img)) {
    fprintf(stderr, "error reading file %s\n", argv[1]);
    exit(1);
  }

  /* Close image file */
  fclose(fp);

  /* Set the initial lattice point */
  s.m = 67; // row index
  s.n = 45; // column index

  /* Set the threshold */
  T = 1.0;

  /* Set up structure for the output grayscale image */
  get_TIFF( & output_img, input_img.height, input_img.width, 'g');

  /* Allocate memory for for the 2-D array of integers which contains the class of each pixel  */
  seg = (unsigned int ** ) get_img(input_img.width, input_img.height, sizeof(unsigned int));

  ConnectedSet(s, T, input_img.mono, input_img.width, input_img.height, ClassLabel, seg, & NumConPixels);

  /* Get the image with the elements in the connected set printed as black (0) and the remaining pixels printed as white (255) */
  for (i = 0; i < input_img.height; i++) {
    for (j = 0; j < input_img.width; j++) {
      if (seg[i][j] == ClassLabel) {
        output_img.mono[i][j] = 0;
      } else {
        output_img.mono[i][j] = 255;
      }
    }
  }

  /* Open the output image file */
  if ((fp = fopen("output_T=1.tif", "wb")) == NULL) {
    fprintf(stderr, "cannot open file output.tif\n");
    exit(1);
  }

  /* Write the output image */
  if (write_TIFF(fp, & output_img)) {
    fprintf(stderr, "error writing TIFF file %s\n", argv[2]);
    exit(1);
  }

  /* Close the output image file */
  fclose(fp);

  /* De-allocate space which was used for the images */
  free_TIFF( & (input_img));
  free_TIFF( & (output_img));

  free_img((void ** ) seg);

  return (0);
}

void ConnectedNeighbors(
  struct pixel s,
  double T,
  unsigned char ** img,
  int width,
  int height,
  int * M,
  struct pixel c[4]) {
  * M = 0;
  if ((s.m - 1) >= 0 && abs(img[s.m][s.n] - img[s.m - 1][s.n]) <= T) {
    c[ * M].m = s.m - 1;
    c[ * M].n = s.n;
    ( * M) ++;
  }
  if ((s.m + 1) < height && abs(img[s.m][s.n] - img[s.m + 1][s.n]) <= T) {
    c[ * M].m = s.m + 1;
    c[ * M].n = s.n;
    ( * M) ++;
  }
  if ((s.n - 1) >= 0 && abs(img[s.m][s.n] - img[s.m][s.n - 1]) <= T) {
    c[ * M].m = s.m;
    c[ * M].n = s.n - 1;
    ( * M) ++;
  }
  if ((s.n + 1) < width && abs(img[s.m][s.n] - img[s.m][s.n + 1]) <= T) {
    c[ * M].m = s.m;
    c[ * M].n = s.n + 1;
    ( * M) ++;
  }
}

void ConnectedSet(
  struct pixel s,
  double T,
  unsigned char ** img,
  int width,
  int height,
  int ClassLabel,
  unsigned int ** seg,
  int * NumConPixels) {

  int M = 0;
  struct pixel c[4];

  ConnectedNeighbors(s, T, img, width, height, & M, c);

  while (M > 0) {
    if (seg[c[M - 1].m][c[M - 1].n] != ClassLabel) {
      seg[c[M - 1].m][c[M - 1].n] = ClassLabel;
      ( * NumConPixels) ++;
      ConnectedSet(c[M - 1], T, img, width, height, ClassLabel, seg, NumConPixels);
    }
    M--;
  }
}