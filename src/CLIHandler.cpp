#include <unistd.h>
#include "CLIHandler.hpp"

#include "MemoryHandler.hpp"

void CLIHandler::addOptions(Option *options, size_t size)
{
    _opt_string = MemoryHandler::safeAllocate<char>(2 * size + 1);
    _options = {options, size};

    size_t pos = 0;

    for (size_t i = 0; i < size; ++i)
    {
        Option opt = options[i];
        _opt_string[pos++] = opt.name[0];
        if (opt.has_args)
        {
            _opt_string[pos++] = ':';
        }
    }

    _opt_string[pos] = '\0';
}

void CLIHandler::parse(int argc, char **argv)
{
    _program_name = argv[0];

    int opt;
    while ((opt = getopt(argc, argv, _opt_string)) != -1)
    {
        bool found = false;
        for (size_t i = 0; i < _options.size(); ++i)
        {
            Option option = _options[i];
            if (option.name[0] != opt)
                continue;
            option.handler.handler(optarg, option.handler.args);
            found = true;
        }

        if (!found)
        {
            fprintf(stderr, "Unknown option: -%c\n", opt);
            showHelp();
            exit(EXIT_FAILURE);
        }
    }
}

void CLIHandler::showHelp()
{
    printf("Usage: %s [options]\n", _program_name);
    printf("Options:\n");
    for (size_t i = 0; i < _options.size(); ++i)
    {
        Option option = _options[i];
        printf("  -%s\t%s\n", option.name, option.description);
    }
}

CLIHandler::~CLIHandler()
{
    MemoryHandler::freeMemory(_opt_string);
    MemoryHandler::freeMemory(_options.data());
}