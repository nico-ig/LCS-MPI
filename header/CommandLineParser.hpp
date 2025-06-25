#pragma once

#include "CLIHandler.hpp"
#include "MemoryHandler.hpp"

class CommandLineParser {
private:
    CLIHandler _cli;
    bool _help = false;
    short _num_threads;
    short _block_multiplier;
    char** _input_files;

public:
    CommandLineParser(int argc, char** argv);

    inline static void readInputFiles(char* arg, void* input_files) { static size_t i = 0; (*reinterpret_cast<char ***>(input_files))[i++] = arg; }
    inline static void readHelp(char*, void* help) { *reinterpret_cast<bool *>(help) = true; }

    char** getInputFiles();

    inline bool helpRequested() { return _help; }
    inline void showHelp() { _cli.showHelp(); }
    
    ~CommandLineParser();
};
