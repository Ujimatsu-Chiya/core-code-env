#ifndef CPP_IO_TOOLS_H
#define CPP_IO_TOOLS_H

#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <string>

// Fixed IO files used by generated runners.
const char *READ_PATH = "user.in";
const char *WRITE_PATH = "user.out";

// Thin line-based reader over user.in.
class StdinWrapper
{
private:
    std::ifstream inputFile;

public:
    StdinWrapper()
    {
        inputFile.open(READ_PATH);
        if (!inputFile.is_open())
        {
            std::cerr << "Unable to open input file!" << std::endl;
            exit(1);
        }
    }

    // Returns empty string on EOF.
    std::string read_line()
    {
        std::string line;
        if (std::getline(inputFile, line))
        {
            return line;
        }
        return "";
    }

    ~StdinWrapper()
    {
        if (inputFile.is_open())
        {
            inputFile.close();
        }
    }
};

// Thin line-based writer over user.out.
class StdoutWrapper
{
private:
    std::ofstream outputFile;

public:
    StdoutWrapper()
    {
        outputFile.open(WRITE_PATH);
        if (!outputFile.is_open())
        {
            std::cerr << "Unable to open output file!" << std::endl;
            exit(1);
        }
    }

    void write_line(const std::string &s)
    {
        outputFile << s << '\n';
    }

    ~StdoutWrapper()
    {
        if (outputFile.is_open())
        {
            outputFile.close();
        }
    }
};

#endif // CPP_IO_TOOLS_H
