#ifndef CPP_IO_TOOLS_H
#define CPP_IO_TOOLS_H

#include <iostream>
#include <fstream>
#include <cstring>

const char* READ_PATH = "user.in";
const char* WRITE_PATH = "user.out";

void strip(char* str) {
    int start = 0;
    while (isspace((unsigned char)str[start])) {
        start++;
    }
    int end = strlen(str) - 1;
    while (end >= start && isspace((unsigned char)str[end])) {
        end--;
    }
    int len = end - start + 1;
    if (len > 0) {
        memmove(str, str + start, len);
        str[len] = '\0';
    } else {
        str[0] = '\0';
    }
}

class StdinWrapper {
private:
    FILE* inputFile;
    char* line;
    long fileSize;

public:
    StdinWrapper() {
        inputFile = fopen(READ_PATH, "r");
        if (inputFile == nullptr) {
            std::cerr << "Unable to open input file!" << std::endl;
            exit(1);
        }

        fseek(inputFile, 0, SEEK_END);
        fileSize = ftell(inputFile);
        fseek(inputFile, 0, SEEK_SET);

        line = new char[fileSize + 1];
    }

    char* read_line() {
        if (fgets(line, fileSize + 1, inputFile) != nullptr) {
            line[strcspn(line, "\n")] = '\0';
            strip(line);
            return (line[0] != '\0') ? line : nullptr;
        }
        return nullptr;
    }

    ~StdinWrapper() {
        if (inputFile != nullptr) {
            fclose(inputFile);
        }
        delete[] line;
    }
};

class StdoutWrapper {
private:
    FILE* outputFile;

public:
    StdoutWrapper() {
        outputFile = fopen(WRITE_PATH, "w");
        if (outputFile == nullptr) {
            std::cerr << "Unable to open output file!" << std::endl;
            exit(1);
        }
    }

    void write_line(const char* s) {
        fprintf(outputFile, "%s\n", s);
    }

    ~StdoutWrapper() {
        if (outputFile != nullptr) {
            fclose(outputFile);
        }
    }
};

#endif // CPP_IO_TOOLS_H