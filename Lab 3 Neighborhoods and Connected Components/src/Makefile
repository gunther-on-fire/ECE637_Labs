# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: Connected_Sets Image_Segmentation

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o

Connected_Sets: Connected_Sets.o $(OBJ) 
	$(CC) $(CFLAGS) -o Connected_Sets Connected_Sets.o $(OBJ) -lm
	mv Connected_Sets $(BIN)

Image_Segmentation: Image_Segmentation.o $(OBJ) 
	$(CC) $(CFLAGS) -o Image_Segmentation Image_Segmentation.o $(OBJ) -lm
	mv Image_Segmentation $(BIN)
