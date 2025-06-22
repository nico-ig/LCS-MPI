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
    inline static void readThreadsNumber(char* arg, void* num_threads) { *reinterpret_cast<short *>(num_threads) = static_cast<ut::utype>(std::stoi(arg)); } 
    inline static void readBlockMultiplier(char* arg, void* block_multiplier) { *reinterpret_cast<short *>(block_multiplier) = static_cast<short>(std::stoi(arg)); }
    inline static void readHelp(char*, void* help) { *reinterpret_cast<bool *>(help) = true; }

    char** getInputFiles();
    ut::utype getNumThreads();
    ut::utype getBlockMultiplier();

    inline bool helpRequested() { return _help; }
    inline void showHelp() { _cli.showHelp(); }
    
    ~CommandLineParser();
};
