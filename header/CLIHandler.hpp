#pragma once

#include "Utils.hpp"
#include "MemoryHandler.hpp"

struct OptionHandler {
  void(*handler)(char*, void*);
  void* args;
  OptionHandler() : handler(nullptr), args(nullptr) {}
  OptionHandler(void(*h)(char*, void*), void* a) : handler(h), args(a) {}
};

struct Option {
  char* name;
  char* description;
  bool has_args;
  OptionHandler handler;
  Option(char* n, char* d, bool h, OptionHandler oh)
    : name(n), description(d), has_args(h), handler(oh) {}
};

class CLIHandler {
private:
    char* _program_name;
    char* _opt_string;
    ut::vector<Option> _options;

public:
    CLIHandler() = default;
  
    void addOptions(Option* options, size_t size);
    void parse(int argc, char** argv);
    void showHelp();

    ~CLIHandler();
};