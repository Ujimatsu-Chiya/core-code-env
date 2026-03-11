#ifndef C_IO_TOOLS_H
#define C_IO_TOOLS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    FILE* inputFile;
    char* line;
    long fileSize;
} StdinWrapper;

StdinWrapper* create_stdin_wrapper();
char* read_line(StdinWrapper* wrapper);
void delete_stdin_wrapper(StdinWrapper* wrapper);

typedef struct {
    FILE* outputFile;
} StdoutWrapper;

StdoutWrapper* create_stdout_wrapper();
void write_line(StdoutWrapper* wrapper, const char* s);
void delete_stdout_wrapper(StdoutWrapper* wrapper);

#endif // C_IO_TOOLS_H