# include "c_io_tools.h"

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

StdinWrapper* create_stdin_wrapper() {
    StdinWrapper* wrapper = (StdinWrapper*)malloc(sizeof(StdinWrapper));
    if (wrapper == NULL) {
        fprintf(stderr, "Memory allocation failed!\n");
        exit(1);
    }

    wrapper->inputFile = fopen(READ_PATH, "r");
    if (wrapper->inputFile == NULL) {
        fprintf(stderr, "Unable to open input file!\n");
        free(wrapper);
        exit(1);
    }

    fseek(wrapper->inputFile, 0, SEEK_END);
    wrapper->fileSize = ftell(wrapper->inputFile);
    fseek(wrapper->inputFile, 0, SEEK_SET);

    wrapper->line = (char*)malloc((wrapper->fileSize + 1) * sizeof(char));
    if (wrapper->line == NULL) {
        fprintf(stderr, "Memory allocation failed!\n");
        fclose(wrapper->inputFile);
        free(wrapper);
        exit(1);
    }

    return wrapper;
}

char* read_line(StdinWrapper* wrapper) {
    if (fgets(wrapper->line, wrapper->fileSize + 1, wrapper->inputFile) != NULL) {
        wrapper->line[strcspn(wrapper->line, "\n")] = '\0';
        strip(wrapper->line);
        return (wrapper->line[0] != '\0') ? wrapper->line : NULL;
    }
    return NULL;
}

void delete_stdin_wrapper(StdinWrapper* wrapper) {
    if (wrapper != NULL) {
        if (wrapper->inputFile != NULL) {
            fclose(wrapper->inputFile);
        }
        if (wrapper->line != NULL) {
            free(wrapper->line);
        }
        free(wrapper);
    }
}

StdoutWrapper* create_stdout_wrapper() {
    StdoutWrapper* wrapper = (StdoutWrapper*)malloc(sizeof(StdoutWrapper));
    if (wrapper == NULL) {
        fprintf(stderr, "Memory allocation failed!\n");
        exit(1);
    }

    wrapper->outputFile = fopen(WRITE_PATH, "w");
    if (wrapper->outputFile == NULL) {
        fprintf(stderr, "Unable to open output file!\n");
        free(wrapper);
        exit(1);
    }

    return wrapper;
}

void write_line(StdoutWrapper* wrapper, const char* s) {
    if (wrapper->outputFile != NULL) {
        fprintf(wrapper->outputFile, "%s\n", s);
    }
}

void delete_stdout_wrapper(StdoutWrapper* wrapper) {
    if (wrapper != NULL) {
        if (wrapper->outputFile != NULL) {
            fclose(wrapper->outputFile);
        }
        free(wrapper);
    }
}
