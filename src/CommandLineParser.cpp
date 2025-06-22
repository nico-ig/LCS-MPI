#include "CommandLineParser.hpp"
#include "MemoryHandler.hpp"

CommandLineParser::CommandLineParser(int argc, char **argv)
{
    _input_files = MemoryHandler::safeAllocate<char *>(2);
    Option *options = MemoryHandler::safeAllocate<Option>(4);

    options[0] = Option(
        (char *)"f",
        (char *)"Path to sequence file. Exactly two paths must be provided",
        true,
        OptionHandler(&CommandLineParser::readInputFiles, reinterpret_cast<void *>(&_input_files)));

    options[1] = Option(
        (char *)"t",
        (char *)"Number of threads to use",
        true,
        OptionHandler(&CommandLineParser::readThreadsNumber, reinterpret_cast<void *>(&_num_threads)));

    options[2] = Option(
        (char *)"b",
        (char *)"Cache line size multiplier for block size",
        true,
        OptionHandler(&CommandLineParser::readBlockMultiplier, reinterpret_cast<void *>(&_block_multiplier)));

    options[3] = Option(
        (char *)"h",
        (char *)"Print usage",
        false,
        OptionHandler(&CommandLineParser::readHelp, reinterpret_cast<void *>(&_help)));

    _cli.addOptions(options, 4);
    _cli.parse(argc, argv);
}

char **CommandLineParser::getInputFiles()
{
    if (!_help && _input_files[1] == nullptr)
    {
        fprintf(stderr, "Error: Exactly two input files are required\n");
        showHelp();
        exit(EXIT_FAILURE);
    }
    return _input_files;
}

ut::utype CommandLineParser::getNumThreads()
{
    if (!_help && _num_threads <= 0)
    {
        fprintf(stderr, "Error: Number of threads must be greater than 0\n");
        showHelp();
        exit(EXIT_FAILURE);
    }
    return _num_threads;
}

ut::utype CommandLineParser::getBlockMultiplier()
{
    if (!_help && _block_multiplier <= 0)
    {
        fprintf(stderr, "Error: Block multiplier must be greater than 0\n");
        showHelp();
        exit(EXIT_FAILURE);
    }
    return _block_multiplier;
}

CommandLineParser::~CommandLineParser()
{
    MemoryHandler::freeMemory(_input_files);
}