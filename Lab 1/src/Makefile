# For Linux or any machines with gcc compiler
CC = gcc 
CFLAGS = -std=c99 -Wall -pedantic
BIN = ../bin

all: FIR_LP_Filter FIR_Sharpening_Filter IIR_Filter

clean:
	/bin/rm *.o $(BIN)/*

OBJ = tiff.o allocate.o randlib.o

FIR_LP_Filter: FIR_LP_Filter.o $(OBJ) 
	$(CC) $(CFLAGS) -o FIR_LP_Filter FIR_LP_Filter.o $(OBJ) -lm
	mv FIR_LP_Filter $(BIN)

FIR_Sharpening_Filter: FIR_Sharpening_Filter.o $(OBJ) 
	$(CC) $(CFLAGS) -o FIR_Sharpening_Filter FIR_Sharpening_Filter.o $(OBJ) -lm
	mv FIR_Sharpening_Filter $(BIN)

IIR_Filter: IIR_Filter.o $(OBJ) 
	$(CC) $(CFLAGS) -o IIR_Filter IIR_Filter.o $(OBJ) -lm
	mv IIR_Filter $(BIN)

