#include "CommandLineParser.hpp"
#include "MemoryHandler.hpp"

CommandLineParser::CommandLineParser(int argc, char **argv)
{
    _input_files = MemoryHandler::safeAllocate<char *>(2);
    Option *options = MemoryHandler::safeAllocate<Option>(2);

    options[0] = Option(
        (char *)"f",
        (char *)"Path to sequence file. Exactly two paths must be provided",
        true,
        OptionHandler(&CommandLineParser::readInputFiles, reinterpret_cast<void *>(&_input_files)));

    options[1] = Option(
        (char *)"h",
        (char *)"Print usage",
        false,
        OptionHandler(&CommandLineParser::readHelp, reinterpret_cast<void *>(&_help)));

    _cli.addOptions(options, 2);
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

CommandLineParser::~CommandLineParser()
{
    MemoryHandler::freeMemory(_input_files);
}