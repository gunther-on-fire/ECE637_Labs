# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: Image_Restoration

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o

Image_Restoration: Image_Restoration.o $(OBJ) 
	$(CC) $(CFLAGS) -o Image_Restoration Image_Restoration.o $(OBJ) -lm
	mv Image_Restoration $(BIN)
